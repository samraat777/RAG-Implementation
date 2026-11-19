
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone

DOCS_DIR = "docs"

ARTICLES = {
    "apple.txt": ("Apple Inc.", "https://en.wikipedia.org/wiki/Apple_Inc."),
    "google.txt": ("Google", "https://en.wikipedia.org/wiki/Google"),
    "microsoft.txt": ("Microsoft", "https://en.wikipedia.org/wiki/Microsoft"),
    "tesla.txt": ("Tesla, Inc.", "https://en.wikipedia.org/wiki/Tesla,_Inc."),
    "nvidia.txt": ("Nvidia", "https://en.wikipedia.org/wiki/Nvidia"),
}

os.makedirs(DOCS_DIR, exist_ok=True)

for filename, (title, source_url) in ARTICLES.items():
    print(f"Downloading: {title}...")

    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": 1,
        "exsectionformat": "plain",
        "redirects": 1,
        "titles": title,
    })

    url = f"https://en.wikipedia.org/w/api.php?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "RAGDocumentCollector/1.0 (educational project)"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        pages = data["query"]["pages"]
        page = next(iter(pages.values()))

        content = page.get("extract", "")

        if not content.strip():
            print(f"Warning: No content found for {title}")
            continue

        output_path = os.path.join(DOCS_DIR, filename)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(f"TITLE: {page['title']}\n")
            file.write(f"SOURCE: {source_url}\n")
            file.write(
                f"RETRIEVED: {datetime.now(timezone.utc).isoformat()}\n"
            )
            file.write("=" * 80 + "\n\n")
            file.write(content)

        print(f"Saved: {output_path} ({len(content)} characters)")

    except Exception as error:
        print(f"Failed to download {title}: {error}")

print("\nWikipedia document collection completed!")
