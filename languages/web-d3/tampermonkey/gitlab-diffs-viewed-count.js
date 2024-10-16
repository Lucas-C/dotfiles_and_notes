// ==UserScript==
// @name        Gitlab diffs viewed files count
// @match       https://*/*/-/merge_requests/*/diffs
// @grant       GM_addStyle
// @version     1.0
// @author      Lucas Cimon
// ==/UserScript==

const viewedDiv = document.createElement("div");
viewedDiv.id = "viewed-count";
document.body.appendChild(viewedDiv);

GM_addStyle (`
    #viewed-count {
      position: fixed;
      top: 0;
      right: 0;
      z-index: 9000; /* must be > 200 */
      padding: 1rem;
    }
`);

function updateViewedCount() {
  viewedDiv.textContent = "Viewed count: " + Object.keys(JSON.parse(localStorage[`${location.pathname.replace('/diffs', '')}-file-reviews`])).length;
}
updateViewedCount();
document.addEventListener("click", updateViewedCount);
