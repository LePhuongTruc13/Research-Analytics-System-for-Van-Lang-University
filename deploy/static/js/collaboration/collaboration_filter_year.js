class CollaborationFilterYear {

    constructor() {

        // ====================================================
        // DROPDOWN ELEMENTS
        // ====================================================

        this.dropdown = document.getElementById(
            "dropdown-year"
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
        // CURRENT YEAR
        // ====================================================

        this.selectedYear = null;

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
    // LOAD YEAR LIST
    // ========================================================

    loadYears(yearList) {

        this.menu.innerHTML = "";

        //-----------------------------------------------------
        // OPTION: ALL
        //-----------------------------------------------------

        const allItem = document.createElement("div");

        allItem.className =
            "dropdown-item active";

        allItem.dataset.value = "all";

        allItem.textContent = "Tất cả năm";

        allItem.addEventListener(
            "click",
            () => {

                this.selectYear(
                    null,
                    "Tất cả năm"
                );

            }
        );

        this.menu.appendChild(
            allItem
        );

        //-----------------------------------------------------
        // YEAR ITEMS
        //-----------------------------------------------------

        yearList.forEach((year) => {

            const item =
                document.createElement("div");

            item.className =
                "dropdown-item";

            item.dataset.value = year;

            item.textContent = year;

            item.addEventListener(
                "click",
                () => {

                    this.selectYear(
                        year,
                        year
                    );

                }
            );

            this.menu.appendChild(
                item
            );

        });

    }

    // ========================================================
    // SELECT YEAR
    // ========================================================

    selectYear(
        year,
        label
    ) {

        this.selectedYear = year;

        this.selectedText.textContent = label;

        //-----------------------------------------------------
        // UPDATE ACTIVE ITEM
        //-----------------------------------------------------

        this.menu
            .querySelectorAll(".dropdown-item")
            .forEach((item) => {

                item.classList.remove(
                    "active"
                );

                if (
                    String(item.dataset.value)
                    ===
                    String(
                        year ?? "all"
                    )
                ) {

                    item.classList.add(
                        "active"
                    );

                }

            });

        //-----------------------------------------------------
        // CLOSE MENU
        //-----------------------------------------------------

        this.dropdown.classList.remove(
            "open"
        );

        //-----------------------------------------------------
        // EMIT EVENT
        //-----------------------------------------------------

        document.dispatchEvent(

            new CustomEvent(

                "collaborationYearChanged",

                {

                    detail: {

                        year: this.selectedYear

                    }

                }

            )

        );

    }

    // ========================================================
    // GET CURRENT YEAR
    // ========================================================

    getSelectedYear() {

        return this.selectedYear;

    }

}
export default CollaborationFilterYear;