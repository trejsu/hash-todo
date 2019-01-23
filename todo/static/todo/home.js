function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function () {
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $('.tick').click(function () {
    var id = $(this).attr('data-id');
    var status = $(this).attr('data-status');
    var data = {status: oppositeStatus(status)};

    var tick = $(this);

    $.ajax({
      type: 'PATCH',
      // todo: extract base url
      url: 'http://localhost:8000/api/v1/tasks/' + id + '/',
      contentType: 'application/json',
      data: JSON.stringify(data)
    }).done(function (data) {
      $('#item-' + data.id).addClass(data.status).removeClass(oppositeStatus(data.status));
      $('#tick-' + data.id).addClass(statusToIcon[data.status]).removeClass(statusToIcon[oppositeStatus(data.status)]);
      tick.attr('data-status', data.status);
    }).fail(function (msg) {
      console.error(msg);
    });
  });

});

function oppositeStatus(status) {
  return status === 'active' ? 'done' : 'active';
}

var statusToIcon = {
  'active': 'far fa-circle',
  'done': 'fas fa-check'
};