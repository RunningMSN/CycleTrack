function deleteCycle(cycleId) {
  fetch("/delete-cycle", {
    method: "POST",
    body: JSON.stringify({ cycleId: cycleId }),
  }).then((_res) => {
    window.location.href = "/cycles";
  });
}

function deleteClass(courseId) {
  fetch("/delete-class", {
    method: "POST",
    body: JSON.stringify({ courseId: courseId }),
  }).then((_res) => {
    window.location.href = "/gpa";
  });
}

function deleteBlock(blockId) {
  fetch("/delete-block", {
    method: "POST",
    body: JSON.stringify({ blockId: blockId }),
  }).then((_res) => {
    let form = '<form method="POST" action = "/profile"><input type="hidden" name="block_id" id="block_id" value=' + blockId + '> <input type="hidden" name="delete_block" value="{{block.id}}"></form>';
    let formElement = $(form);
    $('body').append(formElement);
    $(formElement).submit()
  });
}

function reorderBlock(blockId,blockOrder,direction){
  fetch("/reorder-block", {
    method: "POST",
    body: JSON.stringify({ blockId: blockId , blockOrder:blockOrder,direction:direction}),
  }).then((_res) => {
    let form = '<form method="POST" action = "/profile"><input type="hidden" name="block_id" id="block_id" value=' + blockId + '> <input type="hidden" name="reorder_block" value='+ blockOrder +'><input type="hidden" name="reorder_direction" value='+ direction +'></form>';
    let formElement = $(form);
    $('body').append(formElement);
    $(formElement).submit()
  });
}
