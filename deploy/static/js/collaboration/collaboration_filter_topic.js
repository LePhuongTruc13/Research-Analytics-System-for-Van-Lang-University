/**
 * ============================================================
 * COLLABORATION FILTER TOPIC
 * ============================================================
 * Chức năng:
 *  - Quản lý dropdown chọn chủ đề.
 *  - Lưu topic_id đang được chọn.
 *  - Không gọi API.
 *  - Không build graph.
 *  - collaboration.js sẽ sử dụng giá trị này để điều phối.
 * ============================================================
 */

class CollaborationFilterTopic {

    constructor() {

        // ====================================================
        // DROPDOWN ELEMENTS
        // ====================================================

        this.dropdown = document.getElementById(
            "dropdown-topic"
        );

        this.selected = this.dropdown.querySelector(
            ".dropdown-selected"
        );

        this.selectedText = this.selected.querySelector(
            "span"
        );

        this.menu = this.dropdown.querySelector(
            ".dropdown-menu"
        );

        // ====================================================
        // CURRENT TOPIC
        // ====================================================

        this.selectedTopic = null;

        // ====================================================
        // INITIALIZE
        // ====================================================

        this.initialize();

    }

    // ========================================================
    // INITIALIZE
    // ========================================================

    initialize() {

        this.bindDropdown();

        this.bindOutsideClick();

    }

    // ========================================================
    // OPEN / CLOSE DROPDOWN
    // ========================================================

    bindDropdown() {

        this.selected.addEventListener(
            "click",
            (event) => {

                event.stopPropagation();

                this.dropdown.classList.toggle(
                    "open"
                );

            }
        );

    }

    // ========================================================
    // CLOSE WHEN CLICK OUTSIDE
    // ========================================================

    bindOutsideClick() {

        document.addEventListener(
            "click",
            () => {

                this.dropdown.classList.remove(
                    "open"
                );

            }
        );

    }

    // ========================================================
    // LOAD TOPIC LIST
    // ========================================================
    
    loadTopics(topicList) {

        this.menu.innerHTML = "";

        // ----------------------------------------------------
        // OPTION: ALL TOPICS
        // ----------------------------------------------------

        const allItem = document.createElement(
            "div"
        );

        allItem.className =
            "dropdown-item active";

        allItem.dataset.value = "all";

        allItem.textContent =
            "Tất cả chủ đề";

        allItem.addEventListener(
            "click",
            () => {

                this.selectTopic(
                    null,
                    "Tất cả chủ đề"
                );

            }
        );

        this.menu.appendChild(
            allItem
        );

        // ----------------------------------------------------
        // LOAD TOPICS
        // ----------------------------------------------------

        topicList.forEach(
            (topic) => {

                const item =
                    document.createElement(
                        "div"
                    );

                item.className =
                    "dropdown-item";

                item.dataset.value =
                    topic.topic_id;

                item.textContent =
                    topic.topic_name;

                item.addEventListener(
                    "click",
                    () => {

                        this.selectTopic(

                            topic.topic_id,

                            topic.topic_name

                        );

                    }
                );

                this.menu.appendChild(
                    item
                );

            }
        );

    }

    // ========================================================
    // SELECT TOPIC
    // ========================================================

    selectTopic(
        topicId,
        label
    ) {

        this.selectedTopic = topicId;

        this.selectedText.textContent =
            label;

        // ----------------------------------------------------
        // UPDATE ACTIVE ITEM
        // ----------------------------------------------------

        this.menu
            .querySelectorAll(
                ".dropdown-item"
            )
            .forEach(
                (item) => {

                    item.classList.remove(
                        "active"
                    );

                    if (

                        String(
                            item.dataset.value
                        )

                        ===

                        String(
                            topicId ?? "all"
                        )

                    ) {

                        item.classList.add(
                            "active"
                        );

                    }

                }
            );

        // ----------------------------------------------------
        // CLOSE MENU
        // ----------------------------------------------------

        this.dropdown.classList.remove(
            "open"
        );

        // ----------------------------------------------------
        // EMIT EVENT
        // ----------------------------------------------------

        document.dispatchEvent(

            new CustomEvent(

                "collaborationTopicChanged",

                {

                    detail: {

                        topic_id:
                            this.selectedTopic

                    }

                }

            )

        );

    }

    // ========================================================
    // GET CURRENT TOPIC
    // ========================================================

    getSelectedTopic() {

        return this.selectedTopic;

    }

}
export default CollaborationFilterTopic;