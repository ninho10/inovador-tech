/**
 * Lógica principal do site Inovador Tech
 * Main logic for Inovador Tech website
 */

document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('mainNav');
    const cursor = document.getElementById('custom-cursor');
    const cursorGlow = document.getElementById('cursor-glow');

    // Cursor customizado apenas para dispositivos com mouse (não touch)
    // Custom cursor only for non-touch (mouse) devices
    const isTouchDevice = window.matchMedia('(hover: none) and (pointer: coarse)').matches;

    if (!isTouchDevice && cursor && cursorGlow) {
        // Movimentação do Cursor Customizado / Custom Cursor Movement
        document.addEventListener('mousemove', (e) => {
            cursor.style.display = 'block';
            cursorGlow.style.display = 'block';

            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';

            // O brilho segue com um leve atraso / Glow follows with slight delay
            cursorGlow.style.left = (e.clientX - 15) + 'px';
            cursorGlow.style.top = (e.clientY - 15) + 'px';
        });

        // Esconde o cursor quando o mouse sai da janela / Hide cursor on mouse leave
        document.addEventListener('mouseleave', () => {
            cursor.style.display = 'none';
            cursorGlow.style.display = 'none';
        });

        // Efeito de clique no cursor / Cursor click effect
        document.addEventListener('mousedown', () => cursor.style.transform = 'scale(0.8)');
        document.addEventListener('mouseup', () => cursor.style.transform = 'scale(1)');
    }

    // Altera o fundo da navbar ao rolar a página / Changes navbar background on scroll
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Inicialização do TSParticles v2 com API correta
    // TSParticles v2 Initialization with correct API
    const particlesContainer = document.getElementById('tsparticles');
    if (typeof tsParticles !== 'undefined' && particlesContainer) {
        tsParticles.load("tsparticles", {
            fpsLimit: 60,
            particles: {
                number: {
                    value: 60,
                    density: { enable: true, area: 800 }
                },
                color: { value: "#00f3ff" },
                shape: { type: "circle" },
                opacity: { value: 0.3, random: true },
                size: { value: 2, random: true },
                links: {
                    enable: true,
                    distance: 150,
                    color: "#00f3ff",
                    opacity: 0.1,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 0.8,
                    direction: "none",
                    random: false,
                    straight: false,
                    outModes: { default: "out" },
                    bounce: false
                }
            },
            interactivity: {
                detectsOn: "canvas",
                events: {
                    onHover: { enable: true, mode: "grab" },
                    onClick: { enable: true, mode: "push" },
                    resize: true
                },
                modes: {
                    grab: { distance: 140, links: { opacity: 0.5 } },
                    push: { quantity: 4 }
                }
            },
            detectRetina: true
        });
    }

    // Smooth scroll para links internos / Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    console.log("Inovador Tech: Interface de Alta Tecnologia Pronta!");
});
