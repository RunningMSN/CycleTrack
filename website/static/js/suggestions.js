function checkValid() {
        var form_type = document.getElementById("form_type").value;
        var content = document.getElementById("content").value
        var button = document.getElementById("submit_button");

        if (form_type !== "" && content !== "") {
            button.removeAttribute("disabled");
        } else {
            button.setAttribute("disabled", "disabled");
        }
     }