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
      let j = document.getElementById('save-button').className.split(" "); j.pop();
      document.getElementById('save-button').className = j.join(" ")
    }
    
    reader.readAsDataURL(file_pointer.files[0]);
  }
}

const handle_upload = function() {
  let img_src = document.getElementById("uploaded-img-src").src

}

const reset_input = function() {
  document.getElementById('manual-upload').value = '';
  console.log(document.getElementById('manual-upload').value)
}

const remove_file = function() {
  $('.file-upload-content').hide();
  $('.file-upload-wrapper').show();
  let k = document.getElementById('remove-button').className + " disabled"
  document.getElementById('remove-button').className = k
  let j = document.getElementById('save-button').className + " disabled"
  document.getElementById('save-button').className = j
}