// USAGE: firefox imacros://run/?m=script.js
// Docs: http://wiki.imacros.net/iMacros_for_Firefox#Javascript_Scripting_Interface
// It has a very useful 'recording' mode

const IMACRO = 'CODE:\n\
SET !TIMEOUT_STEP 0\n\
TAB T=1
URL GOTO=https://mywebsite.com/page?action={{var1}}\n\
TAG POS=1 TYPE=INPUT:CHECKBOX FORM=ID:modify ATTR=NAME:checkbox_{{var2}} CONTENT=YES\n\
TAG POS=1 TYPE=INPUT:SUBMIT FORM=ID:modify ATTR=*\n';

const VALUES = ["A", "B", "C"];

for(var iVal = 0; iVal < VALUES.length; iVal++){
    for(var n = 0; n < 10; n++){
        var value = VALUES[iVal];
        iimDisplay("var1:" + value + " | var2: " + n)
        iimSet("var1", value);
        iimSet("var2", n);
        var return_code = iimPlay(IMACRO);
        iimDisplay("Return code: " + return_code + " - Error: " + iimGetErrorText());
    }
}
