import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app

TEMPLATES = ROOT / "templates"
PARTIAL = TEMPLATES / "_oraculo_popup.html"
POPUP_CSS = ROOT / "static" / "css" / "oraculo-popup.css"
POPUP_JS = ROOT / "static" / "js" / "oraculo-popup.js"
PAGE_TEMPLATES = sorted(
    path for path in TEMPLATES.rglob("*.html") if path.name != "_oraculo_popup.html"
)
DEMO_SLUGS = (
    "academia", "barbearia", "clinica", "consultorio", "escola", "hotel",
    "imobiliaria", "loja", "oficina", "planilha", "restaurante", "salao",
)


class GlobalOraculoPopupContractTests(unittest.TestCase):
    def test_all_page_templates_include_shared_assets_and_partial_once(self):
        self.assertEqual(len(PAGE_TEMPLATES), 18)
        for template in PAGE_TEMPLATES:
            source = template.read_text(encoding="utf-8")
            with self.subTest(template=template.relative_to(TEMPLATES)):
                self.assertEqual(source.count("oraculo-popup.css"), 1)
                self.assertEqual(source.count("oraculo-popup.js"), 1)
                self.assertEqual(source.count("{% include '_oraculo_popup.html' %}"), 1)
                self.assertEqual(source.count('id="oraculo-free-popup"'), 0)

    def test_shared_partial_has_cta_and_non_javascript_fallback(self):
        source = PARTIAL.read_text(encoding="utf-8")
        required = (
            'id="oraculo-free-popup"',
            'role="dialog"',
            'aria-modal="true"',
            'data-popup-cta="oraculo-free"',
            'https://oraculo-crm.sitesinovador.com.br/',
            'id="oraculo-free-popup-dismiss"',
            '<noscript>',
            'aria-label="Benefícios do Oráculo CRM"',
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, source)

    def test_rendered_routes_contain_the_popup_once(self):
        routes = ["/", "/oraculo", "/sistema-sob-medida", "/planilhas", "/sites", "/nossos-servicos"]
        routes.extend(f"/demo/{slug}" for slug in DEMO_SLUGS)
        with app.test_client() as client:
            for route in routes:
                response = client.get(route)
                with self.subTest(route=route):
                    self.assertEqual(response.status_code, 200)
                    body = response.get_data(as_text=True)
                    self.assertEqual(body.count('id="oraculo-free-popup"'), 1)
                    self.assertIn('href="https://oraculo-crm.sitesinovador.com.br/"', body)

    def test_popup_behavior_keeps_frequency_and_accessibility_guards(self):
        css = POPUP_CSS.read_text(encoding="utf-8")
        js = POPUP_JS.read_text(encoding="utf-8")
        js_tokens = (
            "sessionStorage", "localStorage", "event.key === 'Escape'",
            "firstFocusable", "lastFocusable", "closeButtons.forEach",
            "if (cta)", "cta.addEventListener",
        )
        css_tokens = (
            "prefers-reduced-motion", "max-height: calc(100dvh - 24px)",
        )
        for token in js_tokens:
            with self.subTest(token=token):
                self.assertIn(token, js)
        for token in css_tokens:
            with self.subTest(token=token):
                self.assertIn(token, css)


if __name__ == "__main__":
    unittest.main()
