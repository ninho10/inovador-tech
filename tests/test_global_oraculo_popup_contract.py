import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app

TEMPLATES = ROOT / "templates"
PAGE_TEMPLATES = sorted(
    path for path in TEMPLATES.rglob("*.html")
    if path.name not in {"_oraculo_popup.html", "_oraculo_banner.html"}
)
DEMO_SLUGS = (
    "academia", "barbearia", "clinica", "consultorio", "escola", "hotel",
    "imobiliaria", "loja", "oficina", "planilha", "restaurante", "salao",
)
POPUP_TOKENS = (
    "oraculo-popup.css",
    "oraculo-popup.js",
    "_oraculo_popup.html",
    "oraculo-free-popup",
)


class GlobalOraculoPopupContractTests(unittest.TestCase):
    def test_popup_is_not_referenced_by_any_page_template(self):
        self.assertEqual(len(PAGE_TEMPLATES), 18)
        for template in PAGE_TEMPLATES:
            source = template.read_text(encoding="utf-8")
            with self.subTest(template=template.relative_to(TEMPLATES)):
                for token in POPUP_TOKENS:
                    self.assertNotIn(token, source)

        popup_partial = (TEMPLATES / "_oraculo_popup.html").read_text(encoding="utf-8")
        self.assertNotIn('id="oraculo-free-popup"', popup_partial)

    def test_home_has_the_crm_banner_and_other_pages_do_not(self):
        home = (TEMPLATES / "index.html").read_text(encoding="utf-8")
        self.assertIn("oraculo-banner.css", home)
        self.assertIn("_oraculo_banner.html", home)
        banner = (TEMPLATES / "_oraculo_banner.html").read_text(encoding="utf-8")
        self.assertIn('id="oraculo-free-banner"', banner)
        self.assertIn('href="https://oraculo-crm.sitesinovador.com.br/"', banner)
        self.assertIn("Testar o Oráculo CRM grátis", banner)

        for template in PAGE_TEMPLATES:
            if template.name == "index.html":
                continue
            source = template.read_text(encoding="utf-8")
            with self.subTest(template=template.relative_to(TEMPLATES)):
                self.assertNotIn("oraculo-banner.css", source)
                self.assertNotIn("_oraculo_banner.html", source)

    def test_rendered_routes_do_not_contain_popup_and_only_home_has_banner(self):
        routes = ["/", "/oraculo", "/sistema-sob-medida", "/planilhas", "/sites", "/nossos-servicos"]
        routes.extend(f"/demo/{slug}" for slug in DEMO_SLUGS)
        with app.test_client() as client:
            for route in routes:
                response = client.get(route)
                with self.subTest(route=route):
                    self.assertEqual(response.status_code, 200)
                    body = response.get_data(as_text=True)
                    for token in POPUP_TOKENS:
                        self.assertNotIn(token, body)
                    if route == "/":
                        self.assertIn('id="oraculo-free-banner"', body)
                        self.assertIn('href="https://oraculo-crm.sitesinovador.com.br/"', body)
                    else:
                        self.assertNotIn('id="oraculo-free-banner"', body)


if __name__ == "__main__":
    unittest.main()
