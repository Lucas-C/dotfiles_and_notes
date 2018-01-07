// NOT TO SELF: puppeteer >more>stable> SlimerJS >more>standard> PhantomJs -> cf. https://github.com/ariya/phantomjs/issues/15236
// DESCRIPTION: Ce script a pour but de garder un historique de screenshots de ce à quoi ressemble NSR au cours de son évolution.
// AUTHOR: Lucas Cimon
// INSTALL: sudo npm install -g casperjs slimerjs
/*  + sous Cygwin, utiliser ceci :
casperjs () {
    local node_path="$(npm list -g 2>/dev/null | head -n 1)\node_modules"
    local engine=phantomjs
    [ "$1" = "--engine=slimerjs" ] && engine=slimerjs && shift
    local script_winpath="$(cygpath -aw "$1")"; shift
    NODE_PATH=$node_path $engine "$node_path\casperjs\bin\bootstrap.js" --casper-path="$node_path\casperjs" --cli $script_winpath "$@"
}
 */
// USAGE: casperjs --engine=slimerjs --proxy=$PROXY_HOST:$PROXY_PORT --debug=yes multidevices-take-nsr-screenshots.js
// HEADLESS: avant la commande ci-dessus :
//    Xvfb :19 -screen 0 1920x1080x16 >/Xvfb.log 2>&1 &
//    export DISPLAY=:19

const consent_cookie   = {name: 'hasConsent',    value: 'true',                                     domain: 'jobs.voyages-sncf.com'};
const punchline_cookie = {name: 'nsr_punchline', value: '%22USER_EXPLICITLY_CHOSE_NO_PUNCHLINE%22', domain: 'jobs.voyages-sncf.com'};
const pages = [
    {url: 'jobs.voyages-sncf.com/',                                                  cookies: [consent_cookie], comment: 'no-punchline-cookie' },
    {url: 'jobs.voyages-sncf.com/',                                                  cookies: [consent_cookie, punchline_cookie]               },
    {url: 'jobs.voyages-sncf.com/offers',                                            cookies: [consent_cookie, punchline_cookie]               },
    {url: 'jobs.voyages-sncf.com/news/15_ans_de_voyage_avec_nos_clients_a21855da08', cookies: [consent_cookie, punchline_cookie]               },
    {url: 'jobs.voyages-sncf.com/offer/Chef_de_Projet_b4bbe448fd',                   cookies: [consent_cookie, punchline_cookie]               },
];
const viewports = [
    {name: 'iphone4-portrait',     dims: {width: 320,  height: 480}  },
    {name: 'iphone4-landscape',    dims: {width: 480,  height: 320}  },
    {name: 'iphone5-landscape',    dims: {width: 558,  height: 320}  },
    {name: 'iphone6-portrait',     dims: {width: 375,  height: 667}  },
    {name: 'iphone6-landscape',    dims: {width: 667,  height: 375}  },
    {name: 'ipad-portrait',        dims: {width: 768,  height: 1024} },
    {name: 'ipad-landscape',       dims: {width: 1024, height: 768}  },
    {name: 'desktop-old-standard', dims: {width: 1280, height: 1024} },
    {name: 'desktop-large-thin',   dims: {width: 1366, height: 768}  },
];

const todayStrDate = (new Date()).toISOString().substring(0, 10);
const delay = 1500;
const casper = require('casper').create({
    verbose: true,
    logLevel: 'debug'
});
casper.start('http://jobs.voyages-sncf.com');

viewports.forEach(function(viewport) {
    pages.forEach(function(page) {
        casper.then(function () {
            casper.page.cookies = page.cookies.map(makeCookie);
            casper.page.viewportSize = viewport.dims;
        }).thenOpen('http://' + page.url, function() {
            casper.wait(delay);
        }).then(function() {
            casper.capture(todayStrDate
                           + '_' + page.url
                           + (page.comment ? '_' + page.comment : '')
                           + '_' + viewport.name
                           + '_' + viewport.dims.width + 'x' + viewport.dims.height + '.png');
        });
    });
});

casper.on('remote.message', function(browser_console_msg) {
  console.log(browser_console_msg);
});
casper.run();

function makeCookie(cookie) {
    return {
        'name':     cookie.name,
        'value':    cookie.value,
        'domain':   cookie.domain,
        'path':     cookie.path || '/',
        'expires':  cookie.expires || ((new Date()).getTime() + 3600 * 24 * 30) /* <- expires in 1 month */,
        'httponly': cookie.httponly || false,
        'secure':   cookie.secure || false,
    }
}
