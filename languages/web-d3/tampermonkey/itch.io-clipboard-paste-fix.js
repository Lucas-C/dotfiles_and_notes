// ==UserScript==
// @name        itch.io-clipboard-paste-fix
// @namespace   Violentmonkey Scripts
// @match       https://*.itch.io/*
// @grant       none
// @version     1.0
// @author      Lucas Cimon
// @description Enable clipboard pasting in itch.io review forms - Context: https://chezsoi.org/shaarli/shaare/YIa5Wg
// ==/UserScript==

window.$.Redactor.prototype.paste = () => ({})



// Research debug code:
var Redactor = window.$.Redactor; // cf. https://imperavi.com/redactor/docs/
var originalPaste = Redactor.prototype.paste;
Redactor.prototype.paste = function() {
  console.log("Redactor.paste() START - this.opts:", this.opts);
  var paste = originalPaste();
  var originalInit = paste.init;
  paste.init = function (e) {
    console.log("Redactor.paste.init() START");
    originalInit.apply(this, [e]);
  };
  return paste;
}

var originalUtils = Redactor.prototype.utils;
Redactor.prototype.utils = function() {
  console.log("Redactor.utils() START");
  var utils = originalUtils();
  return utils;
}

Redactor.settings.callbacks = {
  paste: function () {
    console.log("Redactor.settings.callbacks.paste START - this:", this);
  },
};
