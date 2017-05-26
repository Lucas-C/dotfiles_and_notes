import re
from string import ascii_letters

WORD_CHARS = ascii_letters + 'çéâêîôûàèùëïü'


class KnownTagsExtractor():
    def __init__(self, tags):
        self.tag_words = {tag: _words(tag.lower()) for tag in tags}
        self.tags_regex = re.compile(r'\b(' + '|'.join(set(word.replace('++', r'\+\+') for words in self.tag_words.values() for word in words)) + r')\b')

    def find_tags(self, text):
        text = text.lower()
        for tag, words in self.tag_words.items():
            match = True
            for word in words:
                if not _text_contains_word(text, word):
                    match = False
                    break
            if match:
                yield tag

    def find_tags_re(self, text): # tested with http://sametmax.com/vue-jlavais-pas-vu/ : 20s instead of 3s :(
        matches = set(m.group() for m in re.finditer(self.tags_regex, text.lower()))
        for tag, words in self.tag_words.items():
            if all(word in matches for word in words):
                yield tag

def _words(tag):
    return tuple(word for word in tag.replace('_', ' ').replace('/', ' ').replace('&', ' ').replace(':', '').split(' ') if word != '')

def _text_contains_word(text, word):
    try:
        i = text.index(word)
        j = i + len(word)
        if (i == 0 or (text[i-1] not in WORD_CHARS)) and (j == len(text) or (text[j] not in WORD_CHARS)):
            return True
        return _text_contains_word(text[j:], word)
    except ValueError:
        return False
