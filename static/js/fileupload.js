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

const src_to_blob = function(dataURI) {
    // convert base64 to raw binary data held in a string
    var byteString = atob(dataURI.split(',')[1]);
    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
    // write the bytes of the string to an ArrayBuffer
    var ab = new ArrayBuffer(byteString.length);
    // create a view into the buffer
    var ia = new Uint8Array(ab);
    // set the bytes of the buffer to the correct values
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    // write the ArrayBuffer to a blob, and you're done
    var blob = new Blob([ab], {type: mimeString});
    return blob;
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const handle_upload = function() {
  // extract the image
  let img_src = document.getElementById("uploaded-img-src").src
  let imgblob = src_to_blob(img_src);
  // get privacy settings and file name
  let public = document.getElementById('privacy-select-box').checked
  let img_name = document.getElementById('file-name-input').value

  // parse csrf and handle request
  try {
    let data = new FormData();
    if (img_name == "") {
      throw 'please input an image name'
    }
    data.append('img_name', img_name)
    data.append('img', imgblob)
    data.append('public', public)

    let csrf = getCookie('csrftoken')
    if (!csrf) {
      throw 'csrf token error'
    }

    let headers = new Headers(); 
    headers.append('X-CSRFToken', csrf)

    // make sure to send data in form of a blob
    fetch('/data/create_image/', {
      method: 'POST', 
      credentials: 'same-origin',
      cache: 'no-cache',
      mode: 'cors',
      body: data,
      headers: headers
    })
    .then((res) => {
      // show a success message
      if (res.status === 200) {
        remove_file(); reset_input();
        document.getElementById('add-image-close').click()

        Toastify({
          text: "Successfully uploaded!",
          duration: 3000
        }).showToast();
      
      }
      else {
        throw 'failed, please try again.'
      }
    })
    .catch((error) => {

      Toastify({
        text: 'failed, please try again.',
        backgroundColor: "linear-gradient(to right, #FF5733, #B42000)",
        duration: 3000
      }).showToast();

      throw error
    })
    
  } catch (error) {
    // show an error message
    console.log(error)
  }
}

const reset_input = function() {
  document.getElementById('manual-upload').value = '';
  document.getElementById('file-name-input').value = '';
}

const remove_file = function() {
  $('.file-upload-content').hide();
  $('.file-upload-wrapper').show();
  let k = document.getElementById('remove-button').className + " disabled"
  document.getElementById('remove-button').className = k
  let j = document.getElementById('save-button').className + " disabled"
  document.getElementById('save-button').className = j
}