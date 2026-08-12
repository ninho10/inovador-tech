#!/usr/bin/env bash
# Atualiza somente o serviço site da stack sitesinovador.
# Fonte versionada no repositório; o Cron do Hermes chama este arquivo via wrapper.
set -Eeuo pipefail

export TZ="${TZ:-America/Sao_Paulo}"

REPO="/home/ubuntu/sitesinovador/landing-page"
COMPOSE_FILE="/home/ubuntu/sitesinovador/docker-compose.yml"
SERVICE="site"
CONTAINER="sitesinovador-site-1"
REMOTE="origin"
BRANCH="main"
PUBLIC_BASE="https://sitesinovador.com.br"
STATE_ROOT="/home/ubuntu/backups/inovador-tech-site"
LOCK_FILE="/home/ubuntu/.cache/inovador-tech-site-update.lock"
DEPLOYED_COMMIT_FILE="$STATE_ROOT/current_commit"

mkdir -p "$(dirname "$LOCK_FILE")" "$STATE_ROOT"
exec 9>"$LOCK_FILE"
flock -n 9 || exit 0

cd "$REPO"

log_file=""
log() {
    local line
    line="[$(date --iso-8601=seconds)] $*"
    if [[ -n "$log_file" ]]; then
        printf '%s\n' "$line" | tee -a "$log_file"
    else
        printf '%s\n' "$line"
    fi
}

fail_before_update() {
    log "ERROR: $*"
    exit 1
}

if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
    fail_before_update "branch local diferente de $BRANCH"
fi

# Durante o rollback para uma versão anterior ao versionamento do deploy, os
# artefatos locais podem voltar a aparecer como untracked. Eles são permitidos
# somente nestes caminhos; qualquer outra divergência bloqueia o deploy.
working_tree_status="$(git status --porcelain=v1)"
if [[ -n "$working_tree_status" ]]; then
    while IFS= read -r status_line; do
        case "$status_line" in
            "?? .dockerignore"|"?? Dockerfile"|"?? scripts/"|"?? scripts/update-site.sh") ;;
            *) fail_before_update "working tree não está limpa; divergência: $status_line" ;;
        esac
    done <<< "$working_tree_status"
fi

if ! sudo -n docker info >/dev/null 2>&1; then
    fail_before_update "Docker não está acessível via sudo sem interação"
fi

if ! git fetch --prune "$REMOTE" "$BRANCH" >/dev/null 2>&1; then
    fail_before_update "git fetch falhou"
fi

source_commit="$(git rev-parse HEAD)"
remote_commit="$(git rev-parse "$REMOTE/$BRANCH")"

deployed_commit=""
if [[ -f "$DEPLOYED_COMMIT_FILE" ]]; then
    deployed_commit="$(tr -d '[:space:]' < "$DEPLOYED_COMMIT_FILE")"
fi

if [[ -z "$deployed_commit" ]]; then
    deployed_commit="$source_commit"
    printf '%s\n' "$deployed_commit" > "$DEPLOYED_COMMIT_FILE"
fi

if [[ -n "$deployed_commit" ]] && ! git cat-file -e "$deployed_commit^{commit}" 2>/dev/null; then
    fail_before_update "commit registrado como implantado não existe no clone local"
fi

if [[ "$source_commit" == "$remote_commit" ]] && [[ "$deployed_commit" == "$remote_commit" ]]; then
    # Execução saudável e sem alteração: stdout vazio evita ruído no canal.
    exit 0
fi

previous_commit="$deployed_commit"

stamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_dir="$STATE_ROOT/$stamp"
mkdir -p "$backup_dir"
log_file="$backup_dir/update.log"

previous_image="$(sudo -n docker inspect "$CONTAINER" --format '{{.Image}}' 2>/dev/null || true)"
if [[ "$source_commit" != "$previous_commit" ]]; then
    log_file="$backup_dir/preflight.log"
    log "ERROR: checkout local diverge do commit registrado como implantado; intervenção manual necessária"
    exit 1
fi

printf '%s\n' "$previous_commit" > "$backup_dir/previous_commit"
printf '%s\n' "$source_commit" > "$backup_dir/source_commit_before_update"
printf '%s\n' "$remote_commit" > "$backup_dir/target_commit"
printf '%s\n' "$previous_image" > "$backup_dir/previous_image"
sudo -n docker inspect "$CONTAINER" > "$backup_dir/previous_container.json"
git show -s --format=fuller "$previous_commit" > "$backup_dir/previous_commit.txt"
git show -s --format=fuller "$remote_commit" > "$backup_dir/target_commit.txt"

log "UPDATE: $previous_commit -> $remote_commit"

rollback() {
    log "ROLLBACK: retornando para $previous_commit"
    local rollback_ok=1

    if ! git reset --hard "$previous_commit" >"$backup_dir/rollback-git.log" 2>&1; then
        log "ERROR: não foi possível restaurar o commit anterior"
        rollback_ok=0
    fi

    if (( rollback_ok )); then
        if ! sudo -n docker compose -f "$COMPOSE_FILE" build "$SERVICE" >"$backup_dir/rollback-build.log" 2>&1; then
            log "ERROR: rebuild da versão anterior falhou"
            rollback_ok=0
        fi
    fi

    if (( rollback_ok )); then
        if ! sudo -n docker compose -f "$COMPOSE_FILE" up -d --no-deps "$SERVICE" >"$backup_dir/rollback-up.log" 2>&1; then
            log "ERROR: recriação do container anterior falhou"
            rollback_ok=0
        fi
    fi

    if (( rollback_ok )); then
        if ! wait_for_site; then
            log "ERROR: versão anterior não respondeu no probe interno"
            rollback_ok=0
        fi
    fi

    if (( rollback_ok )); then
        if ! probe_public_root; then
            log "ERROR: versão anterior não respondeu no probe público"
            rollback_ok=0
        fi
    fi

    if (( rollback_ok )); then
        printf '%s\n' "$previous_commit" > "$DEPLOYED_COMMIT_FILE"
        log "ROLLBACK_OK: serviço restaurado; atualização ficará pendente para a próxima execução"
    else
        log "ROLLBACK_FAILED: intervenção manual necessária"
    fi
}

wait_for_site() {
    local attempt code
    for attempt in $(seq 1 30); do
        if sudo -n docker inspect "$CONTAINER" --format '{{.State.Running}}' 2>/dev/null | grep -qx true; then
            code="$(sudo -n docker exec "$CONTAINER" python3 -c 'import urllib.request; print(urllib.request.urlopen("http://127.0.0.1:3000/", timeout=3).status)' 2>/dev/null || true)"
            if [[ "$code" == "200" ]]; then
                return 0
            fi
        fi
        sleep 2
    done
    return 1
}

probe_public_root() {
    local body="${backup_dir:-/tmp}/public-root.html"
    local code
    code="$(curl --fail --silent --show-error --location --retry 3 --retry-delay 2 --max-time 30 -o "$body" -w '%{http_code}' "$PUBLIC_BASE/" 2>/dev/null || true)"
    [[ "$code" == "200" ]]
}

probe_public_updated() {
    local path code body
    for path in / /nossos-servicos /demo/academia; do
        body="$backup_dir/public-${path//\//_}.html"
        code="$(curl --fail --silent --show-error --location --retry 3 --retry-delay 2 --max-time 30 -o "$body" -w '%{http_code}' "$PUBLIC_BASE$path" 2>/dev/null || true)"
        if [[ "$code" != "200" ]]; then
            log "PROBE_FAILED: $path HTTP=$code"
            return 1
        fi
    done
    return 0
}

if ! git merge --ff-only "$REMOTE/$BRANCH" >"$backup_dir/merge.log" 2>&1; then
    log "ERROR: fast-forward do repositório falhou"
    exit 1
fi

if ! sudo -n docker compose -f "$COMPOSE_FILE" build "$SERVICE" >"$backup_dir/build.log" 2>&1; then
    log "ERROR: build da nova versão falhou; log=$backup_dir/build.log"
    rollback
    exit 1
fi

if ! sudo -n docker compose -f "$COMPOSE_FILE" up -d --no-deps "$SERVICE" >"$backup_dir/up.log" 2>&1; then
    log "ERROR: recriação do container da nova versão falhou; log=$backup_dir/up.log"
    rollback
    exit 1
fi

if ! wait_for_site; then
    log "ERROR: nova versão não respondeu no probe interno"
    rollback
    exit 1
fi

if ! probe_public_updated; then
    log "ERROR: nova versão falhou no probe público"
    rollback
    exit 1
fi

new_image="$(sudo -n docker inspect "$CONTAINER" --format '{{.Image}}')"
container_started="$(sudo -n docker inspect "$CONTAINER" --format '{{.State.StartedAt}}')"
printf '%s\n' "$new_image" > "$backup_dir/new_image"
printf '%s\n' "$container_started" > "$backup_dir/container_started_at"
printf '%s\n' "$remote_commit" > "$DEPLOYED_COMMIT_FILE"

log "UPDATE_OK: commit=$remote_commit container=$CONTAINER image=$new_image started=$container_started"
exit 0
