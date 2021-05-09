const handle_dropped_file = function(event) {
  console.log(event)
}

const handle_selected_file = function(file_pointer) {
  if (file_pointer.files && file_pointer.files[0]) {
    var reader = new FileReader()

    reader.onload = function(e) {
      $(".file-upload-wrapper").hide()
      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();

      let k = document.getElementById('remove-button').className.split(" "); k.pop();
      document.getElementById('remove-button').className = k.join(" ")
    }
    
    reader.readAsDataURL(file_pointer.files[0]);
  }
}

const remove_file = function() {
  $('.file-upload-content').hide();
  $('.file-upload-wrapper').show();
  let k = document.getElementById('remove-button').className + " disabled"
  document.getElementById('remove-button').className = k
}