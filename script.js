document.getElementById('hide-button').addEventListener('click', function() {
  var originalImageInput = document.getElementById('original-image');
  var secretTextInput = document.getElementById('secret-text');

  var originalImageFile = originalImageInput.files[0];
  var secretText = secretTextInput.value;

  if (!originalImageFile || !secretText) {
    alert('Please select an image and enter text.');
    return;
  }

  var formData = new FormData();
  formData.append('image', originalImageFile);
  formData.append('secret_text', secretText);

  fetch('/hide', {
    method: 'POST',
    body: formData
  })
  .then(response => response.blob())
  .then(blob => {
    var downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(blob);
    downloadLink.download = 'hidden_image.png';
    downloadLink.click();
  })
  .catch(error => console.error('Error:', error));
});
