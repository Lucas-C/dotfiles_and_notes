// ==UserScript==
// @name         RiceBoy
// @namespace    https://chezsoi.org/lucas
// @version      0.1
// @description  Allow to navigate through Evan Dahm's online comics with arrow keys: Rice Boy, Order of Tales & Vattu
// @author       Lucas Cimon
// @match        https://tampermonkey.net/index.php?version=4.8.5847&ext=fire&updated=true
// @grant        none
// @include      http://www.rice-boy.com/order/index.php?c=*
// @include      http://www.rice-boy.com/see/index.php?c=*
// @include      http://www.rice-boy.com/vattu/index.php?c=*
// ==/UserScript==

(function() {
    'use strict';
    const pageNumber = +window.location.search.substr(3);
    window.onkeyup = e => {
        if (e.keyCode == '37') { // left arrow
            window.location.search = '?c=' + ('' + (pageNumber - 1)).padStart(3, '0');
        } else if (e.keyCode == '39') { // right arrow
            window.location.search = '?c=' + ('' + (pageNumber + 1)).padStart(3, '0');
        }
    };
})();