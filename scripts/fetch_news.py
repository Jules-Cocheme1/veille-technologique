import json
import os
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path


OUTPUT_PATH = Path("docs/data/articles.json")
MAX_ARTICLES_PER_AXIS = 8
FEEDS = (
    {
        "axis": "security",
        "source": "CERT-FR",
        "url": "https://www.cert.ssi.gouv.fr/feed/",
    },
    {
        "axis": "systems",
        "source": "IT-Connect",
        "url": "https://www.it-connect.fr/feed/",
    },
    {
        "axis": "ai-cyber",
        "source": "SecurityWeek",
        "url": "https://www.securityweek.com/feed/",
    },
)

SYSTEMS_TERMS = (
    "intelligence artificielle",
    "artificial intelligence",
    "machine learning",
    "generative ai",
    "aiops",
    "automatisation",
    "automation",
    "copilot",
    "ansible",
    "terraform",
    "infrastructure as code",
)
AI_TERMS = (
    "intelligence artificielle",
    "artificial intelligence",
    "machine learning",
    "generative ai",
    "large language model",
    "llm",
)
CYBER_TERMS = (
    "cyber",
    "securite",
    "security",
    "ransomware",
    "malware",
    "phishing",
    "incident response",
    "security operations",
    "threat actor",
    "hack",
    "hacking",
    "breach",
    "vulnerability",
    "soc",
)


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def clean_text(value):
    extractor = TextExtractor()
    extractor.feed(value or "")
    return " ".join(" ".join(extractor.parts).split())


def clean_summary(value):
    summary = clean_text(value)
    return re.sub(r"\s*(?:the post|le post)\b.*$", "", summary, flags=re.IGNORECASE).strip()


def normalize(value):
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def contains_short_ai_term(text):
    return re.search(r"\b(?:ia|ai)\b", text) is not None


def matches_any(text, terms):
    return any(term in text for term in terms)


def direct_child_text(element, names):
    for child in element:
        if child.tag.rsplit("}", 1)[-1].casefold() in names:
            return "".join(child.itertext()).strip()
    return ""


def entry_link(element):
    for child in element:
        if child.tag.rsplit("}", 1)[-1].casefold() == "link":
            link = child.attrib.get("href", "").strip()
            if link:
                return link
            return "".join(child.itertext()).strip()
    return ""


def parse_date(value):
    if not value:
        return None
    try:
        result = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        try:
            result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if result.tzinfo is None:
        result = result.replace(tzinfo=timezone.utc)
    return result.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_relevant(axis, title, summary):
    text = normalize(f"{title} {summary}")
    if axis == "systems":
        return contains_short_ai_term(text) or matches_any(text, SYSTEMS_TERMS)
    if axis == "ai-cyber":
        has_ai = contains_short_ai_term(text) or matches_any(text, AI_TERMS)
        return has_ai and matches_any(text, CYBER_TERMS)
    return True


def fetch_articles(feed):
    request = urllib.request.Request(
        feed["url"],
        headers={"User-Agent": "VeilleTechnologique/1.0 (+https://github.com/Jules-Cocheme1/veille-technologique)"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        root = ET.fromstring(response.read())

    articles = []
    seen_urls = set()
    entries = [
        element
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1].casefold() in {"item", "entry"}
    ]

    for entry in entries:
        title = clean_text(direct_child_text(entry, {"title"}))
        url = entry_link(entry)
        summary = clean_summary(
            direct_child_text(entry, {"description", "summary", "content", "encoded"})
        )
        if not title or not url or url in seen_urls or not url.startswith(("https://", "http://")):
            continue
        if not is_relevant(feed["axis"], title, summary[:500]):
            continue

        seen_urls.add(url)
        articles.append(
            {
                "axis": feed["axis"],
                "title": title,
                "summary": summary[:260] or "Ouvrir la source pour consulter la publication.",
                "source": feed["source"],
                "url": url,
                "publishedAt": parse_date(
                    direct_child_text(entry, {"pubdate", "published", "updated", "date"})
                ),
            }
        )
        if len(articles) == MAX_ARTICLES_PER_AXIS:
            break

    return articles


def read_previous_articles():
    if not OUTPUT_PATH.exists():
        return {}
    with OUTPUT_PATH.open(encoding="utf-8") as existing_file:
        previous_data = json.load(existing_file)
    if not isinstance(previous_data, dict) or not isinstance(previous_data.get("articles"), list):
        raise ValueError(f"Le fichier {OUTPUT_PATH} ne respecte pas le format attendu.")
    return {
        feed["axis"]: [
            article
            for article in previous_data["articles"]
            if isinstance(article, dict) and article.get("axis") == feed["axis"]
        ]
        for feed in FEEDS
    }


def main():
    previous_articles = read_previous_articles()
    collected_articles = []
    failed_feeds = []

    for feed in FEEDS:
        try:
            articles = fetch_articles(feed)
        except (OSError, ET.ParseError, ValueError) as error:
            print(
                f"Avertissement : collecte impossible pour {feed['source']} ({feed['url']}) : {error}",
                file=sys.stderr,
            )
            failed_feeds.append(feed["source"])
            collected_articles.extend(previous_articles.get(feed["axis"], []))
            continue
        collected_articles.extend(articles)

    if len(failed_feeds) == len(FEEDS):
        raise RuntimeError("Aucun flux RSS n'a pu être collecté ; le fichier existant est conservé.")

    collected_articles.sort(
        key=lambda article: article.get("publishedAt") or "",
        reverse=True,
    )
    payload = {
        "updatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "articles": collected_articles,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = OUTPUT_PATH.with_suffix(".json.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as output_file:
            json.dump(payload, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")
        os.replace(temporary_path, OUTPUT_PATH)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    print(f"{len(collected_articles)} publication(s) enregistrée(s) dans {OUTPUT_PATH}.")
    if failed_feeds:
        print(f"Flux indisponibles, publications précédentes conservées : {', '.join(failed_feeds)}.")


if __name__ == "__main__":
    main()
