// ==========================================================
// Dashboard Recent Publications
// ==========================================================

function renderRecentPublications(data) {

    const container =
        document.getElementById(
            "recent_publications"
        );


    if (!container) return;


    container.innerHTML = "";


    if (!data || data.length === 0) return;



    // Sort mới nhất trước và chỉ lấy 5 bài
    const recentPapers = data
        .sort((a, b) =>
            b.publication_year - a.publication_year
        )
        .slice(0, 5);



    const html = recentPapers.map(paper => {


        const openAccess =

            paper.is_open_access
                ? "🟢 Open Access"
                : "🔒 Closed";



        return `

        <div class="pub-item">


            <div class="pub-info">


                <h4>

                    ${paper.title}

                </h4>


                <p>

                    Citations:
                    ${paper.cited_by_count.toLocaleString()}


                    &nbsp;&nbsp;|&nbsp;&nbsp;


                    ${openAccess}

                </p>


            </div>



            <span class="pub-year">

                ${paper.publication_year}

            </span>


        </div>

        `;


    }).join("");



    container.innerHTML = html;


}