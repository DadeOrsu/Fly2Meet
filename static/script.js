  document.addEventListener('DOMContentLoaded', function () {
    const showAdvancedOptionsCheckbox = document.getElementById('show_advanced_options');
    const advancedOptionsElements = document.querySelectorAll('.advanced-option');

    showAdvancedOptionsCheckbox.addEventListener('change', function () {
      if (showAdvancedOptionsCheckbox.checked) {
        for (let i = 0; i < advancedOptionsElements.length; i++) {
          advancedOptionsElements[i].style.display = 'block';
        }
      } else {
        for (let i = 0; i < advancedOptionsElements.length; i++) {
          advancedOptionsElements[i].style.display = 'none';
        }
      }
    });
  });

