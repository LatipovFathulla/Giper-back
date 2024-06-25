document.addEventListener("DOMContentLoaded", function() {
  var fileInput = document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener('mousedown', function(event) {
      if ((event.metaKey || event.ctrlKey) && !fileInput.hasAttribute('multiple')) {
        fileInput.setAttribute('multiple', 'multiple');
      }
    });

    fileInput.addEventListener('mouseup', function(event) {
      if (!(event.metaKey || event.ctrlKey) && fileInput.hasAttribute('multiple')) {
        fileInput.removeAttribute('multiple');
      }
    });
  }
});
