from pathlib import Path
from typing import Optional


def scores(tablet_name: str, highlight_year: Optional[int] = None, quantity=5) -> str:
    path = f"../../results/{tablet_name}"
    lines = Path(path).read_text().splitlines()
    header = lines[2]
    scores = lines[3:]
    top_scores = scores[0:quantity]
    output = [header]
    output.extend(top_scores)

    if highlight_year is not None:
        remaining_scores = scores[quantity:]
        start_list = tuple(map(lambda y: f"{y} ", [highlight_year, highlight_year - 1, highlight_year + 1]))
        highlights = [score for score in remaining_scores if score.startswith(start_list)]
        output.append("...")
        output.extend(highlights)

    return "\n".join(output)
