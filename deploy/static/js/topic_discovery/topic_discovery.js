// ==========================================================
// Topic Discovery
// ==========================================================

document.addEventListener(

    "DOMContentLoaded",

    initializeTopicDiscovery

);


// ==========================================================
// Initialize
// ==========================================================

async function initializeTopicDiscovery() {

    try {

        const response = await fetch(

            "/topic_discovery/api/topic_discovery"

        );

        if (!response.ok) {

            throw new Error(

                "Cannot load Topic Discovery."

            );

        }

        const data = await response.json();

        //--------------------------------------------------
        // Sidebar
        //--------------------------------------------------

        renderTopicList(

            data.topics

        );

        //--------------------------------------------------
        // Search
        //--------------------------------------------------

        initializeTopicSearch();

        //--------------------------------------------------
        // Load default topic
        //--------------------------------------------------

        if (

            data.topics &&
            data.topics.length > 0

        ) {

            await loadTopic(

                data.topics[0].topic_id,

                data.topics[0].topic_name

            );

        }

    }

    catch (error) {

        console.error(error);

    }

}


// ==========================================================
// Load Topic
// ==========================================================

async function loadTopic(

    topicId,

    topicName

) {

    try {

        const response = await fetch(

            `/topic_discovery/api/topic_discovery?topic_id=${topicId}`

        );

        if (!response.ok) {

            throw new Error(

                "Cannot load topic."

            );

        }

        const data = await response.json();

        //--------------------------------------------------
        // Summary
        //--------------------------------------------------

        renderTopicSummary(

            data.summary

        );

        //--------------------------------------------------
        // Publication Trend
        //--------------------------------------------------

        renderPublicationTrend(

            data.publication_trend

        );

        //--------------------------------------------------
        // Authors
        //--------------------------------------------------

        renderTopAuthors(

            data.top_authors,

            topicName

        );

        //--------------------------------------------------
        // Keywords
        //--------------------------------------------------

        renderTopicKeywords(

            data.keywords

        );

    }

    catch (error) {

        console.error(error);

    }

}


// ==========================================================
// Search Topic
// ==========================================================

async function searchTopic(

    keyword

) {

    try {

        const response = await fetch(

            `/topic_discovery/api/topic_discovery?keyword=${encodeURIComponent(keyword)}`

        );

        if (!response.ok) {

            throw new Error(

                "Cannot search."

            );

        }

        const data = await response.json();

        renderTopicList(

            data.topics

        );

    }

    catch (error) {

        console.error(error);

    }

}