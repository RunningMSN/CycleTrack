function checkPasswordMatch() {
    var password1 = document.getElementById("password1").value;
    var password2 = document.getElementById("password2").value;
    var text_div = document.getElementById("password_match_text");

    if (password1 == password2) {
        text_div.classList.add("d-none");
        return true;
    } else {
        text_div.classList.remove("d-none");
        return false;
    }
}

function checkPasswordRequirements() {
    // Only use the first password for checking
    var password = document.getElementById("password1").value;
    var text_div = document.getElementById("password_requirement_text");

    if (password.length > 7) {
        text_div.classList.add("d-none");
        return true;
    } else {
        text_div.classList.remove("d-none");
        return false;
    }
}

function formValid() {
    var terms_agree = document.getElementById("terms_agree").checked;
    var email = document.getElementById("email").value;
    var submit_button = document.getElementById("submit_button");
    if (checkPasswordRequirements() && checkPasswordMatch() && email.length > 0 && terms_agree) {
        submit_button.removeAttribute("disabled");
    } else {
        submit_button.setAttribute("disabled", "disabled");
    }
}