var currentPage = 0;
var maxPages = 100;
var url = '/admin-panel/load-more-posts';


document.getElementById('load-more').addEventListener('click', function() {
  currentPage++;
  loadPosts(currentPage);
});

function loadPosts(page) {
  var xhr = new XMLHttpRequest();

  xhr.open('GET', url + '?page=' + page, true);

  xhr.onload = function() {
    if (xhr.status === 200) {
      console.log('success');

      var data = JSON.parse(xhr.responseText);
      var logs = data.logs;

      var postList = document.getElementById('logs-list');
      for (var i=0; i<logs.length; i++) {

        var li = document.createElement('li');
        li.classList.add("table-row");
        for (const key in logs[i]) {

            var span = document.createElement('span');
            span.textContent = logs[i][key];
            span.classList.add("table-data");

            li.appendChild(span);
        }

        postList.appendChild(li);
      }
    }
    else {
        console.log('error 404');
    }
  };

  xhr.send();
}