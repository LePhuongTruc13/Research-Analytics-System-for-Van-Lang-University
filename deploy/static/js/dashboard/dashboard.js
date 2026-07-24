// ==========================================================
// Dashboard Main
// ==========================================================

document.addEventListener(

    "DOMContentLoaded",

    initializeDashboard

);


// ==========================================================
// Initialize Dashboard
// ==========================================================

async function initializeDashboard() {

    try {

        const response = await fetch(

            "/api/dashboard"

        );

        if (!response.ok) {

            throw new Error(

                "Failed to load dashboard data."

            );

        }

        const data = await response.json();

        // --------------------------------------------------
        // Summary Cards
        // --------------------------------------------------

        renderSummaryCards(

            data.cards

        );

        // --------------------------------------------------
        // Charts
        // --------------------------------------------------

        renderCharts(

            data.charts

        );

        // --------------------------------------------------
        // Recent Publications
        // --------------------------------------------------

        renderRecentPublications(

            data.recent_publications

        );

        // --------------------------------------------------
        // Dashboard Events
        // --------------------------------------------------

        initializeDashboardEvents();

    }

    catch (error) {

        console.error(

            "Dashboard Error:",

            error

        );

    }

}