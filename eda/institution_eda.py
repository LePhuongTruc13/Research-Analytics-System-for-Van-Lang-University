import matplotlib.pyplot as plt

from eda.load_data import (
    load_institutions,
    load_author_institution,
)

plt.style.use("ggplot")
plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 11,
    "axes.titlesize": 16,
    "axes.labelsize": 12,
})


def total_institutions(institutions):
    """
    Print total number of institutions.
    """

    print("=" * 50)
    print(f"Total institutions: {len(institutions):,}")


def country_distribution(institutions):
    """
    Plot institution distribution by country.
    """

    country = (
        institutions["country_code"]
        .fillna("Unknown")
        .value_counts()
        .head(15)
    )

    plt.figure(figsize=(10, 5))

    country.plot(kind="bar")

    plt.title("Top Countries by Number of Institutions")
    plt.xlabel("Country")
    plt.ylabel("Number of Institutions")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def authors_per_institution(author_institution):
    """
    Plot authors per institution.
    """

    counts = (
        author_institution
        .groupby("institution_id")
        .size()
    )

    print("\nAuthors per Institution Statistics")
    print(counts.describe())

    print(f"\nAverage authors per institution: {counts.mean():.2f}")

    plt.figure(figsize=(9, 5))

    plt.hist(
        counts,
        bins=20,
        edgecolor="black",
        alpha=0.8
    )

    plt.title("Authors per Institution")
    plt.xlabel("Number of Authors")
    plt.ylabel("Number of Institutions")

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()


def top_institutions_by_authors(
    institutions,
    author_institution,
    top_n=10
):
    """
    Print top institutions by number of authors.
    """

    top = (
        author_institution
        .groupby("institution_id")
        .size()
        .reset_index(name="author_count")
        .merge(
            institutions[
                [
                    "institution_id",
                    "institution_name",
                    "country_code"
                ]
            ],
            on="institution_id",
            how="left"
        )
        .sort_values(
            "author_count",
            ascending=False
        )
        .head(top_n)
    )

    print("\nTop Institutions by Number of Authors")
    print(
        top[
            [
                "institution_name",
                "country_code",
                "author_count"
            ]
        ].to_string(index=False)
    )

    plt.figure(figsize=(10, 5))

    plt.bar(
        top["institution_name"],
        top["author_count"]
    )

    plt.title("Top Institutions by Number of Authors")
    plt.xlabel("Institution")
    plt.ylabel("Number of Authors")

    plt.xticks(rotation=60, ha="right")

    plt.tight_layout()
    plt.show()


def top_countries(institutions):
    """
    Print top countries by number of institutions.
    """

    top = (
        institutions["country_code"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    top.columns = [
        "country_code",
        "institution_count"
    ]

    print("\nTop Countries")
    print(top.head(10).to_string(index=False))


def main():

    institutions = load_institutions()

    author_institution = load_author_institution()

    total_institutions(institutions)

    country_distribution(institutions)

    authors_per_institution(author_institution)

    top_institutions_by_authors(
        institutions,
        author_institution
    )

    top_countries(institutions)


if __name__ == "__main__":
    main()