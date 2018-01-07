// NOT TO SELF: puppeteer >more>stable> SlimerJS >more>standard> PhantomJs -> cf. https://github.com/ariya/phantomjs/issues/15236
// INSTALL: sudo npm install -g phantomjs@1.9.16 casperjs
//    the latest v1.9.17 version of PhantomJS crashed, so I used the previous one
// USAGE: casperjs --web-security=no $this --email=$email --password=$password < photobox_photos_ids.txt
//                 ^ this is to avoid 'casperjs cannot make cross domain ajax requests' errors
// Photobox photos ids retrieved from an album page source HTML with:
//    grep -o '/mon-photobox/photo?album_id=59146573&photo_id=[0-9]\+' album.html | uniq | sed 's/.*[^0-9]\([0-9]\+\)$/\1/'

var system = require('system'),
    casper = require('casper').create({
        verbose: true,
        logLevel: 'debug'
    });

casper.start('http://www.photobox.fr/mon-espace');

casper.on('remote.message', function(message) {
  console.log(message);
});

casper.then(function () { // DEBUG
    require('utils').dump(casper.steps.map(function(step) {
        return step.toString();
    }));
});

casper.then(function () {
    casper.fill('form#pbx_loginform', {
        email: casper.cli.get('email'),
        password: ''+casper.cli.get('password') // conversion to string is mandatory, cf. CasperJS issue #1275
    }, true);
    check_login_succeeded(); // Not yet !
    casper.waitWhileSelector('#pbx_signin');
});

casper.then(function () {
    check_login_succeeded(); // This time yes
    casper.capture('post-login-step.png');
    while (!system.stdin.atEnd()) {
        var id = system.stdin.readLine();
        // We cannot define a function directly here as we are inside a loop
        casper.then(imgDownloader(id));
    }
});

function check_login_succeeded () {
    casper.log('#pbx_signin exists: ' + casper.exists('#pbx_signin'));
    var pbx_popup_window_css_display = casper.evaluate(function () { return document.getElementById('pbx_popup_window').style.display; });
    casper.log('#pbx_popup_window CSS display: ' + pbx_popup_window_css_display); // Should be ''
    var pbx_signin_text = casper.evaluate(function () { return document.getElementById('account-icon').textContent.trim(); });
    casper.log('#pbx_signin text: ' + pbx_signin_text); // Should NOT be 'Mon espace'
}

function imgDownloader (id) {
    return function () {
        casper.open('http://www.photobox.fr/mon-espace/photo/agrandie?photo_id=' + id).then(function () {
            var imgSrc = casper.evaluate(function () { return document.querySelector('body > img').src; });
            casper.echo(imgSrc + ' ' + id + '.jpg');
            casper.download(imgSrc, id + '.jpg');
        });
    };
}

casper.run();
