"""
Inspired by:
- https://github.com/yzhangcs/yzhangcs.github.io/blob/main/arxiv-daily.py
- https://github.com/Jacob-Zhou/jacob-zhou.github.io/blob/master/arxiv-daily.py
"""

import re
import json
from datetime import datetime, timedelta, timezone
from typing import Iterable

import arxiv


def load_json(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def dump_json(filepath, data):
    with open(filepath, "w", encoding="utf8") as fout:
        json.dump(data, fout, indent=2, ensure_ascii=False)


def cover_timezones(date: datetime) -> datetime:
    # to UTF+8
    return date.astimezone(timezone(timedelta(hours=8)))


def collect_category(category: str, days: int = 1) -> Iterable[arxiv.Result]:
    """Collect arxiv papers from a category."""
    client = arxiv.Client(num_retries=10, page_size=500)
    query = arxiv.Search(
        query=f"cat:{category}",
        sort_by=arxiv.SortCriterion.LastUpdatedDate,
    )
    results = client.results(query)
    max_iter = 1000
    while True:
        try:
            paper = next(results)
        except StopIteration:
            break
        except arxiv.arxiv.UnexpectedEmptyPageError:
            continue

        max_iter -= 1
        if max_iter <= 0:
            break

        date = datetime.now(paper.updated.tzinfo)
        if paper.updated.date() < date.date() - timedelta(days=days):
            break

        # Convert to UTC+8
        date = cover_timezones(paper.updated).strftime("%b %d %Y %a")
        paper.local_date = date

        yield paper


def span(string: str, span_class: str):
    return f'<span class="{span_class}">{string}</span>'


def replace(pattern: str, string: str, span_class: str):
    obj = re.search(pattern, string, flags=re.I)
    if obj is not None:
        s, e = obj.span()
        string = string[:s] + span(string[s:e], span_class) + string[e:]
    return string


def tan_class(
    papers: Iterable[dict],
    keys: list = None,
    authors: list = None,
    comments: list = None,
    element_class: str = "emph",
):
    keys = keys or []
    authors = authors or []
    comments = comments or []

    new_papers = {}
    for cat, cat_papers in papers.items():
        new_papers[cat] = []
        for paper in cat_papers:
            for i, author in enumerate(paper["authors"]):
                if author in authors:
                    paper["authors"][i] = span(author, element_class)
            for comment in comments:
                paper["comment"] = replace(comment, paper["comment"], element_class)
            key_cands = sorted(keys, key=lambda x: len(x), reverse=True)
            for key in key_cands:
                paper["title"] = replace(key, paper["title"], element_class)
                paper["abstract"] = replace(key, paper["abstract"], element_class)
            new_papers[cat].append(paper)
    return new_papers


if __name__ == "__main__":
    settings = load_json("settings.json")

    # Collect papers
    papers = {}
    for category in settings["categories"]:
        print(f"Collecting {category}...")
        papers[category] = []
        for paper in collect_category(category, days=1):
            papers[category].append(
                {
                    "title": paper.title,
                    "url": paper.entry_id,
                    "pdf_url": paper.pdf_url,
                    "date": paper.local_date,
                    "authors": [author.name for author in paper.authors],
                    "comment": "" if paper.comment is None else paper.comment,
                    "abstract": paper.summary,
                }
            )
            print(
                f"Collected: {category} ({len(papers[category])}) - {paper.local_date} - {paper.title}"
            )

    print("Dumping...")
    dump_json("papers.json", papers)
    nums = {category: len(papers[category]) for category in papers}
    print(f"Total collected: {nums}")
    print("Add class to papers...")
    new_papers = tan_class(
        papers,
        keys=settings.get("keys"),
        authors=settings.get("authors"),
        comments=settings.get("comments"),
        element_class="emph"
    )
    print("Dumping...")
    dump_json("papers_with_style.json", new_papers)
    print("Done!")
