const MAX_VISIBLE_AUTHORS = 12;

let authors = [];
let filteredAuthors = [];
let selectedAuthorId = null;

// =====================================================
// Initialize
// =====================================================

function initAuthorFilter(authorData){

    authors = [...authorData];

    filteredAuthors = [...authors];

    renderAuthorList(filteredAuthors);

    initSearch();
}

// =====================================================
// Search
// =====================================================

function initSearch(){

    const input = document.getElementById("author-search");

    input.addEventListener("input", function(){

        const keyword = this.value
            .trim()
            .toLowerCase();

        if(keyword === ""){

            filteredAuthors = [...authors];

        }else{

            filteredAuthors = authors.filter(author =>

                author.author_name
                    .toLowerCase()
                    .includes(keyword)

            );

        }

        renderAuthorList(filteredAuthors);

    });

}

// =====================================================
// Render
// =====================================================

function renderAuthorList(authorList){

    const container = document.getElementById("author-list");

    container.innerHTML = "";

    authorList
        .slice(0, MAX_VISIBLE_AUTHORS)
        .forEach(author=>{

            const div = document.createElement("div");

            div.className = "author-item";

            if(author.author_id === selectedAuthorId){

                div.classList.add("active");

            }

            div.dataset.authorId = author.author_id;

            div.innerHTML =

                `<div class="author-name">

                    ${author.author_name}

                </div>`;

            div.addEventListener(

                "click",

                ()=>selectAuthor(author)

            );

            container.appendChild(div);

        });

}

// =====================================================
// Select
// =====================================================

function selectAuthor(author){

    selectedAuthorId = author.author_id;

    renderAuthorList(filteredAuthors);

    document.dispatchEvent(

        new CustomEvent(

            "authorSelected",

            {

                detail:{

                    author_id:author.author_id,

                    author_name:author.author_name

                }

            }

        )

    );

}

// =====================================================
// External API
// =====================================================

window.AuthorFilter = {

    init:initAuthorFilter,

    getSelectedAuthor(){

        return selectedAuthorId;

    },
    
    selectRandom(author){
        selectAuthor(author);
    }

};