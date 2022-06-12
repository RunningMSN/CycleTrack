// Filter settings
var mddo = false;
var mddophd = false;
var mentorship = false;
var lors = false;
var mcat = false;
var qa = false;
var international = false;

// All elements
var allItems = document.getElementsByClassName('resource-item')

function changeSetting(buttonId) {
    // Change settings
    if (buttonId == 'mddo_button') {
        mddo = !mddo;
    } else if (buttonId == 'mddophd_button') {
        mddophd = !mddophd;
    } else if (buttonId == 'mentorship_button') {
        mentorship = !mentorship;
    } else if (buttonId == 'lors_button') {
        lors = !lors;
    } else if (buttonId == 'mcat_button') {
        mcat = !mcat;
    } else if (buttonId == 'qa_button') {
        qa = !qa;
    } else if (buttonId == 'international_button') {
        international = !international;
    }

    // Change button appearance
    var element = document.getElementById(buttonId);
    if (element.classList.contains('btn-outline-primary')) {
        element.classList.remove('btn-outline-primary');
        element.classList.add('btn-primary');
    } else {
        element.classList.remove('btn-primary');
        element.classList.add('btn-outline-primary');
    }

    filterList();
}

function filterList() {
    if (!mddo && !mddophd && !mentorship && !lors && !mcat && !mcat && !qa && !international) {
        for (let i = 0; i < allItems.length; i++) {
            allItems[i].classList.remove('d-none');
        }
    } else {
        for (let i = 0; i < allItems.length; i++) {
            remove = false;
            // Check each filter
            if (mddo && !allItems[i].classList.contains('mddo')) {
                remove = true;
            }
            if (mddophd && !allItems[i].classList.contains('mddophd')) {
                remove = true;
            }
            if (mentorship && !allItems[i].classList.contains('mentorship')) {
                remove = true;
            }
            if (lors && !allItems[i].classList.contains('lors')) {
                remove = true;
            }
            if (mcat && !allItems[i].classList.contains('mcat')) {
                remove = true;
            }
            if (qa && !allItems[i].classList.contains('qa')) {
                remove = true;
            }
            if (international && !allItems[i].classList.contains('international')) {
                remove = true;
            }

            if (remove) {
                allItems[i].classList.add('d-none');
            } else {
                allItems[i].classList.remove('d-none');
            }
        }
    }
}