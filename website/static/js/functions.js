function deleteCycle(cycleId) {
  fetch("/delete-cycle", {
    method: "POST",
    body: JSON.stringify({ cycleId: cycleId }),
  }).then((_res) => {
    window.location.href = "/cycles";
  });
}

function deleteSchool(schoolId) {
  fetch("/delete-school", {
    method: "POST",
    body: JSON.stringify({ schoolId: schoolId }),
  }).then((_res) => {
    window.location.href = "/cycles"; /*fix later to make go back to school list*/
  });
}