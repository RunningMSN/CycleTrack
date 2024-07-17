var school_type = 'All';
var state = 'All';
var country = 'All';
var search = 'All';

$(document).ready(function() {
    $("#school_type").change(function() {
        school_type = $(this).val();
        filterSettings();
    });
    $("#state").change(function() {
        state = $(this).val();
        filterSettings();
    });
    $("#country").change(function() {
        country = $(this).val();
        filterSettings();
    });
     $("#searchbar").on('input', function() {
        input = $(this).val();
        if (input.length > 0) {
            search = input;
        } else {
            search = 'All';
        }
        filterSettings();
    });
});

function filterSettings() {
    var all_schools = document.getElementsByClassName('school_entry');
    var removeCount = 0;
    for (let i = 0; i < all_schools.length; i++){
        var remove = false;
        // Check search
        if (search != 'All') {
            if (!all_schools[i].id.toLowerCase().includes(search.toLowerCase())) {
                remove = true;
            }
        }
        // Check school type
        if (school_type != 'All') {
            if (!all_schools[i].classList.contains('school_type_' + school_type)) {
                remove = true;
            }
        }
        // Check state
        if (state != 'All') {
            if (!all_schools[i].classList.contains('state_' + state)) {
                remove = true;
            }
        }
        // Check country
        if (country != 'All') {
            if (!all_schools[i].classList.contains('country_' + country)) {
                remove = true;
            }
        }

        // Check applied setting
        var appliedSetting = document.getElementById("toggle_applied");
        if (appliedSetting.checked) {
            if (!all_schools[i].classList.contains('applied_True')) {
                remove = true;
            }
        }

        // Add or remove school
        if (remove) {
            all_schools[i].classList.add("d-none");
            removeCount += 1;
        } else {
            all_schools[i].classList.remove("d-none");
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

async function research(answer) {
    var research_invite = document.getElementById("research_invite");
    var research_form = document.getElementById("research_form");
    var research_answer = document.getElementById("research_answer");

    research_answer.value = answer;

    var formData = new FormData(research_form);

    try {
        const response = await fetch(research_form.action, {
            method: 'POST',
            body: formData
        });
    } catch (error) {
        console.error('Form submission error:', error);
    }

    research_invite.classList.add("d-none");
}