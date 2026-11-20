from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for attr in ("href", "src"):
            value = attrs.get(attr)
            if value:
                self.references.append(value)

def inspect(page):
    parser = PageParser()
    parser.feed(page.read_text(encoding="utf-8"))
    errors = []
    for reference in parser.references:
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc:
            continue
        target_path = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page.resolve()
        try:
            target_path.relative_to(ROOT)
        except ValueError:
            errors.append(f"{page.relative_to(ROOT)}: link escapes repository: {reference}")
            continue
        if not target_path.exists() or not target_path.is_file():
            errors.append(f"{page.relative_to(ROOT)}: missing local target: {reference}")
            continue
        if parsed.fragment and target_path.suffix.lower() in {".html", ".htm"}:
            target_parser = PageParser()
            target_parser.feed(target_path.read_text(encoding="utf-8"))
            if parsed.fragment not in target_parser.ids:
                errors.append(f"{page.relative_to(ROOT)}: missing anchor: {reference}")
    return errors

pages = [ROOT / "index.html", ROOT / "projects" / "academic-projects.html"]
pages.extend(sorted((ROOT / "projects").glob("*/index.html")))
all_errors = []
for page in pages:
    if not page.exists():
        all_errors.append(f"Missing page: {page}")
    else:
        all_errors.extend(inspect(page))

if all_errors:
    print("\n".join(all_errors), file=sys.stderr)
    raise SystemExit(1)

print(f"Portfolio link check passed for {len(pages)} HTML pages.")
