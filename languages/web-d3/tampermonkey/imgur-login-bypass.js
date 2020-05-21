// ==UserScript==
// @name         Imgur Login Bypass
// @namespace
// @version      0.3
// @description  A small script that bypassess Imgur's NSFW login requierment for single image posts.
// @author       128bitz then Lucas-C
// @license      GPL-3.0-or-later; http://www.gnu.org/licenses/gpl-3.0.txt
// @match        https://imgur.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    if (window.location.href.includes('/embed')) {
        // There is an annoying link to on the image, we remove it:
        function removeImageLink() {
            const imgLinkAnchor = document.getElementById('image-link');
            if (imgLinkAnchor && imgLinkAnchor.children.length) {
                imgLinkAnchor.parentNode.appendChild(imgLinkAnchor.children[0]);
            }
            // Make the image clickable to get to next page:
            document.getElementById('image').children[0].onclick = () => {
                document.getElementById('next-hover').click();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            };
            setTimeout(removeImageLink, 500);
        }
        removeImageLink();
    } else {
        // Auto-redirect to public page:
        window.location += '/embed?pub=true';
    }
})();
