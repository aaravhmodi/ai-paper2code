"""
arxiv_scraper.py
Fetches metadata from the arXiv API and stores it as JSON for use in your RAG pipeline.
"""

import requests, feedparser, json, os
from tqdm import tqdm

# --- CONFIG ---
SEARCH_TERMS = ["transformer", "diffusion model", "graph neural network", "language model"]
MAX_RESULTS = 20        # per query
OUTPUT_FILE = "data/metadata/arxiv.json"

# --- HELPER FUNCTION ---
def fetch_arxiv_results(query, start=0, max_results=10):
    """
    Calls the arXiv API and returns parsed results as a feedparser object.
    """
    url = (
        f"http://export.arxiv.org/api/query?"
        f"search_query=all:{query}&start={start}&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    response = requests.get(url)
    feed = feedparser.parse(response.text)
    return feed.entries

# --- MAIN SCRIPT ---
def main():
    os.makedirs("data/metadata", exist_ok=True)
    all_papers = []

    for term in SEARCH_TERMS:
        print(f"\n🔍 Fetching papers for query: {term}")
        entries = fetch_arxiv_results(term, max_results=MAX_RESULTS)

        for entry in tqdm(entries):
            paper = {
                "title": entry.title,
                "authors": [a.name for a in entry.authors],
                "summary": entry.summary.strip(),
                "published": entry.published,
                "updated": entry.updated,
                "id": entry.id,
                "pdf_url": next((l.href for l in entry.links if l.rel == "related" and "pdf" in l.type), None),
                "categories": [t["term"] for t in entry.tags] if "tags" in entry else [],
                "primary_category": entry.arxiv_primary_category["term"]
                    if "arxiv_primary_category" in entry else None,
            }
            all_papers.append(paper)

    # Save metadata
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_papers, f, indent=2)

    print(f"\n✅ Saved {len(all_papers)} papers to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
