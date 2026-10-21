import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from scripts import fetch_news


class FakeResponse:
    def __init__(self, body):
        self.body = body.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.body


class FetchNewsTests(unittest.TestCase):
    def test_systems_feed_filters_irrelevant_articles_and_cleans_summary(self):
        rss = """<?xml version="1.0"?>
        <rss><channel>
          <item>
            <title>L'IA automatise l'administration des systèmes</title>
            <link>https://example.test/ia</link>
            <description><![CDATA[<p>Un <strong>nouvel outil</strong> pour les équipes.</p>]]></description>
            <pubDate>Wed, 14 Oct 2026 08:30:00 +0000</pubDate>
          </item>
          <item>
            <title>Un nouvel écran pour les joueurs</title>
            <link>https://example.test/ecran</link>
            <description>Présentation du modèle cette semaine.</description>
          </item>
        </channel></rss>"""

        with patch.object(fetch_news.urllib.request, "urlopen", return_value=FakeResponse(rss)):
            articles = fetch_news.fetch_articles(
                {"axis": "systems", "source": "IT-Connect", "url": "https://feed.test/rss"}
            )

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["title"], "L'IA automatise l'administration des systèmes")
        self.assertEqual(articles[0]["summary"], "Un nouvel outil pour les équipes.")
        self.assertEqual(articles[0]["publishedAt"], "2026-10-14T08:30:00Z")

    def test_ai_cyber_feed_requires_both_topics(self):
        rss = """<?xml version="1.0"?>
        <rss><channel>
          <item>
            <title>AI improves cybersecurity threat detection</title>
            <link>https://example.test/ai-cyber</link>
            <description>Security teams assess the new model.</description>
          </item>
          <item>
            <title>AI assistants for developers</title>
            <link>https://example.test/ai-only</link>
            <description>New tools for daily work.</description>
          </item>
          <item>
            <title>Privacy-preserving AI can protect heart data</title>
            <link>https://example.test/heart-data</link>
            <description>The threat model fit on a sticky note.</description>
          </item>
        </channel></rss>"""

        with patch.object(fetch_news.urllib.request, "urlopen", return_value=FakeResponse(rss)):
            articles = fetch_news.fetch_articles(
                {"axis": "ai-cyber", "source": "SecurityWeek", "url": "https://feed.test/rss"}
            )

        self.assertEqual([article["url"] for article in articles], ["https://example.test/ai-cyber"])

    def test_failed_feed_keeps_its_previous_articles(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "articles.json"
            previous = {
                "updatedAt": "2026-10-20T08:00:00Z",
                "articles": [
                    {
                        "axis": "security",
                        "title": "Bulletin déjà collecté",
                        "url": "https://example.test/security",
                    }
                ],
            }
            output_path.write_text(json.dumps(previous), encoding="utf-8")
            feeds = (
                {"axis": "security", "source": "CERT-FR", "url": "https://feed.test/security"},
                {"axis": "systems", "source": "IT-Connect", "url": "https://feed.test/systems"},
                {"axis": "ai-cyber", "source": "SecurityWeek", "url": "https://feed.test/ai"},
            )
            errors = io.StringIO()

            with (
                patch.object(fetch_news, "OUTPUT_PATH", output_path),
                patch.object(fetch_news, "FEEDS", feeds),
                patch.object(fetch_news, "fetch_articles", side_effect=[OSError("indisponible"), [], []]),
                redirect_stderr(errors),
            ):
                fetch_news.main()

            result = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(result["articles"], previous["articles"])
        self.assertIn("CERT-FR", errors.getvalue())

    def test_all_failed_feeds_do_not_overwrite_existing_data(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "articles.json"
            output_path.write_text('{"updatedAt":"old","articles":[]}\n', encoding="utf-8")
            feeds = (
                {"axis": "security", "source": "CERT-FR", "url": "https://feed.test/security"},
                {"axis": "systems", "source": "IT-Connect", "url": "https://feed.test/systems"},
                {"axis": "ai-cyber", "source": "SecurityWeek", "url": "https://feed.test/ai"},
            )

            with (
                patch.object(fetch_news, "OUTPUT_PATH", output_path),
                patch.object(fetch_news, "FEEDS", feeds),
                patch.object(fetch_news, "fetch_articles", side_effect=OSError("indisponible")),
                redirect_stderr(io.StringIO()),
                self.assertRaises(RuntimeError),
            ):
                fetch_news.main()

            self.assertEqual(
                output_path.read_text(encoding="utf-8"),
                '{"updatedAt":"old","articles":[]}\n',
            )


if __name__ == "__main__":
    unittest.main()
