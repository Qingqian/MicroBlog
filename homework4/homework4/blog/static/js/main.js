setInterval(function () {
  $.ajax({
    url: '/blog/blogger-list',
    type: 'GET',
    success: function (html) {
      console.log('replaced');
      $('#blogger-list').html(html);
    }
  });
}, 7000);
