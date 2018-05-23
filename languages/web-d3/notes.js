
// In Firefox Web Console
javascript:alert(document.lastModified) // last page update (can be current time if page has dynamic elements)
javascript:window.print()
document.body.contentEditable='true'; // makes everything editable (IE: document.designMode='on')

$$("#articleContent ul li").length

console.time('myTime') / console.timeEnd('myTime') // for quick benchmarks
console.table(array) // display array of objects as a nice table in browser console
console.memory // JS heap info

debugger // breakpoint for debugger
performance.timing // and performance.memory : useful debugging informations
console.profile('profileName') & console.profileEnd('profileName')

while (e.firstChild) { e.removeChild(e.firstChild); } >>faster>> e.innerHTML = ''

<script id='loadarea' type='text/javascript'></script>
document.getElementById('loadarea').src = '.../test.cgi?js';

Function.prototype.bind // set 'this' and/or partially apply arguments
// GOTCHAS:
o = {name: 'FOO', get_name: function () { return this.name; } }
o.get_name() // 'FOO'
var func = o.get_name;
func() // ''
o.get_name = o.get_name.bind({name: 'BAR'})
o.get_name() // 'BAR'
// + no way to found out if o.get_name is bounded or not !! (nor to what object it's bounded)

Object.freeze / Object.seal

Object.create > mutating .protoype // cf. https://github.com/mbostock/d3/issues/1805

.classList.add('myCssClass') / .classList.remove('myCssClass') / .classList.toggle('myCssClass')  // min IE version: 10
function addCSSRule(sheet, selector, rules, index) {
    if(sheet.addRule) { // slightly faster
        sheet.addRule(selector, rules, index /* default: -1*/);
    } else {
        sheet.insertRule(selector + "{" + rules + "}", index /* default: -1*/);
    }
}
addCSSRule(document.styleSheets[0], "header", "float: left");
function cssRules(){
    var rules = {};
    [].forEach.call(document.styleSheets, function (styleSheet) {
        [].forEach.call(styleSheet.cssRules, function (cssRule) {
            rules[cssRule.selectorText] = cssRule;
        });
    });
    return rules;
};
cssRules()['.class'].style.X = Y

$._data($(elem).get(0), "events") // get events binded to 'elem' in jQuery
tipsy // Facebook style tooltips for jQuery

format = function (string) { // Provide both {0} & {keyword} substitutions, '<C3><A0> la Python' - Alt: _.template
    var output = string,
        extra_args = [].slice.call(arguments, 1);
    if (extra_args.length === 1 && typeof extra_args[0] !== 'string' && !(extra_args[0] instanceof String)) {
        extra_args = extra_args[0];
    }
    for (var key in extra_args) {
        if (typeof extra_args[key] !== 'undefined') {
            output = output.replace(new RegExp('\\{' + key + '\\}', 'g'), extra_args[key]);
        }
    }
    return output;
}
extend = function () { // jQuery.extend equivalent
    for (var i = 1; i < arguments.length; i++) {
        for (var key in arguments[i]) { // include inherited properties
            arguments[0][key] = arguments[i][key];
        }
    }
    return arguments[0];
}
unique = function (array) { // Remove duplicates in an array, like jQuery.unique
    return array.filter(function (e, i, arr) {
        return arr.lastIndexOf(e) === i;
    });
}
encode_query_params = function (data, encode_function) {
    encode_function = encode_function || encodeURIComponent; // Default to UTF8, alt: 'escape' for latin1 / iso-8859-1 encoding : ç -> %E7 not %C3%A7
    return Object.keys(data).map(function(key) {
        return [key, data[key]].map(encode_function).join('=');
    }).join('&');
}
range = function (start, end) { // Alt: _.range
    var range_array=[];
    for (var i=start; i<end; ++i) {
        range_array.push(i);
    }
    return range_array;
}


var extra_args = [].slice.call(arguments, 1);
foo.bind(null, accumulator).apply(null, extra_args) // foo(accumulator, *arguments[1:])

madge > colony & dependo // AMD or CommonJS modules dependencies graphs
(function(exports) { // for modules, use CommonJS 'require'
    var private_name = 'protected_by_closure';
    var MyClass = function(name) {
        this.name = name;
    };
    exports.MyClass = MyClass; // exports == module 'this'
    User.prototype.toString = function() { // protoype => shared between all instances of that class
        return this.name + ' ' + this.private_name;
    };
})(this); // IIFE pattern: Immediately Invoked Function Expression

const TEXT = <> // const not supported by IE
multi
lines
text
</>.toString();
JSON.stringify(obj, null, 2) // pretty stringifier, an equivalent lib to this builtin is json.js

var args = [].slice.call(arguments); // arguments -> Array
[ 'aaa', 'bbb'... ].join('') // Concat of many strings
[].push.apply(array1, array2); // Concat array2 in array1, returns its length
function RemoveArrayElement( array, element ) !!let (pos=array.lastIndexOf(element)) pos != -1 && array.splice(pos, 1);

+new Date() // milliseconds since epoch

'abcd'.match(/a(.*)/) // regexp, also new RegExp("string", 'igm') where g: global, m:multi-line i: ignore case
RegExp.$1 // 'bcd'
/whatever/g.test() // ! STATEFUL ! no need for 'g' with .test() or use .exec/.match()
str.replace(new RegExp('\\{' + key + '\\}', 'g'), value);

execCommand('copy') // manual copy to clipboard, cf. http://blog.idleman.fr/snippet-27-javascript-copier-dans-le-presse-papier-sans-flash-et-fonctionne-sur-ie/

function foo({ name:name, project:project}) { return [name, project] } // optional named args
var [n, p] = foo({ name:'soubok' }) // unwrapping multiple return values

// Handy functions
function toType(obj) {
    return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
}
function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n); // For 'parseInt', ALWAYS specify the base !
}
+nbr # or ~~nbr or 0|nbr : poor man's parseInt with flooring

// Watch property changes
var o = { foo:42 };
o.watch('foo', function (id, oldval, newval) { ... });
document.location.watch('hash', console.trace)
o.foo = "42";
// Define getter - Alt: Object.defineProperty(window, "myVariable", { get: function () { ...
o.__defineGetter__('x', function(){ return 7 } ) // one can even o.__lookupGetter__
// default method called
o.__noSuchMethod__ = function(meth_name){...}

//!! NEVER USE '==' !   Still:
o.constructor === Object // true - Control typeof, instanceof
// => 'instanceof' does not work on primitive values (it returns 'false')
// Also, beware: typeof null === "object"
var a = { "abc" : 1 }
a[[[["abc"]]]] === a["abc"] // true

foo.call(newThis, arg1, arg2) || foo.apply(newThis, argsArray) // change current "this" in afunction call

with({ a:5 }) { function toto() { return a } } // local scope

try { ... } catch ( err if err instanceof ReferenceError ) { ... } finally {}
EvalError, RangeError, ReferenceError, SyntaxError, TypeError, URIError // Std error types
console.trace() // stack trace
new Error().stack // Current call stack, can be printed
arguments.callee.caller.toString()
foo.toSource(2) // get function code source, with comments !

requestAnimationFrame > setInterval OR setTimeout // For smart animating, recommended by Mozilla

// most portable way to get width / height:
height: function () {
    var boundingRect = document.documentElement.getBoundingClientRect(); // most portable standard function
    return boundingRect.bottom - boundingRect.top;
},
width: function () {
    var boundingRect = document.documentElement.getBoundingClientRect(); // most portable standard function
    return boundingRect.right - boundingRect.left;
}


//~~//~~//~~//
// Tricks //
//~~//~~//
// Evaluate to 'fail' - FROM: https://twitter.com/lagergren/statuses/337484475204255744
(![]+[])[+[]]+(![]+[])[+!+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]];

{} + [] // 0
[] + {} // [object Object]

'5' + 3 // 53
'5' - 3 // 2

(0 === -0) && (0 === +0) // positive/negative zeros just equal 0

if (new Boolean(false)) // not 'false' because this is an object wrapper !
// The only false values are NaN, false, 0, null, undefined, and ''.
// One can use 'Boolean' without 'new' to properly convert any value to its matching boolean value
// That's because calling primitive wrapper constructors without new returns primitive values

if ( false ) { var bar = 42; } // Will define bar with value "undefined" (only if using 'var')

// Vulnerability : redefining the Array constructor:
function Array() { alert("hi"); }
// this constructor is called whenever arrays are created:
var a = [ 43 ];

// Closure pitfall
var i = 42;
function foo() { return i }
i = "BOO";
foo() // "BOO", use 'let' to fix that

// Sharp variablie : obsolete, discouraged & non-standard
var a = { titi:#1={}, toto:#1# };
a.titi === a.toto; // is: true
var a = { b:#1={ c:#1# } }
// a.b.c.c.c.c.c.c...

Print( 1000000000000000128 ); // prints 1000000000000000100

new, with // NEVER use them as variables ! They're reserved keywords


//~\~\~\\
// LIBS \\
//~\~\~\~\\
"use strict";

// Find out JS version
<script language="javascript">var js_version="1.0"</script>
<script language="javascript1.1">var js_version="1.1"</script>
<script language="javascript1.2">var js_version="1.2"</script>
<script language="javascript1.3">var js_version="1.3"</script>
<script language="javascript1.4">var js_version="1.4"</script>
<script language="javascript1.5">var js_version="1.5"</script>
<script language="javascript1.6">var js_version="1.6"</script>

// Javascript 1.7
let > var // BUT DO NOT USE IT IN A BROWSER !! -> for(let i=0; i<10000; i++){console.log(typeof null =='undefined')}

array comprehension
generators
[a, b] = [b, a] // destructuring assignement
// Javascript 1.8
f = function(x) x*x // lambda notation with expression closure
Array.reduce

asm.js // static subset of JS, can be compiled ahead, include static typing
// Rarely hand-written: C++ -> LLVM bytecode -> asm.js

ParallelJS // .mapPar() .filterPar() .reducePar()

hex_md5('string') // crypt/md5.js
// davidshimjs/qrcodejs

lazy.js, lodash > underscore.js // Functional prog libs
Immutable // Facebook JS lib
moment.js > sugar.js // parse, validate, manipulate, and display dates

webpack, browserify, systemJs // module bundlers
npm install --loglevel verbose $pkg // Node Packaged Modules
npm view $pkg_name [dist.tarball] // get URL of a package tarball
npm shrinkwrap // locks down the versions of a package's dependencies

substack/minimist > substack/optimist // argument options parser - Alt: chevex/yargs, divarvel/cliparse-node, tj/commander.js

var Transform = require('stream').Transform,
    PassThrough = require('stream').PassThrough;
function makeStream(src) { // Alt: through2
  var res = new Transform();
  res._transform = function (chunk, encoding, callback) { callback() }
  res._flush = function (callback) {
    res.push(src)
    callback()
  }
  return res;
}

var http = require('http');
http.createServer(function (req, res) {
  console.log('request recieved');
  console.log('url: ' + req.url);
  console.log('headers: ' + JSON.stringify(req.headers));
  res.writeHead(402, {'Content-Type': 'text/plain'});
  res.end('');
}).listen(8181, '127.0.0.1');
console.log('Server running at http://127.0.0.1:8181/');
// Alt: npm install connect serve-static && node server.js # that contains:
var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname)).listen(8080);
// Alt: npm install http-server -g && http-server

yammer/circuit-breaker-js // Hystrix-like circuit breaker for JavaScript

var fs = require("fs"); // Node.js
fs.readFileSync('./input.txt').toString().split('\n').forEach(function (line) {
    console.log(line);
});

NODE_DEBUG=cluster,net,http,fs,tls,module,timers // http://www.juliengilli.com/2013/05/26/Using-Node.js-NODE_DEBUG-for-fun-and-profit/
node-inspector & node --debug scriptFileName.js // http://stackoverflow.com/a/3944507 - Browser -> $host:8080/debug?port=5858 - Need the following iptables rules:
// for chain in INPUT OUTPUT; do iptables -A $chain -p tcp -m tcp --dport 8080 -j ACCEPT; done
mdb // awesome-looking NodeJs debugger, by Joyent - Alt: http://stackoverflow.com/questions/1911015/how-do-i-debug-node-js-applications/16512303#16512303

var util = require('util');
log(util.inspect(process._getActiveRequests()));
log(util.inspect(process._getActiveHandles()));

plato // source code visualization, static analysis, and complexity tool
FGRibreau/check-build // includes:
    eslint --fix > JSHint > JSLint > gjslint --disable 0001,0011,0110,0120,0121 -r src/ -e .flowlibs // static code analysis
    JSCS // code style checker
    jsinspect // check for code duplication
    buddy.js // detect magic numbers
    depcheck : "how each dependency is used, which dependencies are useless, and which dependencies are missing from package.json" // Also: npm outdated
    Nsp // detect security vulnerabilities

nyc (instanbul-based, inc. coverage) > karma-runner/karma > JsTestDriver > Qunit // Testing libs
Sinon.js // test spies, stubs and mocks - framwork agnostic & no dependencies
Vows.js // asynchronous BDD for Node.js
admc/wd // node.js client for webdriver/selenium 2
Protractor // Framework for Selenium testing of AngularJS apps
proxyquire // easily overre modules dependencies during tests
nodemon // watch files in current directory, and restart a script on any change detected

var logs = driver.manage().logs(), // driver is a selenium-webdriver instance
    fetchLogsPromises = _.map(webdriver.logging.Type, logs.get.bind(logs)); // !! native .map does not work here - there are 5 logging.Type defined here: https://github.com/SeleniumHQ/selenium/blob/master/javascript/webdriver/logging.js#L234
Promise.all(fetchLogsPromises).then(function (fetchedLogs) {
    fetchedLogs.forEach(function (logs, logIndex) {
        logs.forEach(function (log) {
            console.log('\x1b[3%sm%s [%s] %s\x1b[0m', logIndex + 1, new Date(log.timestamp), log.level.name, log.message);
        });
    });
});

// E4X is an official JavaScript standard that adds direct support for XML

Google Closure Compiler, Library & Linter //  Markdown Optimize JS code
Google V8 // Open Source high perf JS engine written in C++. Features :
// - Hidden classes
// - Dynamic machine code generation
// - Profiler : d8 --prof script.js

// Languages that compile to JS:
CoffeeScript // Compared to ES6 ? -> discourse point of view: https://meta.discourse.org/t/is-it-better-for-discourse-to-use-javascript-or-coffeescript/3153/2
TypeScript, Flow // provide static type checking
Brython, RapydScript, Pyjamas, PythonJS // for Python

Esprima // ECMAScript parser

CommonMark // "Standard" Markdown https://github.com/jgm/stmd/blob/master/js/stmd.js
cemerick/jsdifflib

sweetalert // pretty replacement for 'alert'

ywng/Progressive-News-Cloud, jasondavies/d3-cloud // word clouds generators

esprima // JS AST manipulation: parsing, rewrite, refactoring ; + escodegen for code generation - Also: substack/node-falafel based on acorn

Sencha Ext JS // framework for building feature-rich cross-platform web applications targeting desktop, tablets, and smartphones - Commercial / GPLv3 license

Matt-Esch/virtual-dom & anthonyshort/deku
"Manual DOM manipulation is messy and keeping track of the previous DOM state is hard. A solution to this problem is to write your code as if you were recreating
the entire DOM whenever state changes. Of course, if you actually recreated the entire DOM every time your application state changed, your app would be very slow
and your input fields would lose focus."


/********************************
* Progressive/lazy image loading
********************************/
Some criterias to consider:
- 3 main strategies:
  * preloading images appearing after the page "fold"
  * lazy loading : load images only as needed, when the user scroll
  * progressive images: display a low-res image first, aka LQIP = Low Quality Image Placeholder
- use a placeholder image (e.g. a base64 very small / spinner gif) or a low-res version (as Facebook/Medium do) ?
- combine with interlaced GIF/PNG or progressive JPEG ?
- support for <noscript> ? Notably: if JS is disabled, won't there by a CSS styling issue if there are 2 images ?


Some solutions as of summer 2017:
- [Lazy Load XT](http://ressio.github.io/lazy-load-xt/demo/index.htm) & [jQuery Lazy](http://jquery.eisbehr.de/lazy/): jQuery plugins, lazy load images on scroll, with fade-in or spinner effect, support <noscript>
- [bLazy.js](http://dinbror.dk/blazy/)
- [progressively](https://thinker3197.github.io/progressively/) : simple, seems to require a <figure>
- [lazyload](http://www.andreaverlicchi.eu/lazyload/) : require width/height but support scrolling pannels
- [lazysizes](https://github.com/aFarkas/lazysizes) : the basic noscript pattern relies on Modernizer `.no-js` CSS class to handle <noscript>
But the plugin works great ! Demo:

    <head>
    <style>
    .intrinsic {
        position: relative;
        padding-bottom: 75%;
        height: 0;
    }
    </style>
    <script src="lazysizes.min.js" async=""></script>
    <script src="lazysizes.noscript.min.js" async=""></script>
    </head>
    <body>
    <div class="intrinsic lazyload" data-noscript=""><noscript>
        <img src="https://farm5.staticflickr.com/4094/4859138371_9713d4396e_b.jpg">
    </noscript></div>
    ...
    </body>

/*******
 Perfs
*******/
Google PageSpeed
GT Metrix
Webpagetest
BoomerangJS
