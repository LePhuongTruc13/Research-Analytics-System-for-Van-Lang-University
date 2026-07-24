import matplotlib.pyplot as plt

from eda.load_data import load_authors, load_paper_author

plt.style.use("ggplot")
plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 11,
    "axes.titlesize": 16,
    "axes.labelsize": 12,
})


def total_authors(authors):
    """
    Print total number of authors.
    """

    print("=" * 50)
    print(f"Total authors: {len(authors):,}")


def authors_per_paper(paper_author):
    """
    Plot number of authors per paper.
    """

    counts = (
        paper_author
        .groupby("paper_id")
        .size()
    )

    print("\nAuthors per Paper Statistics")
    print(counts.describe())

    print(f"\nAverage authors per paper: {counts.mean():.2f}")

    plt.figure(figsize=(9, 5))

    plt.hist(
        counts,
        bins=20,
        edgecolor="black",
        alpha=0.8
    )

    plt.title("Authors per Paper")
    plt.xlabel("Number of Authors")
    plt.ylabel("Number of Papers")

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()


def top_papers_by_authors(paper_author, top_n=10):
    """
    Print papers with the most authors.
    """

    top = (
        paper_author
        .groupby("paper_id")
        .size()
        .reset_index(name="author_count")
        .sort_values(
            by="author_count",
            ascending=False
        )
        .head(top_n)
    )

    print("\nTop Papers by Number of Authors")
    print(top.to_string(index=False))


def papers_per_author(paper_author):
    """
    Plot number of papers per author.
    """

    counts = (
        paper_author
        .groupby("author_id")
        .size()
    )

    print("\nPapers per Author Statistics")
    print(counts.describe())

    print(f"\nAverage papers per author: {counts.mean():.2f}")

    plt.figure(figsize=(9, 5))

    plt.hist(
        counts,
        bins=20,
        edgecolor="black",
        alpha=0.8
    )

    plt.title("Papers per Author")
    plt.xlabel("Number of Papers")
    plt.ylabel("Number of Authors")

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()


def top_authors_by_papers(authors, paper_author, top_n=10):
    """
    Print authors with the most papers.
    """

    top = (
        paper_author
        .groupby("author_id")
        .size()
        .reset_index(name="paper_count")
        .merge(
            authors[["author_id", "author_name"]],
            on="author_id",
            how="left"
        )
        .sort_values(
            by="paper_count",
            ascending=False
        )
        .head(top_n)
    )

    print("\nTop Authors by Number of Papers")
    print(top[["author_id", "author_name", "paper_count"]].to_string(index=False))


def main():

    authors = load_authors()
    paper_author = load_paper_author()

    total_authors(authors)

    authors_per_paper(paper_author)

    top_papers_by_authors(paper_author)

    papers_per_author(paper_author)

    top_authors_by_papers(authors, paper_author)


if __name__ == "__main__":
    main()