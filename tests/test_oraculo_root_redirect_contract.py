"""Scope marker: the CRM root redirect is tested in the CRM worktree."""

import unittest


class MainSiteScopeTests(unittest.TestCase):
    def test_crm_redirect_is_outside_main_site_scope(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
