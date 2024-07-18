const md_button = document.getElementById("md_button");
const phd_button = document.getElementById("phd_button");
const md_info = document.getElementsByClassName('md_info');
const phd_info = document.getElementsByClassName('phd_info');


for (let i = 0; i < phd_info.length; i++){
    phd_info[i].classList.add("d-none");
}

function resizeAllGraphs() {
    var containers = document.querySelectorAll('.md_info, .phd_info');
    containers.forEach(function(container) {
        Plotly.Plots.resize(container);
    });
}

function switchToMd() {
    md_button.classList.remove("btn-outline-primary");
    md_button.classList.add("btn-primary");
    phd_button.classList.add("btn-outline-primary");
    phd_button.classList.remove("btn-primary");

    for (let i = 0; i < md_info.length; i++){
        md_info[i].classList.remove("d-none");
    }

    for (let i = 0; i < phd_info.length; i++){
        phd_info[i].classList.add("d-none");
    }

    Plotly.Plots.resize("reg_status")
    Plotly.Plots.resize("reg_status_prev")
    Plotly.Plots.resize("reg_interviews_graph")
    Plotly.Plots.resize("reg_acceptance_graph")
}

function switchToPhd() {
    phd_button.classList.remove("btn-outline-primary");
    phd_button.classList.add("btn-primary");
    md_button.classList.add("btn-outline-primary");
    md_button.classList.remove("btn-primary");

    for (let i = 0; i < phd_info.length; i++){
        phd_info[i].classList.remove("d-none");
    }

    for (let i = 0; i < md_info.length; i++){
        md_info[i].classList.add("d-none");
    }

    if (document.getElementById("phd_status")) {
        Plotly.Plots.resize("phd_status");
    }
    if (document.getElementById("phd_status_prev")) {
        Plotly.Plots.resize("phd_status_prev");
    }
    if (document.getElementById("phd_interviews_graph")) {
        Plotly.Plots.resize("phd_interviews_graph");
    }
    if (document.getElementById("phd_acceptance_graph")) {
        Plotly.Plots.resize("phd_acceptance_graph");
    }
    if (document.getElementById("phd_map")) {
        Plotly.Plots.resize("phd_map");
    }
    if (document.getElementById("phd_mcat_gpa")) {
        Plotly.Plots.resize("phd_mcat_gpa");
    }
}