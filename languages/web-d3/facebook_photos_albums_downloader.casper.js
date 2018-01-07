// NOT TO SELF: puppeteer >more>stable> SlimerJS >more>standard> PhantomJs -> cf. https://github.com/ariya/phantomjs/issues/15236
// INSTALL: sudo npm install -g phantomjs slimerjs
//          echo -e "var require = patchRequire(require);\nmodule.exports = require('lodash');" > lodash.js
// USAGE: ANSICON=1 casperjs --engine=slimerjs --debug=yes $this --email=$email --password=$password --album-url=$url
//        ^ this enable colored output under Windows x64

require('lodash');

var casper = require('casper').create({
        viewportSize: {width: 1366, height: 768},
        verbose: true,
        logLevel: 'debug'
    });

casper.start(casper.cli.get('album-url'));

casper.then(function () {
    casper.fill('form#login_form', {
        email: casper.cli.get('email'),
        pass: ''+casper.cli.get('password') // conversion to string is mandatory, cf. CasperJS issue #1275
    }, true);
    casper.waitWhileSelector('#login_form', function () {
        casper.scrollToBottom();
        casper.wait(2000, function () {
            anchorIds = this.evaluate(function() {
                return __utils__.findAll('#fbTimelinePhotosContent a.uiMediaThumb').map(function(a) {
                    return a.getAttribute('id');
                });
            });
            casper.echo('anchorIds count: ' + anchorIds.length, 'WARNING');
            recurOpenPopin(anchorIds, 0);
        });
    });
});

function recurOpenPopin(anchorIds, index) {
    var anchorId = anchorIds[index];
    casper.echo('recurOpenPopin index=' + index + ' - anchorId=' + anchorId, 'WARNING');
    casper.echo('[recurOpenPopin] pendingWait=' + casper.pendingWait + ' - loadInProgress=' + casper.loadInProgress + ' - navigationRequested=' + casper.navigationRequested, 'INFO_BAR');
    casper.waitForSelector('#' + anchorId, function () {
        casper.click('#' + anchorId);
        // "Whenever a step is completed, CasperJS will check against 3 flags: pendingWait, loadInProgress, and navigationRequested.
        // If any of those flags is true, then do nothing, go idle until a later time (setInterval style).
        // If none of those flags is true, then the next step will get executed."
        // FROM: http://stackoverflow.com/a/13185963/636849 - source can be seen in Casper.checkStep : https://github.com/casperjs/casperjs/blob/master/modules/casper.js#L400
        casper.echo('[photoDownloader] pendingWait=' + casper.pendingWait + ' - loadInProgress=' + casper.loadInProgress + ' - navigationRequested=' + casper.navigationRequested, 'INFO_BAR');
        casper.wait(2000, function () {
            var photoUrl = casper.evaluate(function () { return document.querySelector('.spotlight').src; });
            casper.download(photoUrl, anchorId + '.jpg');
            casper.echo('Downloaded ' + photoUrl + ' -> ' + anchorId + '.jpg', 'WARNING');
            casper.click('._xlt');
            index++;
            if (index < anchorIds.length) {
                recurOpenPopin(anchorIds, index);
            }
        });
    });
}

casper.on('navigation.requested', function(url, type, willNavigate, isMainFrame) {
    casper.echo('[navigation.requested] url=' + url + ' - type=' + type + ' - willNavigate=' + willNavigate + ' - isMainFrame=' + isMainFrame, 'INFO_BAR');
    casper.navigationRequested = false;
});

casper.on('resource.requested', function(requestData, networkRequest) {
    casper.echo('[resource.requested] pendingWait=' + casper.pendingWait + ' - loadInProgress=' + casper.loadInProgress + ' - navigationRequested=' + casper.navigationRequested, 'INFO_BAR');
    require('utils').dump(requestData);
    /*if (/facebook\.com\/ajax\/ei\.php/.exec(requestData.url)) {
        casper.echo('Aborting request ' + requestData.url, 'WARN_BAR');
        networkRequest.abort();
    } else {
        casper.echo('Allowing request ' + requestData.url, 'GREEN_BAR');
    }*/
});

casper.on('resource.received', function(resource) {
    casper.echo('[resource.received] pendingWait=' + casper.pendingWait + ' - loadInProgress=' + casper.loadInProgress + ' - navigationRequested=' + casper.navigationRequested, 'INFO_BAR');
    require('utils').dump(resource);
});

casper.on('remote.message', function(message) { // console spy to ease debugging
    console.echo(message, 'COMMENT');
});

casper.run();




function displayCookies() {
    phantom.cookies.map(function (c) {
        casper.echo('domain='+c.domain+' name='+c.name+' path='+c.path+' value='+c.value);
    });
}

function cookieValuesPerName() {
    var valuesPerName = {};
    phantom.cookies.map(function (cookie) {
        valuesPerName[cookie.name] = cookie.value;
    });
    return valuesPerName;
}
