//~~//~~//~~//~~//
// JavaScript //
//~~//~~//~~//
const MY_CONST = 0; // Not supported by IE

// Concat array2 in array1
Array.prototype.push.apply(array1, array2);

// Evaluate to 'fail'
(![]+[])[+[]]+(![]+[])[+!+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]];

// Redefining the Array constructor:
function Array() { alert("hi"); }
// this constructor is called whenever arrays are created:
var a = [ 43 ];

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

// Functional prog lib
http://underscorejs.org

// Testing libs
http://phantomjs.org
http://qunitjs.com

// V8 : Open Source high perf JS engine written in C++. Features :
// - Hidden classes
// - Dynamic machine code generation
// - Profiler : d8 --prof script.js

