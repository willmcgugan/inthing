"""Test inthing.urls."""

from __future__ import print_function
from __future__ import unicode_literals

import unittest

from inthing import urls


class TestURLs(unittest.TestCase):
    """Test URLs."""

    def test_urls(self):
        """Test URL constants."""
        self.assertEqual(urls.inthing_url, "https://www.inthing.io")
        self.assertEqual(urls.rpc_url, "https://www.inthing.io/api/public/")
        self.assertEqual(urls.event_url, "https://www.inthing.io/api/new-event/")
