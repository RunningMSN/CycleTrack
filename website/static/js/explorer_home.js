var school_type = 'All';
var state = 'All';
var country = 'All';

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
});

function filterSettings() {
    var all_schools = document.getElementsByClassName('school_entry');
    for (let i = 0; i < all_schools.length; i++){
        var remove = false;
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
        // Add or remove school
        if (remove) {
            all_schools[i].classList.add("d-none");
        } else {
            all_schools[i].classList.remove("d-none");
        }
    }
}