// In Firefox Web Console
javascript:alert(document.lastModified) // last page update (can be current time if page has dynamic elements)

$$("#articleContent ul li").length

debugger // breakpoint for debugger

$._data($(elem).get(0), "events") // get events binded to 'elem'

(function(exports) {
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
JSON.stringify(obj) // pretty stringifier, an equivalent lib to this builtin is json.js

// Concat of many strings
[ 'aaa', 'bbb'... ].join('')
// Concat array2 in array1
Array.prototype.push.apply(array1, array2);
// Remove element
function RemoveArrayElement( array, element ) !!let (pos=array.lastIndexOf(element)) pos != -1 && array.splice(pos, 1);

+new Date() // milliseconds since epoch

'abcd'.match(/a(.*)/) // regexp, also new RegExp("string", 'igm') where g: global, m:multi-line i: ignore case
RegExp.$1 // 'bcd'

for ( let i in function(){ return [1,2,3] }() ) ...

function foo({ name:name, project:project}) { return [name, project] } // optional named args
var [n, p] = foo({ name:'soubok' }) // unwrapping multiple return values

// Handy functions
function toType(obj) {
    return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
}
function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n); // For 'ParseInt', ALWAYS specify the base !
}
function range(start, end) {
    var range_array=[];
    for (var i=start; i<end; ++i) {
        range_array.push(i);
    }
    return range_array;
}
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, nbr) {
            return typeof args[nbr] != 'undefined' ? args[nbr] : match;
        });
    };
}

// Watch propery changes
var o = { foo:42 };
o.watch('foo', function (id, oldval, newval) { ... });
o.foo = "42";
// Define getter
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

function Stack() { try { throw Error() } catch(ex) { return ex.stack } } // Display the current call stack
foo.toSource(2) // get function code source, with comments !

requestAnimationFrame > setInterval OR setTimeout // For smart animating, recommended by Mozilla


//~~//~~//~~//
// Tricks //
//~~//~~//
// Evaluate to 'fail'
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

// Sharp variable
var a = { titi:#1={}, toto:#1# };
a.titi === a.toto; // is: true
var a = { b:#1={ c:#1# } }
// a.b.c.c.c.c.c.c...

Print( 1000000000000000128 ); // prints 1000000000000000100

new, with // NEVER use them ! They're reserved keywords


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
let > var
array comprehension
generators

hex_md5('string') // crypt/md5.js

underscorejs.org // Functional prog lib
moment.js // parse, validate, manipulate, and display dates

npm install // Node Packaged Modules

var http = require('http');
http.createServer(function (req, res) {
  console.log('request recieved');
  console.log('url: ' + req.url);
  console.log('headers: ' + JSON.stringify(req.headers));
  res.writeHead(402, {'Content-Type': 'text/plain'});
  res.end('');
}).listen(8181, '127.0.0.1');
console.log('Server running at http://127.0.0.1:8181/');

var fs = require("fs"); // Node.js
fs.readFileSync('./input.txt').toString().split('\n').forEach(function (line) {
    console.log(line);
});
node-inspector & node --debug scriptFileName.js // http://stackoverflow.com/a/3944507/636849

JSHint, JSLint // static code analysis

http://qunitjs.com // Testing lib

// E4X is an official JavaScript standard that adds direct support for XML

Google Closure Compiler, Library & Linter
Google V8 // Open Source high perf JS engine written in C++. Features :
// - Hidden classes
// - Dynamic machine code generation
// - Profiler : d8 --prof script.js

// Languages that compile to JS:
CoffeeScript, TypeScript
Brython, RapydScript, Pyjamas, PythonJS // for Python

Esprima // ECMAScript parser
