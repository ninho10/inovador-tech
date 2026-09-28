import sys
import unittest
from pathlib import Path

from werkzeug.serving import make_server
import threading

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app import app


class RuntimePopupBrowserContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server('127.0.0.1', 0, app)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def get(self, path):
        import http.client
        connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=5)
        connection.request('GET', path)
        response = connection.getresponse()
        body = response.read().decode('utf-8')
        headers = dict(response.getheaders())
        connection.close()
        return response.status, headers, body

    def test_home_serves_banner_without_popup_assets(self):
        status, _, body = self.get('/')
        self.assertEqual(status, 200)
        self.assertIn('id="oraculo-free-banner"', body)
        self.assertIn('href="https://oraculo-crm.sitesinovador.com.br/"', body)
        self.assertIn('Testar o Oráculo CRM grátis', body)
        self.assertNotIn('oraculo-free-popup', body)
        self.assertNotIn('oraculo-popup.css', body)
        self.assertNotIn('oraculo-popup.js', body)

        css_status, css_headers, css = self.get('/static/css/oraculo-banner.css')
        self.assertEqual(css_status, 200)
        self.assertIn('text/css', css_headers.get('Content-Type', ''))
        self.assertIn('oraculo-banner', css)

    def test_all_rendered_routes_have_no_global_popup(self):
        routes = ["/", "/oraculo", "/sistema-sob-medida", "/planilhas", "/sites", "/nossos-servicos"]
        routes.extend(f"/demo/{slug}" for slug in (
            "academia", "barbearia", "clinica", "consultorio", "escola", "hotel",
            "imobiliaria", "loja", "oficina", "planilha", "restaurante", "salao",
        ))
        for route in routes:
            with self.subTest(route=route):
                status, _, body = self.get(route)
                self.assertEqual(status, 200)
                self.assertNotIn('oraculo-free-popup', body)
                self.assertNotIn('oraculo-popup.css', body)
                self.assertNotIn('oraculo-popup.js', body)


if __name__ == '__main__':
    unittest.main()
