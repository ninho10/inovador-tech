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

    def test_home_serves_rendered_popup_assets(self):
        status, _, body = self.get('/')
        self.assertEqual(status, 200)
        self.assertIn('id="oraculo-free-popup"', body)
        self.assertNotIn("{% include '_oraculo_popup.html' %}", body)

        css_status, css_headers, css = self.get('/static/css/oraculo-popup.css')
        js_status, js_headers, js = self.get('/static/js/oraculo-popup.js')
        self.assertEqual(css_status, 200)
        self.assertEqual(js_status, 200)
        self.assertIn('text/css', css_headers.get('Content-Type', ''))
        self.assertIn('javascript', js_headers.get('Content-Type', ''))
        self.assertIn('oraculo-popup-enter', css)
        self.assertIn("event.key === 'Escape'", js)

    def test_all_rendered_routes_have_one_popup(self):
        routes = ["/", "/oraculo", "/sistema-sob-medida", "/planilhas", "/sites", "/nossos-servicos"]
        routes.extend(f"/demo/{slug}" for slug in (
            "academia", "barbearia", "clinica", "consultorio", "escola", "hotel",
            "imobiliaria", "loja", "oficina", "planilha", "restaurante", "salao",
        ))
        for route in routes:
            with self.subTest(route=route):
                status, _, body = self.get(route)
                self.assertEqual(status, 200)
                self.assertEqual(body.count('id="oraculo-free-popup"'), 1)
                self.assertIn('data-popup-cta="oraculo-free"', body)


if __name__ == '__main__':
    unittest.main()
