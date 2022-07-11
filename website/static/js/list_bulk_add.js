// Multi school list
schools = [];
phds = [];
function addSchool() {
    school = document.getElementById('add_school').value;
    phd = document.getElementById('md_phd_check');
    // check if have exact same entry
    if (schools.includes(school)) {
        if (!phds[schools.lastIndexOf(school)] == phd.checked && !phds[schools.indexOf(school)] == phd.checked) {
            if (school.length > 0) {
                schools.push(school);
                phds.push(phd.checked)
            }
        }
    } else {
        if (school.length > 0) {
            schools.push(school);
            phds.push(phd.checked)
        }
    }
    updateDisplay();
}

function removeSchool(school) {
    schools.splice(schools.indexOf(school), 1);
    phds.splice(schools.indexOf(school), 1);
    updateDisplay();
}

function updateDisplay() {
    add_school_list = document.getElementById('add_schools_list');
    add_school_list.innerHTML = "";
    for (let i = 0; i < schools.length; i++) {
        if (!phds[i]) {
            add_school_list.innerHTML += "<li class='list-group-item'>" +
            "<button type='button' class='btn btn-link' onclick='removeSchool(&quot;" + schools[i] + "&quot;)'><i class='bi bi-trash'></i></button>" +
            schools[i] +
            "</li>"
        } else {
            add_school_list.innerHTML += "<li class='list-group-item'>" +
            "<button type='button' class='btn btn-link' onclick='removeSchool(&quot;" + schools[i] + "&quot;)'><i class='bi bi-trash'></i></button>" +
            schools[i] + " (PhD)" +
            "</li>"
        }
    }
    //create custom delimiter for parsing values
    delimitedschools = schools.join('<>');
    delimitedphds = phds.join('<>');
    document.getElementById('school_names').value = delimitedschools;
    document.getElementById('phd_values').value = delimitedphds;
}