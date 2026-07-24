// ==========================================================
// Topic Discovery Chart
// ==========================================================

function renderPublicationTrend(data) {

    if (!data || data.length === 0) {

        return;

    }

    //--------------------------------------------------------
    // Containers
    //--------------------------------------------------------

    const path =
        document.getElementById(
            "publication_path"
        );

    const dots =
        document.getElementById(
            "publication_dots"
        );

    const xAxis =
        document.getElementById(
            "publication_xaxis"
        );

    const yAxis =
        document.getElementById(
            "publication_yaxis"
        );

    const tooltip =
        document.getElementById(
            "publication_tooltip"
        );

    dots.innerHTML = "";
    xAxis.innerHTML = "";
    yAxis.innerHTML = "";

    //--------------------------------------------------------
    // Max Value
    //--------------------------------------------------------

    const maxValue = Math.max(

        ...data.map(

            d => d.paper_count

        )

    );

    //--------------------------------------------------------
    // Nice Max
    //--------------------------------------------------------

    const niceMax =

        Math.ceil(maxValue / 10) * 10;

    //--------------------------------------------------------
    // Y Axis
    //--------------------------------------------------------

    for (let i = 4; i >= 0; i--) {

        const value =

            Math.round(

                niceMax * i / 4

            );

        yAxis.innerHTML +=

            `<span>${value}</span>`;

    }

    //--------------------------------------------------------
    // X Axis
    //--------------------------------------------------------

    data.forEach(item => {

        xAxis.innerHTML +=

            `<span>${item.publication_year}</span>`;

    });

    //--------------------------------------------------------
    // SVG Path
    //--------------------------------------------------------

    let pathString = "";

    data.forEach((item, index) => {

        const x =

            data.length === 1

                ? 50

                : 3 +

                  (

                    index *

                    (94 / (data.length - 1))

                  );

        const y =

            48 -

            (

                item.paper_count /

                niceMax

            ) * 46;

        //----------------------------------------------------
        // Path
        //----------------------------------------------------

        if (index === 0) {

            pathString +=

                `M ${x},${y}`;

        }

        else {

            pathString +=

                ` L ${x},${y}`;

        }

        //----------------------------------------------------
        // Dot
        //----------------------------------------------------

        const dot =

            document.createElement("span");

        dot.className = "dot";

        dot.style.left = `${x}%`;

        dot.style.bottom =

            `${

                (

                    item.paper_count /

                    niceMax

                ) * 96

            }%`;

        //----------------------------------------------------
        // Tooltip
        //----------------------------------------------------

        dot.addEventListener(

            "mouseenter",

            function () {

                tooltip.innerHTML =

                    `
                    <strong>${item.publication_year}</strong>
                    Papers : ${item.paper_count}
                    `;

                tooltip.style.display = "block";

            }

        );

        dot.addEventListener(

            "mousemove",

            function (e) {

                const rect =

                    document

                    .querySelector(".chart-area")

                    .getBoundingClientRect();

                tooltip.style.left =

                    (e.clientX - rect.left + 12) + "px";

                tooltip.style.top =

                    (e.clientY - rect.top - 50) + "px";

            }

        );

        dot.addEventListener(

            "mouseleave",

            function () {

                tooltip.style.display = "none";

            }

        );

        dots.appendChild(dot);

    });

    //--------------------------------------------------------
    // Draw Path
    //--------------------------------------------------------

    path.setAttribute(

        "d",

        pathString

    );

}