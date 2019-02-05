$(document).ready(function () {

  $('[data-toggle="tooltip"]').tooltip();

  var urlParams = new URLSearchParams(window.location.search);
  var done = !urlParams.has('done') || urlParams.get('done') === 'true';
  var showDoneToggle = $('#show-done-toggle');
  toggleText(done);

  function toggleText(newDone) {
    showDoneToggle.text(newDone ? 'hide done' : 'show done');
  }

  showDoneToggle.click(function () {
    var newDone = !done;
    toggleText(newDone);
    urlParams.set('done', newDone.toString());
    window.location.href = '?' + urlParams.toString();
  });

  var addIconHoverCounter = 0;

  $('#add-icon').hover(
    function () {
      if (addIconHoverCounter < 1) {
        $(this).html('<i class="fas fa-plus-circle"></i>');
        addIconHoverCounter += 1;
      }
    },
    function () {
      if (addIconHoverCounter > 0) {
        $(this).html('<i class="fas fa-plus"></i>');
        addIconHoverCounter -= 1;
      }
    }
  );

  $('#id_date').datepicker({dateFormat: 'yy-mm-dd', defaultDate: new Date()});
  $(".datepicker[value='']").datepicker("setDate", "-0d");

});

