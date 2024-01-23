// ==UserScript==
// @name        canva.com-only-free-templates
// @description Only display free templates on canva.com
// @namespace   Violentmonkey Scripts
// @match       https://www.canva.com/fr_fr/modeles/*
// @version     1.0
// @author      Lucas-C
// @run-att     document-start
// ==/UserScript==

function main() {
  if (!/pricing=FREE/.test(window.location.search)) {
      window.location.search += "&pricing=FREE";
  }
}
// Recipe from: https://stackoverflow.com/a/17872564/636849
setInterval (
    function () {
        if (    this.lastPathStr  !== location.pathname
            ||  this.lastQueryStr !== location.search
            ||  this.lastPathStr   === null
            ||  this.lastQueryStr  === null
        ) {
            this.lastPathStr  = location.pathname;
            this.lastQueryStr = location.search;
            main();
        }
    }
    , 222
);