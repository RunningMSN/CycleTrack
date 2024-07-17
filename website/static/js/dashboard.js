function toggleOtherGender(year) {
    var genderOption = document.getElementById("gender_" + year);
    var genderOtherSection = document.getElementById("other_gender_" + year);

    if (genderOption.value == "Other") {
        genderOtherSection.classList.remove("d-none")
    } else {
        genderOtherSection.classList.add("d-none")
    }
}

function toggleOtherSex(year) {
    var sexOption = document.getElementById("sex_" + year);
    var sexOtherSection = document.getElementById("other_sex_" + year);

    if (sexOption.value == "Other") {
        sexOtherSection.classList.remove("d-none")
    } else {
        sexOtherSection.classList.add("d-none")
    }
}

function toggleOtherRaceEthnicity(year) {
    var raceEthnicityOption = document.getElementById("race_ethnicity_" + year);
    var raceEthnicitySection = document.getElementById("other_race_ethnicity_" + year);

    if (raceEthnicityOption.value == "Other") {
        raceEthnicitySection.classList.remove("d-none")
    } else {
        raceEthnicitySection.classList.add("d-none")
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