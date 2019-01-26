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

});

