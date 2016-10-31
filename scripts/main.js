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
        updateResultList(result);
      }
    }
  }, {capture: true});
}

function updateResultList(searchResult) {
  var list = document.querySelector("#resultlist");

  //clear current search results
  while(list.firstChild) {
    list.removeChild(list.firstChild);
  }

  var resultList = document.createElement('ul');
  list.appendChild(resultList);

  for (let i of searchResult) {
    var meta = document.cuesheets[i.ref-1];

    var liElem = document.createElement('li');
    var anchorElem = document.createElement('a');
    liElem.appendChild(anchorElem);

    anchorElem.appendChild(document.createTextNode(meta.title));
    anchorElem.href = 'file://' + meta._path;
    resultList.appendChild(liElem);

  }
}

function loadCuesheets() {

  var links = document.querySelectorAll(".cuesheet");
  var i = 1;
  document.cuesheets = [];

  for (let l of links) {
    var meta = JSON.parse(window.atob(l.dataset.meta));

    meta.id = i;

    document.idx.add(meta);
    document.cuesheets.push(meta);

    i += 1;
  }

  if (window.console) {
    console.log("Found " + links.length + " different titles")
  }

}
})();
