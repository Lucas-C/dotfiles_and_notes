d3.select("css-selector").append("elem") // Also: selectAll

// Joins
.data(..) // return 3 virtual selections: enter(), update[no sub-method] & exit()

// Data stored in __data__ property

.text( "hello ")
.text( function (data_elem, index) { return "index = " + index + " data_elem = " + data_elem; } )
// "if the value passed to it (the Text Operator) is a function, then the function is evaluated for each __data__ element in order.
// And the functions result is used to set each element's text context "

var svgContainer = d3.select("body").append("svg").attr("width", 200).attr("height", 100);

.interpolate("<interpolation>")
// linear, step-before, step-after, basis (B-spline), basis-open, basis-closed, bundle (B-spline straightened), cardinal (Cardinal spline), cardinal-open, cardinal-closed, monotone (cubic interpolation)
