import matplotlib.pyplot as plt

from eda.load_data import load_papers

# Style 
plt.style.use("ggplot")
plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 11,
    "axes.titlesize": 16,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})


def total_papers(df):
    """
    Print total number of papers.
    """

    print("=" * 50)
    print(f"Total papers: {len(df):,}")


def publication_by_year(df):
    """
    Plot publication count by year.
    """

    publication = (
        df["publication_year"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(11, 5))

    plt.plot(
        publication.index,
        publication.values,
        marker="o",
        markersize=6,
        linewidth=2.5,
        color="#1f77b4"
    )

    plt.title("Publications by Year", weight="bold")
    plt.xlabel("Publication Year")
    plt.ylabel("Number of Papers")

    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


def citation_distribution(df):
    """
    Plot citation distribution.
    """

    plt.figure(figsize=(9, 5))

    plt.hist(
        df["cited_by_count"],
        bins=30,
        color="#4C72B0",
        edgecolor="black",
        alpha=0.8
    )

    plt.title("Citation Distribution", weight="bold")
    plt.xlabel("Citation Count")
    plt.ylabel("Number of Papers")

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()


def open_access_distribution(df):
    """
    Plot Open Access vs Non-Open Access.
    """

    counts = df["is_open_access"].value_counts()

    plt.figure(figsize=(7, 7))

    plt.pie(
        counts,
        labels=["Open Access", "Non Open Access"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#66c2a5", "#fc8d62"],
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 11}
    )

    plt.title("Open Access Distribution", weight="bold")

    plt.tight_layout()
    plt.show()


def abstract_length_distribution(df):
    """
    Plot abstract length distribution.
    """

    abstract_length = (
        df["abstract"]
        .fillna("")
        .str.split()
        .str.len()
    )

    plt.figure(figsize=(9, 5))

    plt.hist(
        abstract_length,
        bins=30,
        color="#55A868",
        edgecolor="black",
        alpha=0.8
    )

    plt.title("Abstract Length Distribution", weight="bold")
    plt.xlabel("Number of Words")
    plt.ylabel("Number of Papers")

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()


def top_cited_papers(df, top_n=10):
    """
    Print top cited papers.
    """

    top = (
        df.sort_values(
            "cited_by_count",
            ascending=False
        )[["paper_id", "title", "cited_by_count"]]
        .head(top_n)
    )

    print("\nTop Cited Papers")
    print(top)


def main():

    papers = load_papers()

    total_papers(papers)

    publication_by_year(papers)

    citation_distribution(papers)

    open_access_distribution(papers)

    abstract_length_distribution(papers)

    top_cited_papers(papers)


if __name__ == "__main__":
    main()