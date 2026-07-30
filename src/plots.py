from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib_venn import venn2, venn3


def plot_venn(
    overlap: Mapping[tuple[int, ...], Collection[Any]],
    labels: Sequence[str] | None = None,
    title: str = "Accession overlap",
) -> Figure:
    """Create a Venn diagram from exclusive overlap regions.

    Each key contains the zero-based indices of the sets represented by that
    region. Each value contains the items exclusive to exactly that region.
    """
    if labels is not None:
        n = len(labels)
    else:
        indices = [index for region in overlap for index in region]

        if not indices:
            raise ValueError(
                "Cannot determine the number of sets from an empty overlap."
            )

        n = max(indices) + 1

    if n not in (2, 3):
        raise ValueError(
            "A standard Venn diagram supports only two or three sets. "
            "Use an UpSet plot for four or more sets."
        )

    if labels is None:
        labels = [f"Set {i + 1}" for i in range(n)]
    elif len(labels) != n:
        raise ValueError("The number of labels must match the number of sets.")

    for region in overlap:
        if not region:
            raise ValueError("Overlap keys cannot be empty tuples.")

        if any(index < 0 or index >= n for index in region):
            raise ValueError(f"Invalid set indices in overlap key: {region}")

    # Examples:
    # (0,)    -> "100"
    # (1, 2)  -> "011"
    # (0, 2)  -> "101"
    subsets = {
        "".join("1" if i in region else "0" for i in range(n)): len(items)
        for region, items in overlap.items()
    }

    fig, ax = plt.subplots(figsize=(8, 8))

    if n == 2:
        venn2(
            subsets=subsets,
            set_labels=tuple(labels),
            ax=ax,
        )
    else:
        venn3(
            subsets=subsets,
            set_labels=tuple(labels),
            ax=ax,
        )

    ax.set_title(title)
    fig.tight_layout()

    return fig