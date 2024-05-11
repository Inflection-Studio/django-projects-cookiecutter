Dropzone.autoDiscover = false;

$(document).ready(function () {
  const myDropzone = new Dropzone('#my-dropzone', {
    maxFiles: 10,
    maxFileSize: 3,
    parallelUploads: 10,
    acceptedFiles: '.jpg,.jpeg, .svg, .webp, .png',
    autoProcessQueue: false,
  });

  const submitButton = document.querySelector('#submit-all');

  submitButton.addEventListener('click', function () {
    myDropzone.processQueue(); // Tell Dropzone to process all queued files.
  });
});
