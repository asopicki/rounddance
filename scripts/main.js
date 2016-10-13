"use strict";

(function() {

if (window.JSON && window.atob && document.querySelectorAll && document.querySelector) {
  initSearch();
  loadCuesheets();
  initForm();
}

function initSearch() {
  document.idx = lunr(function() {
    this.field('title', {"boost": 10});
    this.field('phase');
    this.field('difficulty');
    this.field('music');
    this.field('author');
    this.field('rhythm');
  });
}

function initForm() {
  var search = document.querySelector('#query');

  search.disabled = false;

  search.addEventListener('keyup', function(event) {
    var term = search.value;

    var result = null;

    if (term.length > 2) {
      result = document.idx.search(term);

      if (window.console) {
        console.log(result);
      }
    }


  }, {capture: true});
}

function loadCuesheets() {

  var links = document.querySelectorAll(".cuesheet");
  var i = 1;

  for (let l of links) {
    var meta = JSON.parse(window.atob(l.dataset.meta));

    meta.id = i;

    document.idx.add(meta);

    i += 1;
  }

  if (window.console) {
    console.log("Found " + links.length + " different titles")
  }

  /*var lists = document.querySelectorAll("div.list");

  for (let i = 0; i < lists.length; i++) {
    if (document.cuesheets[i].length == 0) {
      lists[i].classList.add("empty");
    }
  }*/
}
})();
