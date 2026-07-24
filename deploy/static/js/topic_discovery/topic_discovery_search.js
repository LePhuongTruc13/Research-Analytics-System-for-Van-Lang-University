// ==========================================================
// Topic Discovery Search
// ==========================================================

let currentTopicId = null;

let allTopics = [];


// ==========================================================
// Render Topic List
// ==========================================================

function renderTopicList(topics) {

    allTopics = topics;

    const container =
        document.getElementById(
            "topic_list"
        );

    container.innerHTML = "";

    topics.forEach((topic, index) => {

        const tag =
            document.createElement("span");

        tag.className = "tag";

        //--------------------------------------------------
        // Default Active
        //--------------------------------------------------

        if (

            currentTopicId === null &&
            index === 0

        ) {

            currentTopicId =
                topic.topic_id;

        }

        if (

            topic.topic_id === currentTopicId

        ) {

            tag.classList.add(
                "active"
            );

        }

        //--------------------------------------------------
        // Text
        //--------------------------------------------------

        tag.textContent =
            topic.topic_name;

        //--------------------------------------------------
        // Dataset
        //--------------------------------------------------

        tag.dataset.topicId =
            topic.topic_id;

        //--------------------------------------------------
        // Click
        //--------------------------------------------------

        tag.onclick = () => {

            selectTopic(

                topic.topic_id,

                topic.topic_name

            );

        };

        container.appendChild(tag);

    });

}


// ==========================================================
// Initialize Search
// ==========================================================

function initializeTopicSearch() {

    const input =

        document.getElementById(

            "topic_search"

        );

    if (!input) return;

    input.addEventListener(

        "input",

        function () {

            const keyword =

                this.value

                    .trim()

                    .toLowerCase();

            //--------------------------------------------------
            // Empty
            //--------------------------------------------------

            if (

                keyword === ""

            ) {

                renderTopicList(

                    allTopics

                );

                return;

            }

            //--------------------------------------------------
            // Filter
            //--------------------------------------------------

            const filtered =

                allTopics.filter(

                    topic =>

                        topic.topic_name

                        .toLowerCase()

                        .includes(

                            keyword

                        )

                );

            renderTopicList(

                filtered

            );

        }

    );

}


// ==========================================================
// Select Topic
// ==========================================================

function selectTopic(

    topicId,

    topicName

) {

    currentTopicId =
        topicId;

    //--------------------------------------------------
    // Remove Active
    //--------------------------------------------------

    document

        .querySelectorAll(

            ".tag"

        )

        .forEach(tag =>

            tag.classList.remove(

                "active"

            )

        );

    //--------------------------------------------------
    // Active Current
    //--------------------------------------------------

    const selected =

        document.querySelector(

            `[data-topic-id="${topicId}"]`

        );

    if (

        selected

    ) {

        selected.classList.add(

            "active"

        );

    }

    //--------------------------------------------------
    // Load Topic
    //--------------------------------------------------

    loadTopic(

        topicId,

        topicName

    );

}