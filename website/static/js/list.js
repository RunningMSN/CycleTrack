function submitCost(costUrl) {
    const form = document.getElementById('submitCostForm');
    // Prevent default form submission
    event.preventDefault();
    // Collect the form data
    const formData = new FormData(form);
    // Submit the form data
    fetch(costUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.text()) // Assuming the server returns a text response
    .then(data => {
        document.getElementById('response').innerText = data; // Display the response
    })
    .catch(error => {
        console.error('Error:', error);
    });
    // Remove message
    var message = document.getElementById('cost_message');
    message.classList.add("d-none");
}

var timer;
const delay = 2000;
function submitNote(schoolId, edit_url) {
    // Clear the previous timer if any
    clearTimeout(timer);

    // Set a new timer
    timer = setTimeout(() => {
        editSchool(schoolId, 'note', edit_url);
    }, delay);
}

function editSchool(schoolId, action, edit_url) {
    var formData = new FormData();
    formData.append('school_id', schoolId);
    formData.append('action', action);
    var data = document.getElementById(action + '_' + schoolId).value;
    formData.append('data', data);

    fetch(edit_url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(responseData => {
        console.log('Success:', responseData);
        var school_entry = document.getElementById(schoolId + "_item");
        if (action != "note") {
            if (data) {
                updateStatus(school_entry, action, schoolId);
            } else {
                revertStatus(school_entry, schoolId);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

var statusHierarchy = [
    "primary",
    "secondary",
    "complete",
    "hold",
    "interview",
    "waitlist",
    "rejection",
    "withdrawn",
    "acceptance"
];

function getCurrentStatus(element) {
    for (let status of statusHierarchy) {
        if (element.classList.contains(`status_${status}`)) {
            return status;
        }
    }
    return null;
}

function updateStatus(element, newStatus, schoolId) {
    const currentStatus = getCurrentStatus(element);
    if (currentStatus === null || statusHierarchy.indexOf(newStatus) > statusHierarchy.indexOf(currentStatus)) {
        if (currentStatus !== null) {
            element.classList.remove(`status_${currentStatus}`);
            document.getElementById(`pipe_${currentStatus}_${schoolId}`).classList.add('d-none');
        }
        element.classList.add(`status_${newStatus}`);
        document.getElementById(`pipe_${newStatus}_${schoolId}`).classList.remove('d-none');
    }
}

function revertStatus(element, schoolId) {
    const currentStatus = getCurrentStatus(element);

    // Remove current status
    if (currentStatus !== null) {
        element.classList.remove(`status_${currentStatus}`);
        document.getElementById(`pipe_${currentStatus}_${schoolId}`).classList.add('d-none');
    }

    // Find last status with data
    let lastStatusWithData = null;
    for (let status of statusHierarchy.slice().reverse()) {
        let input = document.getElementById(`${status}_${schoolId}`);
        if (input && input.value) {
            lastStatusWithData = status;
            break;
        }
    }

    // Update to last status with data
    if (lastStatusWithData !== null) {
        element.classList.add(`status_${lastStatusWithData}`);
        document.getElementById(`pipe_${lastStatusWithData}_${schoolId}`).classList.remove('d-none');
    }
}

var added_schools = [];
function addSchool(school) {
    if (added_schools.includes(school)) {
        var index = added_schools.indexOf(school);
        if (index != -1) {
            added_schools.splice(index, 1)
        }
    } else {
        added_schools.push(school);
    }
    var added_schools_form = document.getElementById("added_schools");
    added_schools_form.value = added_schools;
}

function searchAdd() {
    var schoolListings = document.getElementsByClassName("school_listing");
    var searchbar = document.getElementById("search_schools");
    search = searchbar.value;
    for (let i=0; i < schoolListings.length; i++) {
        if (!schoolListings[i].id.toLowerCase().includes(search.toLowerCase())) {
            schoolListings[i].classList.add("d-none");
        } else {
            schoolListings[i].classList.remove("d-none");
        }
    }

}

function deleteSchool(schoolId, del_url, profileId, phd) {
    // Create form data to delete on back end
    var formData = new FormData();
    formData.append('school_id', schoolId);

    // Use fetch to submit the form data
    fetch(del_url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // Delete on front end
    var school_area = document.getElementById(schoolId + "_item").outerHTML = "";
    // Allow adding school now that has been deleted
    var add_checkbox = document.getElementById(profileId + "_" + phd);
    add_checkbox.disabled = false;
    add_checkbox.checked = false;
}

function displaySchools() {
    var selected_option = document.getElementById("school_picker");
    var md_schools = document.getElementById("md_schools");
    var do_schools = document.getElementById("do_schools");
    var mdphd_schools = document.getElementById("mdphd_schools");
    var dophd_schools = document.getElementById("dophd_schools");
    var searchbar = document.getElementById("search_schools");
    if (selected_option.value == "md") {
        searchbar.classList.remove("d-none");
        md_schools.classList.remove("d-none");
        do_schools.classList.add("d-none");
        mdphd_schools.classList.add("d-none");
        dophd_schools.classList.add("d-none");
    } else if (selected_option.value == "do") {
        searchbar.classList.remove("d-none");
        md_schools.classList.add("d-none");
        do_schools.classList.remove("d-none");
        mdphd_schools.classList.add("d-none");
        dophd_schools.classList.add("d-none");
    } else if (selected_option.value == "mdphd") {
        searchbar.classList.remove("d-none");
        md_schools.classList.add("d-none");
        do_schools.classList.add("d-none");
        mdphd_schools.classList.remove("d-none");
        dophd_schools.classList.add("d-none");
    } else if (selected_option.value == "dophd") {
        searchbar.classList.remove("d-none");
        md_schools.classList.add("d-none");
        do_schools.classList.add("d-none");
        mdphd_schools.classList.add("d-none");
        dophd_schools.classList.remove("d-none");
    }
}

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
            .catch(error => console.log("No graph available."));
        fetch(plot_loc + "/status_" + school_id + "_phd_prev.JSON").then(response => response.json())
            .then(data => {
                data.config = {'responsive': true, 'displaylogo': false, 'displayModeBar': false};
                Plotly.newPlot('mini_cycle_status_prev', data);
            })
            .catch(error => console.log("No graph available."));

    } else {
        title_string = int_name + ' (' + md_or_do + ')';
        fetch(plot_loc + "/status_" + school_id + "_reg_curr.JSON").then(response => response.json())
            .then(data => {
                data.config = {'responsive': true, 'displaylogo': false, 'displayModeBar': false};
                Plotly.newPlot('mini_cycle_status_curr', data);
            })
            .catch(error => console.log("No graph available."));
        fetch(plot_loc + "/status_" + school_id + "_reg_prev.JSON").then(response => response.json())
            .then(data => {
                data.config = {'responsive': true, 'displaylogo': false, 'displayModeBar': false};
                Plotly.newPlot('mini_cycle_status_prev', data);
            })
            .catch(error => console.log("No graph available."));
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

function filterSchools() {
    var all_schools = document.getElementsByClassName('school_entry');
    var removeCount = 0;
    var status = document.getElementById("status_select").value;
    var program = document.getElementById("program_select").value;

    for (let i = 0; i < all_schools.length; i++) {
        var remove = false;
        // Check for program type
        if (program == 'all') {
            remove = false;
        } else if (program == 'MD-PhD') {
            if (all_schools[i].classList.contains('type_MD') && all_schools[i].classList.contains('phd_true')) {
                remove = false;
            } else {
                remove = true;
            }
        } else if (program == 'MD') {
            if (all_schools[i].classList.contains('type_MD') && all_schools[i].classList.contains('phd_false')) {
                remove = false;
            } else {
                remove = true;
            }
        } else if (program == 'DO-PhD') {
            if (all_schools[i].classList.contains('type_DO') && all_schools[i].classList.contains('phd_true')) {
                remove = false;
            } else {
                remove = true;
            }
        } else if (program == 'DO') {
            if (all_schools[i].classList.contains('type_DO') && all_schools[i].classList.contains('phd_false')) {
                remove = false;
            } else {
                remove = true;
            }
        }

        // Check for status
        if (!all_schools[i].classList.contains('status_' + status) && status != 'all') {
            remove = true;
        }

        // Perform remove if needed
        if (remove) {
            all_schools[i].classList.add('d-none');
            removeCount++;
        } else {
            all_schools[i].classList.remove('d-none');
        }
    }

    // Display no schools found message when number of schools removed matches school count
    var noSchools = document.getElementById('no_schools');
    if (all_schools.length == removeCount) {
        noSchools.classList.remove("d-none");
    } else {
        noSchools.classList.add("d-none");
    }
}