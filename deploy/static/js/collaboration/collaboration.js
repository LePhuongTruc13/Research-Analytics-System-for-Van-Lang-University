/**
 * ============================================================
 * COLLABORATION CONTROLLER
 * ============================================================
 *
 * Chức năng:
 * ------------------------------------------------------------
 * - Điều phối toàn bộ Collaboration Network.
 * - Kết nối:
 *
 *      collaboration_graph.js
 *      collaboration_filter_year.js
 *      collaboration_filter_topic.js
 *
 * - Load dữ liệu backend.
 * - Quản lý filter.
 * - Update graph.
 *
 * ============================================================
 */
import CollaborationGraph 
from "./collaboration_graph.js";


import CollaborationFilterYear 
from "./collaboration_filter_year.js";


import CollaborationFilterTopic 
from "./collaboration_filter_topic.js";

class Collaboration {


    // ========================================================
    // CONSTRUCTOR
    // ========================================================


    constructor(config = {}) {


        // ----------------------------------------------------
        // CONFIG
        // ----------------------------------------------------

        this.api = {

            years:
                config.apiYears ??
                "/collaboration/api/collaboration/years",


            topics:
                config.apiTopics ??
                "/collaboration/api/collaboration/topics",


            graph:
                config.apiGraph ??
                "/collaboration/api/collaboration/graph"

        };



        // ----------------------------------------------------
        // STATE
        // ----------------------------------------------------

        this.state = {

            year: null,

            topic_id: null

        };



        // ----------------------------------------------------
        // COMPONENTS
        // ----------------------------------------------------

        this.graph = null;

        this.yearFilter = null;

        this.topicFilter = null;



        // ----------------------------------------------------
        // INIT
        // ----------------------------------------------------

        this.initialize();

    }





    // ========================================================
    // INITIALIZE
    // ========================================================


    initialize() {


        this.initializeGraph();


        this.initializeFilters();


        this.bindEvents();


        this.loadInitialData();


    }





    // ========================================================
    // INIT GRAPH
    // ========================================================


    initializeGraph() {


        this.graph =new CollaborationGraph();


        this.graph.enableDoubleClickReset();


    }

    // ========================================================
    // INIT FILTER
    // ========================================================


    initializeFilters() {


        this.yearFilter =
            new CollaborationFilterYear();



        this.topicFilter =
            new CollaborationFilterTopic();


    }





    // ========================================================
    // EVENTS
    // ========================================================


    bindEvents() {



        document.addEventListener(

            "collaborationYearChanged",

            (event)=>{


                this.state.year =
                    event.detail.year;


                this.reloadGraph();


            }

        );




        document.addEventListener(

            "collaborationTopicChanged",

            (event)=>{


                this.state.topic_id =
                    event.detail.topic_id;


                this.reloadGraph();


            }

        );


    }





    // ========================================================
    // LOAD INITIAL DATA
    // ========================================================


    async loadInitialData() {


        try {


            await Promise.all([


                this.loadYears(),


                this.loadTopics()


            ]);

        // ------------------------------------------------
        // SET DEFAULT: năm mới nhất
        // ------------------------------------------------

            if (this.yearsList && this.yearsList.length > 0) {

                const latestYear = Math.max(...this.yearsList);

                this.state.year = latestYear;

                this.yearFilter.selectYear(latestYear, latestYear);

            } else {

                await this.reloadGraph();

            }

        }
        catch(error){


            console.error(

                "Initialize collaboration failed",

                error

            );


        }


    }





    // ========================================================
    // LOAD YEARS
    // ========================================================


    async loadYears() {

        const response = await fetch(this.api.years);

        if(!response.ok){
            throw new Error("Cannot load years");
        }

        const data = await response.json();

        this.yearsList = data.years ?? data;   

        this.yearFilter.loadYears(
            this.yearsList
        );

    }

    // ========================================================
    // LOAD TOPICS
    // ========================================================

    async loadTopics() {


        const response =
            await fetch(
                this.api.topics
            );



        if(!response.ok){


            throw new Error(
                "Cannot load topics"
            );


        }



        const data =
            await response.json();




        this.topicFilter.loadTopics(

            data.topics ?? data

        );


    }





    // ========================================================
    // LOAD GRAPH
    // ========================================================


    async reloadGraph() {



        this.showLoading();



        try {



            const params =
                new URLSearchParams();



            if(this.state.year){


                params.append(

                    "year",

                    this.state.year

                );

            }




            if(this.state.topic_id){


                params.append(

                    "topic_id",

                    this.state.topic_id

                );

            }




            const url =

                this.api.graph

                +

                "?"

                +

                params.toString();






            const response =
                await fetch(url);




            if(!response.ok){


                throw new Error(

                    "Cannot load graph"

                );


            }





            const graphData =
                await response.json();





            this.graph.updateGraph(

                graphData

            );




        }

        catch(error){



            console.error(

                "Graph loading error",

                error

            );



            this.showError(

                error.message

            );


        }

        finally{


            this.hideLoading();


        }



    }





    // ========================================================
    // LOADING UI
    // ========================================================


    showLoading(){


        const el =
            document.querySelector(
                ".graph-loading"
            );


        if(el){

            el.style.display =
                "flex";

        }


    }



    hideLoading(){


        const el =
            document.querySelector(
                ".graph-loading"
            );


        if(el){

            el.style.display =
                "none";

        }


    }





    // ========================================================
    // ERROR UI
    // ========================================================


    showError(message){



        const el =
            document.querySelector(
                ".graph-error"
            );



        if(el){


            el.textContent =
                message;


            el.style.display =
                "block";


        }



    }





    // ========================================================
    // PUBLIC METHODS
    // ========================================================



    setYear(year){


        this.yearFilter.selectYear(

            year,

            year ?? "Tất cả năm"

        );


    }





    setTopic(topicId,label){


        this.topicFilter.selectTopic(

            topicId,

            label ?? "Tất cả chủ đề"

        );


    }





    reset(){


        this.state.year =
            null;


        this.state.topic_id =
            null;



        this.yearFilter.selectYear(

            null,

            "Tất cả năm"

        );


        this.topicFilter.selectTopic(

            null,

            "Tất cả chủ đề"

        );



        this.graph.resetZoom();



    }





    destroy(){


        if(this.graph){

            this.graph.destroy();

        }


    }



}





// ============================================================
// GLOBAL INSTANCE
// ============================================================


document.addEventListener(

"DOMContentLoaded",

()=>{


    window.collaboration =
        new Collaboration({

            apiYears:
                "/collaboration/api/collaboration/years",

            apiTopics:
                "/collaboration/api/collaboration/topics",

            apiGraph:
                "/collaboration/api/collaboration/graph"

        });



}

);