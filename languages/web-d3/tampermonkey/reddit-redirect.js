// ==UserScript==
// @name         Redirect to old.reddit.com
// @description  The new reddit UI sucks ass
// @match        https://www.reddit.com/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';
    if (window.location.host === "www.reddit.com" && window.location.pathname.startsWith("/r/")) {
        window.location.href = window.location.href.replace("www.reddit.com", "old.reddit.com");
    }
})();
