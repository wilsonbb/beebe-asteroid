"""Check local links in the exported HTML without contacting upstream services."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import os

ROOT = Path("dist/client")
BASE = os.environ.get("BASE_PATH", "").rstrip("/")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        for key in ("href", "src"):
            if key in attr:
                self.links.append(attr[key])


errors = []
pages = list(ROOT.rglob("*.html"))
for page in pages:
    parser = Links()
    parser.feed(page.read_text())
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path:
            continue
        path = unquote(url.path)
        if BASE and path.startswith(BASE + "/"):
            path = path[len(BASE) :]
        target = ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
        if not any(
            p.is_file()
            for p in [target, target / "index.html", target.with_suffix(".html")]
        ):
            errors.append(f"{page.relative_to(ROOT)}: {link}")
assert (ROOT / "index.html").is_file(), "No exported homepage"
assert not errors, "Broken static links:\n" + "\n".join(errors[:30])
print(
    f"Checked {len(pages)} HTML documents: all local image, script, stylesheet and page links resolve."
)
