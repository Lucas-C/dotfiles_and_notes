#!/usr/bin/python3

from pyparsing import CharsNotIn, Forward, Keyword, Literal, OneOrMore, Optional, Suppress, Token, Word, ZeroOrMore, basestring, printables

class StopOnSuffix(Token): # inspired by CharsNotIn
    def __init__( self, suffixes ):
        super().__init__()
        self.skipWhitespace = False
        self.suffixes = set(suffixes)
        self.name = self.__class__.__name__
        self.mayReturnEmpty = True
        self.mayIndexError = False

    def parseImpl( self, instring, loc, doActions=True ):
        if self._suffix_match(instring, loc):
            raise ParseException(instring, loc, '{} early stop : token starts with suffix'.format(self.name), self)
        start = loc
        maxlen = len(instring)
        loc += 1
        while loc < maxlen and not self._suffix_match(instring, loc):
            loc += 1
        return loc, instring[start:loc]

    def _suffix_match(self, instring, loc):
        for suffix in self.suffixes:
            suffix_length = len(suffix)
            if suffix == instring[loc:loc+suffix_length]:
                return True

Bold = Suppress(Literal('**'))
Italic = Suppress(Literal('__'))
Text = OneOrMore(Word(printables))

StyledText = Forward()
BoldText = (Bold + StyledText + Bold)('is_bold')
ItalicText = (Italic + StyledText + Italic)('is_italic')
StyledText << (BoldText | ItalicText | StopOnSuffix(['**', '__', '](', '!icon=', '<!--']))
StyledText.resultsName = 'text'
StyledText.saveAsList = True  # must be done at this point, not before
TextGrammar = StyledText | Text.setResultsName('text', listAllMatches=True)

Icon = Literal('!icon=') + Word(printables).setResultsName('icons', listAllMatches=True)

XmlCommentStart = Keyword('<!--')
XmlCommentEnd = Keyword('-->')
XMLAttrs = XmlCommentStart + OneOrMore(Word(printables), stopOn=XmlCommentEnd).setResultsName('attrs', listAllMatches=True) + XmlCommentEnd

Url = CharsNotIn(')')('url')
Link = Optional(Literal('!'))('is_img') + Literal('[') + TextGrammar + Literal('](') + Url + Literal(')')

LineGrammar = ZeroOrMore(Icon | XMLAttrs) + (Link | TextGrammar) + ZeroOrMore(Icon | XMLAttrs)

def test(text_line):
    parsed_line = LineGrammar.parseString(text_line, parseAll=True)
    print(parsed_line.dump())
test('toto')
test('[Framindmap](https://framindmap.org)')
test('![coucou](http://website.com/favicon.ico)')
test('!toto')
test('Productivity   !icon=chart_bar <!-- fontStyle=";;#104f11;;;" bgColor="#d9b518" -->')
test('**toto**')
test('__toto__')
test('__**toto**__')
test('**__toto__**')
test('toto !icon=ahoy')
test('!icon=A toto !icon=B')
