$(document).ready(function() {
    // Check map scope and hiding names
    var mapScope = document.getElementById('mapScope');
    var hideNames = document.getElementById('hideNames');
    var organizeY = document.getElementById('organizeY');
    $("#vis_type").change(function() {
        var vis_type = $(this).val();
        if (vis_type == 'Map') {
            mapScope.classList.remove("d-none");
        } else {
            mapScope.classList.add("d-none");
        }

        if (vis_type == 'Dot' || vis_type == 'Timeline') {
            hideNames.classList.remove("d-none");
            organizeY.classList.remove("d-none");
        } else {
            hideNames.classList.add("d-none");
            organizeY.classList.add("d-none");
        }
    });

    // Toggle advanced options
    $('#advancedOptions').click(function() {
        $("#advancedArea").toggle(this.checked);
    });
});