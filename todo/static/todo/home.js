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

  var hoverCounter = 0;

  $('#add-icon').hover(
    function () {
      if (hoverCounter < 1) {
        $(this).html('<i class="fas fa-plus-circle"></i>');
        hoverCounter += 1;
      }
    },
    function () {
      if (hoverCounter > 0) {
        $(this).html('<i class="fas fa-plus"></i>');
        hoverCounter -= 1;
      }
    }
  );

  $('#id_date').datepicker();

  // $('#todo-date').each(
  //   function() {
  //       console.log('dupa');
  //       var time = moment($(this).text());
  //       $(this).html(time.endOf('day').fromNow());
  //     }
  // );

});

