function deleteCycle(cycleId) {
  fetch("/delete-cycle", {
    method: "POST",
    body: JSON.stringify({ cycleId: cycleId }),
  }).then((_res) => {
    window.location.href = "/cycles";
  });
}