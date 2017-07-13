#!/usr/bin/python3

from pyparsing import CharsNotIn, Forward, Keyword, Literal, OneOrMore, Optional, QuotedString, Suppress, Token, White, Word, ZeroOrMore, delimitedList, nums, printables

class StopOnSuffix(Token): # inspired by CharsNotIn
    def __init__(self, suffixes):
        super().__init__()
        self.skipWhitespace = False
        self.suffixes = set(suffixes)
        self.name = self.__class__.__name__
        self.mayReturnEmpty = True
        self.mayIndexError = False

    def parseImpl(self, instring, loc, doActions=True):
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
Striked = Suppress(Literal('~~'))
Text = OneOrMore(Word(printables))

StyledText = Forward()
BoldText = (Bold + StyledText + Bold)('is_bold')
ItalicText = (Italic + StyledText + Italic)('is_italic')
StrikedText = (Striked + StyledText + Striked)('is_striked')
StyledText << (BoldText | ItalicText | StrikedText | StopOnSuffix(['**', '__', '~~', '](', '!icon=', '<!--', '(see:']))
StyledText.resultsName = 'text'
StyledText.saveAsList = True  # must be done at this point, not before
TextGrammar = StyledText | Text.setResultsName('text', listAllMatches=True)

Checkbox = (Literal('[') + (Literal('x')('is_checked') | White()) + Literal(']'))('has_checkbox')

Icon = Literal('!icon=') + Word(printables).setResultsName('icons', listAllMatches=True)

DestNodeText = QuotedString('"', escChar='\\')
See = Keyword('(see:') + delimitedList(DestNodeText, delim=',').setResultsName('see') + Literal(')')

XMLAttrs = Keyword('<!--') + OneOrMore(Word(printables), stopOn=Keyword('-->')).setResultsName('attrs', listAllMatches=True) + Keyword('-->')

Url = CharsNotIn(') ')('url')
ImgDimensions = Word(nums)('img_width') + Literal('x') + Word(nums)('img_height')
Link = Optional(Literal('!'))('is_img') + Literal('[') + TextGrammar + Literal('](') + Url + Optional(ImgDimensions) + Literal(')')

LineGrammar = Optional(Checkbox) + ZeroOrMore(Icon | XMLAttrs) + (Link | TextGrammar) + ZeroOrMore(Icon | XMLAttrs) + Optional(See)

if __name__ == '__main__':
    def test(text_line, text, url='', icons=(), attrs=(), is_bold=False, is_italic=False, is_striked=False, is_img=False, img_dims=None, has_checkbox=False, is_checked=False, see=''):
        parsed_line = LineGrammar.parseString(text_line, parseAll=True)
        print(parsed_line.dump())
        assert parsed_line.text[0].strip() == text, parsed_line.text
        assert bool(parsed_line.is_bold) == is_bold
        assert bool(parsed_line.is_italic) == is_italic
        assert bool(parsed_line.is_striked) == is_striked
        assert parsed_line.url == url
        assert bool(parsed_line.is_img) == is_img
        if img_dims or parsed_line.img_width or parsed_line.img_height:
            assert (int(parsed_line.img_width), int(parsed_line.img_height)) == img_dims
        assert bool(parsed_line.has_checkbox) == has_checkbox
        assert bool(parsed_line.is_checked) == is_checked
        assert tuple(parsed_line.icons) == icons
        parsed_attrs = tuple(attr for attrs in parsed_line.attrs for attr in attrs)
        assert parsed_attrs == attrs
        assert list(parsed_line.see) == list(see)
    test('[Framindmap](https://framindmap.org)', text='Framindmap', url='https://framindmap.org')
    test('![coucou](http://website.com/favicon.ico)', text='coucou', url='http://website.com/favicon.ico', is_img=True)
    test('![coucou](http://website.com/favicon.ico 600x0400)', text='coucou', url='http://website.com/favicon.ico', is_img=True, img_dims=(600, 400))
    test('!toto', text='!toto')
    test('Productivity   !icon=chart_bar <!-- fontStyle=";;#104f11;;;" bgColor="#d9b518" -->',
        text='Productivity', icons=('chart_bar',), attrs=('fontStyle=";;#104f11;;;"', 'bgColor="#d9b518"'))
    test('**toto**', text='toto', is_bold=True)
    test('__toto__', text='toto', is_italic=True)
    test('__**toto**__', text='toto', is_bold=True, is_italic=True)
    test('**__toto__**', text='toto', is_bold=True, is_italic=True)
    test('~~toto~~', text='toto', is_striked=True)
    test('toto !icon=ahoy', text='toto', icons=('ahoy',))
    test('!icon=A toto !icon=B', text='toto', icons=('A','B'))
    test('[ ] toto', text='toto', has_checkbox=True, is_checked=False)
    test('[x] toto', text='toto', has_checkbox=True, is_checked=True)
    test('toto (see: "a\\"","b,c")', text='toto', see=['a"','b,c'])
