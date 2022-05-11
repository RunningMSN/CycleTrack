function deleteCycle(cycleId) {
  fetch("/delete-cycle", {
    method: "POST",
    body: JSON.stringify({ cycleId: cycleId }),
  }).then((_res) => {
    window.location.href = "/cycles";
  });
}

function deleteSchool(schoolId, cycleId) {
  fetch("/delete-school", {
    method: "POST",
    body: JSON.stringify({ schoolId: schoolId }),
  }).then((_res) => {
    let form = '<form method="POST" action = "/lists"><input type="hidden" name="cycle_id" id="cycle_id" value=' + cycleId + '></form>';
    let formElement = $(form);
    $('body').append(formElement);
    $(formElement).submit()
  });
}