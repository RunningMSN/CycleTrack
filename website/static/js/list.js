var mini_explorer_graphs = document.getElementsByClassName("mini_explorer_graph_area");

function mini_explore(school_id, phd, name, int_name, md_or_do, plot_loc, explorer_url) {
    var title = document.getElementById("mini_explorer_title");
    if (phd == 'True') {
        title_string = int_name + ' (' + md_or_do + '-PhD)';
        fetch(plot_loc + "/status_" + school_id + "_phd_curr.JSON").then(response => response.json())
            .then(data => {
                data.config = {'responsive': true, 'displaylogo': false, 'displayModeBar': false};
                Plotly.newPlot('mini_cycle_status_curr', data);
            })
            .catch(error => console.log(error));
        fetch(plot_loc + "/status_" + school_id + "_phd_prev.JSON").then(response => response.json())
            .then(data => {
                data.config = {'responsive': true, 'displaylogo': false, 'displayModeBar': false};
                Plotly.newPlot('mini_cycle_status_prev', data);
            })
            .catch(error => console.log(error));

    } else {
        title_string = int_name + ' (' + md_or_do + ')';
        fetch(plot_loc + "/status_" + school_id + "_reg_curr.JSON").then(response => response.json())
            .then(data => {
                data.config = {'responsive': true, 'displaylogo': false, 'displayModeBar': false};
                Plotly.newPlot('mini_cycle_status_curr', data);
            })
            .catch(error => console.log(error));
        fetch(plot_loc + "/status_" + school_id + "_reg_prev.JSON").then(response => response.json())
            .then(data => {
                data.config = {'responsive': true, 'displaylogo': false, 'displayModeBar': false};
                Plotly.newPlot('mini_cycle_status_prev', data);
            })
            .catch(error => console.log(error));
    }
    title.innerHTML = title_string;
    var explorerLinkButton = document.getElementById("explorer_link_button");
    explorerLinkButton.href = explorer_url + '/school/' + name;
}

function switchGraph(graph_name) {
    if (graph_name == "curr_cycle") {
        for (let i = 0; i < mini_explorer_graphs.length; i++) {
            if (mini_explorer_graphs[i].classList.contains("curr_cycle_status")) {
                mini_explorer_graphs[i].classList.remove("d-none");
            } else {
                mini_explorer_graphs[i].classList.add("d-none");
            }
        }
    } else if (graph_name == "prev_cycle") {
        for (let i = 0; i < mini_explorer_graphs.length; i++) {
            if (mini_explorer_graphs[i].classList.contains("prev_cycle_status")) {
                mini_explorer_graphs[i].classList.remove("d-none");
            } else {
                mini_explorer_graphs[i].classList.add("d-none");
            }
        }
    }
}