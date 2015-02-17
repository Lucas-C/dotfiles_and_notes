// Disclaimer: NEVER AGAIN !
// Next time, use Selenium Webdriver or CasperJS

// USAGE: firefox imacros://run/?m=Woffi_scrapper.js
// Woffi_scrapper.js has to be in the ~/iMacros/Macros directory, and the Woffi web page open

(function () {
'use strict';
    var IMACRO = ['SET !TIMEOUT_STEP 0',
                  'TAB T=1',
                  'URL GOTO=javascript:void((function()%7BgoTo({goto_index})%7D)())',
                  'SAVEAS TYPE=HTM FOLDER=* FILE=page_{goto_index}.htm'].join('\n'),
    LOGS = [],
    range = function (start, end, step) {
        step = step || 1;
        var range_array = [];
        for (var i = start; i < end; i++) {
            range_array.push(i * step);
        }
        return range_array;
    },
    sleep = function (delay) {
        iimPlayCode('WAIT SECONDS=' + delay);
    },
    log = function (msg) {
        LOGS.push(msg);
    },
    main = function () {
        var goto_indices = range(0, 212, 25);
        log('Indices: ' + goto_indices.join(','));
        //sleep(3);
        for (var i = 0; i < goto_indices.length; i++) {
            var goto_index = goto_indices[i];
            log('goto_index:' + goto_index);
            var imacro = IMACRO.replace(/{goto_index}/g, goto_index),
                return_code = iimPlayCode(imacro);
            log('Return code: ' + return_code + ' - Error: ' + iimGetErrorText());
        }
    };
    main();
    iimDisplay(LOGS.join('\n'));
})();

/*iimPlay('CODE:\nSET !EXTRACT "OK"')
iimDisplay(iimGetExtract()); // works
iimPlay('CODE:\nSET !EXTRACT {{!FILELOG}}')
iimDisplay(iimGetExtract()); // 'undefined' => no default value (not supported in FF in fact) */

