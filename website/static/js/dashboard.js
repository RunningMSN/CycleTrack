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