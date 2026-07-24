// ==========================================================
// Dashboard Charts
// ==========================================================

let publicationChart = null;
let citationChart = null;


// ==========================================================
// Render All Charts
// ==========================================================

function renderCharts(charts) {

    renderPublicationChart(
        charts.publication_trend
    );

    renderCitationChart(
        charts.citation_trend
    );

    renderTopTopics(
        charts.top_topics
    );

    renderTopCountries(
        charts.top_collaboration_countries
    );

}


// ==========================================================
// Publication Trend
// ==========================================================

function renderPublicationChart(data) {

    const ctx = document
        .getElementById("publication_chart")
        .getContext("2d");

    if (publicationChart) {

        publicationChart.destroy();

    }

    publicationChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: data.map(
                d => d.publication_year
            ),

            datasets: [

                {

                    label: "Publications",

                    data: data.map(
                        d => d.paper_count
                    ),

                    backgroundColor: "#b91c1c",

                    borderRadius: 6

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,


            plugins: {

                legend: {

                    display: false

                }

            }
        }
    });

}


// ==========================================================
// Citation Trend
// ==========================================================

function renderCitationChart(data) {

    const ctx = document
        .getElementById("citation_chart")
        .getContext("2d");

    if (citationChart) {

        citationChart.destroy();

    }

    citationChart = new Chart(ctx, {

        type: "line",

        data: {

            labels: data.map(
                d => d.publication_year
            ),

            datasets: [

                {

                    label: "Citations",

                    data: data.map(
                        d => d.total_citations
                    ),

                    borderColor: "#2563eb",

                    backgroundColor: "rgba(37,99,235,0.15)",

                    fill: true,

                    tension: 0.35

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            }

        }
        

    });

}


// ==========================================================
// Top Topics
// ==========================================================

function renderTopTopics(data) {

    const container =
        document.getElementById(
            "top_topics_list"
        );


    if (!container) return;


    container.innerHTML = "";


    if (!data || data.length === 0) return;


    // Chỉ lấy Top 5
    const topTopics = data.slice(0, 5);


    const maxValue =
        Math.max(
            ...topTopics.map(item =>
                item.paper_count
            )
        );



    const html = topTopics.map(topic => {


        const width =
            maxValue > 0
                ? (topic.paper_count / maxValue) * 100
                : 0;



        return `

            <div class="topic-item">


                <span class="topic-name">

                    ${topic.topic_name}

                </span>



                <div class="progress-bar-container">


                    <div
                        class="progress-fill"
                        style="width:${width}%">
                    </div>


                </div>



                <span class="topic-count">

                    ${topic.paper_count}

                </span>


            </div>

        `;


    }).join("");



    container.innerHTML = html;

}


// ==========================================================
// Top Collaboration Countries
// ==========================================================

function renderTopCountries(data) {

    const container =
        document.getElementById(
            "country_tags"
        );

    container.innerHTML = "";

    data.forEach(country => {

        container.innerHTML += `

        <div class="country-tag">

            <span class="badge">

                ${country.country_code}

            </span>

            ${country.author_count}

        </div>

        `;

    });

}