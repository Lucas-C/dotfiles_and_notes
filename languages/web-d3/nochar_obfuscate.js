(function() {
    'use strict';
    var ALPHANUMERICS_MIN = '0123456789abcdefghijklmnopqrstuvwxyz'.split(''),
    ALPHANUMERICS_MAX = [].concat(ALPHANUMERICS_MIN, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'.split('')),
    ALIAS = {},
    CLEARTEXT_HEADER = [
        // Defining some power of 2 constants
        (ALIAS.cst4            = '_4', 'cst4 = ONE + ONE + ONE + ONE,'),
        (ALIAS.cst8            = '_5', 'cst8 = cst4 + cst4,'),
        (ALIAS.cst16           = '_6', 'cst16 = cst8 + cst8,'),
        // Building the string 'test' and stringifying the Regex.test function
        (ALIAS.tmp_true_str    = '_1', 'tmp_true_str = TRUE_STR,'),
        (ALIAS.tmp3            = '_2', 'tmp3 = ONE + ONE + ONE,'),
        (ALIAS.t               = '_3', 't = tmp_true_str[SINGLE_ZERO],'),
        (ALIAS.test_str        = '_1', 'test_str = t + tmp_true_str[tmp3] + (FALSE_STR)[tmp3] + t,'),
        (ALIAS.func_test_str   = '_3', 'func_test_str = /,/[test_str]+[],'),
        // Extracting the letters 'co' from 'function test() { ... }'
        (ALIAS.tmp26           = '_1', 'tmp26 = cst16 + cst8 + ONE + ONE,'),
        (ALIAS.co              = '_1', 'co = func_test_str[tmp3] + func_test_str[cst4 + ONE + ONE],'),
        // Building the string 'constructor' and stringifying the String function
        (ALIAS.tmp0            = '_2', 'tmp0 = SINGLE_ZERO,'),
        (ALIAS.tmp1            = '_3', 'tmp1 = SINGLE_ONE,'),
        (ALIAS.cstctor_str     = '_2', 'cstctor_str = co[tmp0] + co[tmp1] + (UNDEFINED_STR)[tmp1] + (FALSE_STR)[ONE + ONE + tmp1] + (TRUE_STR)[tmp0] + (TRUE_STR)[tmp1] + (UNDEFINED_STR)[tmp0] + co[tmp0] + (TRUE_STR)[tmp0] + co[tmp1] + (TRUE_STR)[tmp1],'),
        (ALIAS.func_string_str = '_3', 'func_string_str = cstctor_str[cstctor_str]+[],'),
        // Building the string 'toString' from 'function String() { ... }'
        (ALIAS.tmp2            = '_2', 'tmp2 = ONE + ONE,'),
        (ALIAS.tostring_str    = '_1', 'tostring_str = (TRUE_STR)[SINGLE_ZERO] + co[SINGLE_ONE] + func_string_str[cst8 + ONE] + func_string_str[cst8 + tmp2] + func_string_str[cst8 + tmp2 + ONE] + func_string_str[cst8 + cst4] + func_string_str[cst8 + cst4 + ONE] + func_string_str[cst8 + cst4 + tmp2],'),
        // Defining the very useful constant 36
        (ALIAS.cst36           = '_2', 'cst36 = cst16 + cst16 + cst4,'),
    ].join('\n'),
    VAR_REPLACEMENTS = [
        { // First pass: Named constant tricks
            SINGLE_ZERO: '+[]', // if not combined in any operation, require a '+' prefix
            FALSE_STR: '![]+[]',
            ONE: '!+[]',
            SINGLE_ONE: '+!+[]', // if not combined in any operation, require a '+' prefix
            TRUE_STR: '!+[]+[]',
            UNDEFINED_STR: '[][[]]+[]',
        },
        ALIAS, // Second pass: Variable aliases
        { // Third pass: Unicode obfuscators for every variable register
            _1: 'ꓹ',
            _2: 'ǃ',
            _3: 'ᚐ',
            _4: 'ｰ',
            _5: 'ߺ',
            _6: 'ǀ',
        }
    ],
    replace_var = function (string, var_name, var_replacement) {
        return string.replace(new RegExp(var_name, 'gm'), function (match, offset, string) {
            var prev_char = (offset === 0) ? ' ' : string[offset - 1],
                next_char = (offset === string.length) ? ' ' : string[offset + match.length];
            if (ALPHANUMERICS_MAX.indexOf(prev_char) !== -1 || ALPHANUMERICS_MAX.indexOf(next_char) !== -1) {
                return match;
            } else {
                return var_replacement;
            }
        });
    },
    get_binary_terms_str = function (integer) {
        var output = 'SINGLE_ZERO',
            i = 0;
        while (integer) {
            if (integer % 2) {
                if (i == 0) {
                    output = '';
                } else {
                    output += ' + ';
                }
                if (i === 0) {
                    output += 'ONE';
                } else if (i === 1) {
                    output += 'ONE + ONE';
                } else if (i === 5) {
                    output += 'cst16 + cst16';
                } else {
                    output += 'cst' + (1 << i);
                }
            }
            integer = ~~(integer / 2); // euclidean division
            i++;
        }
        return output;
    },
    nochar = function (original_text, debug) {
        var output = CLEARTEXT_HEADER;
        for (var char_i = 0; char_i < original_text.length; char_i++) {
            var character = original_text[char_i];
            if (char_i !== 0) { output += '+'; }
            if (character === ' ') {
                output += 'func_string_str[cst8]';
                continue;
            } else if (character === ')') {
                output += 'func_string_str[cst16]';
                continue;
            }
            var char_as_int = ALPHANUMERICS_MAX.indexOf(character);
            if (char_as_int === -1) {
                throw new Error('Cannot encode character: ' + character);
            }
            var char_as_int_binary_terms_str = get_binary_terms_str(char_as_int);
            if (char_as_int < 10) {
                output += '(' + char_as_int_binary_terms_str + ')';
            } else {
                output += '(' + char_as_int_binary_terms_str + ')[tostring_str](cst36)';
            }
        }
        if (debug) { console.log(output); }
        for (var subst_i in VAR_REPLACEMENTS) {
            var var_substs = VAR_REPLACEMENTS[subst_i];
            for (var var_name in var_substs) {
                output = replace_var(output, var_name, var_substs[var_name]);
            }
            if (debug) { console.log(output); }
        }
        output = output.replace(/( |\n)/g, '');
        output.split('').forEach(function(character) {
            if (ALPHANUMERICS_MAX.indexOf(character) !== -1 || character === ' ') {
                throw new Error('The obfuscator failed to remove all alphanumeric characters: a "'
                    + character + '" remains:\n' + output);
            }
        });
        return output;
    },
    generate_chars_frequency_table = function (string) {
        var chars_count = {};
        nochar_output.split('').forEach(function(character) {
            chars_count[character] = (chars_count[character] || 0) + 1;
        });
        var chars_freq = Object.keys(chars_count).map(function (character) {
            return [character, chars_count[character]];
        });
        chars_freq.sort(function (a, b) { return a[1] - b[1]; });
        return chars_freq;
    },
    input = 'embauchez moi 8)',
    nochar_output = nochar(input),
    output_chars_freq = generate_chars_frequency_table(nochar_output),
    console.log([nochar_output,
        (0, eval)(nochar_output),
        'Length: ' + nochar_output.length,
        'There are ' + output_chars_freq.length + ' different characters in the output: ' + JSON.stringify(output_chars_freq),
    ].join('\n'));
})();
