$(document).ready(function() {
    // Check map scope
    var mapScope = document.getElementById('mapScope');
    $("#vis_type").change(function() {
        var vis_type = $(this).val();
        if (vis_type == 'Map') {
            mapScope.classList.remove("d-none");
        } else {
            mapScope.classList.add("d-none");
        }
    });
    // Toggle advanced options
    $('#advancedOptions').click(function() {
        $("#advancedArea").toggle(this.checked);
    });
});