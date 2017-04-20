#!/usr/bin/python3

#cf. http://pyparsing.wikispaces.com/share/view/81099063

from pyparsing import Forward, Literal, OneOrMore, ParseException, Suppress, Token, Word, basestring, printables

Bold = Suppress(Literal('**'))
Italic = Suppress(Literal('__'))
Text = OneOrMore(Word(printables))

def test(msg):
    parsed = TextGrammar.parseString(msg, parseAll=True)
    #print(parsed.dump())
    print('msg: {} => tokens={} is_bold={} is_italic={}'.format(msg, parsed.text, bool(parsed.is_bold), bool(parsed.is_italic)))


#------------------------------------------------------------------------------
# 1st implementation

class StopOnSuffix(Token): # cannot be a TokenConverter because .postParse does not alter loc
    def __init__( self, token_matcher, suffixes ):
        super(StopOnSuffix,self).__init__()
        self.name = 'StopOnSuffix'
        self.mayReturnEmpty = token_matcher.mayReturnEmpty
        self.mayIndexError = token_matcher.mayIndexError
        self.saveAsList = token_matcher.saveAsList
        self.token_matcher = token_matcher
        self.suffixes = set(suffixes)
    def parseImpl( self, instring, loc, doActions=True ):
        loc, tokens = self.token_matcher.parseImpl(instring, loc, doActions)
        try:
            suffix, match_index = next((suffix, i) for i, match in enumerate(tokens)
                                                   for suffix in self.suffixes if suffix in match)
            match = tokens[match_index]
            match_trun_len = match.index(suffix)
            if match_trun_len > 0:
                loc -= len(match) - match_trun_len + sum(map(len, tokens[match_index+1:])) # this is WRONG: we forbid whitespaces and have NO WAY to know how many were skipped :(
                match = match[:match_trun_len]
                tokens = tokens[:match_index] + [match]
            else:
                loc -= sum(map(len, tokens[match_index:])) # ditto: WRONG
                tokens = tokens[:match_index]
        except StopIteration:
            pass
        return loc, tokens

StyledText = Forward()
BoldText = Bold + StopOnSuffix(StyledText, ['**'])('is_bold') + Bold
ItalicText = Italic + StopOnSuffix(StyledText, ['__'])('is_italic') + Italic
StyledText << (BoldText | ItalicText | Text)
StyledText.resultsName = 'text'
StyledText.saveAsList = True  # must be done at this point, not before
TextGrammar = StyledText

test('**a text**')
test('**__a text__**')
test('__**a text**__')
test('__**a text__**')
test('a **text**')

#------------------------------------------------------------------------------
# 2nd implementation

class StopOnSuffix(Token): # inspired by CharsNotIn
    def __init__( self, suffixes ):
        super(StopOnSuffix,self).__init__()
        self.skipWhitespace = False
        self.suffixes = set(suffixes)
        self.name = 'StopOnSuffix'
        self.mayReturnEmpty = True
        self.mayIndexError = False
        if not all(len(s) == len(suffixes[0]) for s in suffixes[1:]):
            raise ValueError('Suffixes do not all share the same length')

    def parseImpl( self, instring, loc, doActions=True ):
        suffixes = self.suffixes
        suffixLength = len(list(self.suffixes)[0])
        maxlen = len(instring)
        if instring[loc:loc+suffixLength] in self.suffixes:
            raise ParseException(instring, loc, 'StopOnSuffix early stop : token starts with suffix', self)
        start = loc
        loc += 1
        while loc < maxlen and (instring[loc:loc+suffixLength] not in suffixes):
            loc += 1
        return loc, instring[start:loc]

StyledText = Forward()
BoldText = (Bold + StyledText + Bold)('is_bold')
ItalicText = (Italic + StyledText + Italic)('is_italic')
StyledText << (BoldText | ItalicText | StopOnSuffix(['**', '__']))
StyledText.resultsName = 'text'
StyledText.saveAsList = True  # must be done at this point, not before
TextGrammar = StyledText | Text.setResultsName('text', listAllMatches=True)

test('**a text**')
test('**__a text__**')
test('__**a text**__')
test('__**a text__**')
test('a **text**') # crashes because pyparsing raise when parseAll=True on StyledText matching only 2 chars, whereas Text would have matched :(

