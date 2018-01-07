// NOT TO SELF: puppeteer >more>stable> SlimerJS >more>standard> PhantomJs -> cf. https://github.com/ariya/phantomjs/issues/15236
// INSTALL: sudo npm install -g phantomjs casperjs
// USAGE: casperjs $this --email=$email --password=$password 2>notifications

const stderr = require('system').stderr,
      casper = require('casper').create({
        verbose: true,
        logLevel: 'debug'
      });

casper.start('https://www.trictrac.net');

casper.then(function () {
    casper.fill('form', { // Handles the CSRF token transparently
        _username: casper.cli.get('email'),
        _password: ''+casper.cli.get('password') // conversion to string is mandatory, cf. CasperJS issue #1275
    }, /*submit=*/true);
    casper.waitWhileSelector('#signinReveal');
});

// Alternatively we could simply call https://www.trictrac.net/notifications once logged
casper.thenClick('[data-toggle="notification-dropdown"]', function () {
    casper.waitFor(function check() {
        return this.fetchText("#notification-dropdown").trim() !== 'Loading...';
    }, function then() {
        stderr.write(this.fetchText('#notification-dropdown').trim() + '\n');
    });
});

casper.run();
