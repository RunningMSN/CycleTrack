const platform_row = document.getElementById("platform_row");
const team_row = document.getElementById("team_row");
const sample_list = document.getElementById("sample_list");
const graph_card = document.getElementById("graph_card");
const hide_btn = document.getElementById("hide_graph_button");
var graph_buttons = document.getElementsByClassName('graph_button');
var graphs = document.getElementsByClassName('graph');
const sample_list_button = document.getElementById("sample_list_button");

function switchToTeam() {
    team_row.classList.remove("d-none");
    platform_row.classList.add("d-none");
    hideGraph();
}

function switchToPlatform() {
    team_row.classList.add("d-none");
    platform_row.classList.remove("d-none");
}

function sampleList() {
    if (sample_list.classList.contains("d-none")) {
        sample_list.classList.remove("d-none");
        sample_list_button.innerText = "Hide Sample List";
    } else {
        sample_list.classList.add("d-none");
        sample_list_button.innerText = "Show Sample List";
    }
}

function displayGraph(graph_type) {
    for (let i = 0; i < graphs.length; i++){
        graphs[i].classList.add("d-none");
    }

    const graph = document.getElementById(graph_type);
    graph.classList.remove("d-none");

    graph_card.classList.remove("d-none");

    hide_btn.classList.remove("d-none");

    for (let i = 0; i < graph_buttons.length; i++){
        graph_buttons[i].classList.add("d-none");
    }
}

function hideGraph() {
    graph_card.classList.add("d-none");

    hide_btn.classList.add("d-none");

    for (let i = 0; i < graph_buttons.length; i++){
        graph_buttons[i].classList.remove("d-none");
    }

    for (let i = 0; i < graphs.length; i++){
        graphs[i].classList.add("d-none");
    }
}