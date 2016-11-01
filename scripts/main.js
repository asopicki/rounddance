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

function keyword_search(keyword, value) {
  if (window.console) {
    //console.debug('Keyword search fired for term "' + value + '"');
  }

  var result = [];

  for (var i = 0; i < document.cuesheets.length; i++) {
    var obj = document.cuesheets[i];

    if (obj[keyword] && obj[keyword].toLowerCase() === value.toLowerCase()) {
      result.push({
        ref: i+1,
        score: 1
      });
    }
  }

  return result;
}

function initForm() {
  var search = document.querySelector('#query');
  var keywwords = ['phase', 'difficulty'];

  var debounce = function (fn) {
      var timeout;
      return function () {
        var args = Array.prototype.slice.call(arguments),
            ctx = this;

        clearTimeout(timeout);
        timeout = setTimeout(function () {
          fn.apply(ctx, args)
        }, 300);
      }
  };

  search.disabled = false;
  search.select();

  search.addEventListener('input', debounce(function(event) {
    if (window.console) {
      //console.debug('Search fired for term "' + this.value + '"');
    }
    var term = this.value;

    var result = null;

    if (term.length > 2) {
      var keywordsearch = false;
      for (var kw of keywwords) {
        if (term.startsWith(kw+':')) {
          keywordsearch = true;
          result = keyword_search(kw, term.substr(kw.length+1));
        }
      }
      if (!keywordsearch) {
        result = document.idx.search(term);
      }
      updateResultList(result);
    }
  }), {capture: true});
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
