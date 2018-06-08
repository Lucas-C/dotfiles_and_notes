#!python2
# coding: utf-8
# AUTHOR: Lucas Cimon
# REQUIRES: polib and optionnally colorama
# USAGE:
#   ./twine1_localizer.py po_from_tws     the-temple-of-no.tws l10n/en-US.po
#   ./twine1_localizer.py diff_tws_and_po the-temple-of-no.tws l10n/en-US.po
#   ./twine1_localizer.py translate       the-temple-of-no.tws l10n/fr-FR.po the-temple-of-no_fr.tws
import argparse, difflib, pickle, polib, re, sys
try:
    from colorama import Fore, Style, init
    init()  # for Windows
except ImportError:  # fallback so that the imported classes always exist
    class ColorFallback():
        __getattr__ = lambda self, name: ''
    Fore = Style = ColorFallback()


def main():
    args = parse_args()
    args.func(args)

def parse_args():
    parser = argparse.ArgumentParser(description='Manage Twine 1 localization', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()
    extract_po = subparsers.add_parser('po_from_tws', help='Extract all the msgid / msgstr strings from a .tws file into a .po')
    extract_po.add_argument('tws_filepath')
    extract_po.add_argument('out_po_filepath')
    extract_po.set_defaults(func=po_from_tws)
    po_merger = subparsers.add_parser('translate', help='Apply the translated strings of a .po file to a .tws file to localize it')
    po_merger.add_argument('tws_filepath')
    po_merger.add_argument('po_filepath')
    po_merger.add_argument('out_tws_filepath')
    po_merger.set_defaults(func=translate)
    diff = subparsers.add_parser('diff_tws_and_po', help='Display a diff of all text differences between a .tws and a .po,'
                                                         'in order to detect i18n changes in the upstream Twine story')
    diff.add_argument('tws_filepath')
    diff.add_argument('po_filepath')
    diff.set_defaults(func=diff_tws_and_po)
    return parser.parse_args()

def po_from_tws(args):
    tws = load_tws(args.tws_filepath)
    po = polib.POFile()
    po.metadata = {
        'Content-Type': 'text/plain; charset=utf-8',
    }
    for tiddler in tws['storyPanel']['widgets']:
        passage = tiddler['passage']
        if passage.tags != ['Twine.image'] and passage.text:
            po.append(polib.POEntry(
                msgid=passage.title,
                msgstr=passage.text,
            ))
    po.save(args.out_po_filepath)

def translate(args):
    tws = load_tws(args.tws_filepath)
    po = polib.pofile(args.po_filepath)
    translations = {entry.msgid: entry for entry in po.translated_entries()}
    for tiddler in tws['storyPanel']['widgets']:
        passage = tiddler['passage']
        if passage.title in translations:
            translation = translations[passage.title]
            passage.text = translation.msgstr
            for match in re.findall(r'\[\[[^]|]+\]\]', passage.text):
                print >>sys.stderr, Fore.RED + u'Untranslated link in passage "{}" starting on the .po line {} : {}'.format(passage.title, translation.linenum, match).encode('utf8', 'replace') + Fore.RESET
        elif passage.text and passage.tags != ['Twine.image']:
            print >>sys.stderr, 'No traduction found for', passage.title
    dump_tws(tws, args.out_tws_filepath)

def diff_tws_and_po(args):
    tws = load_tws(args.tws_filepath)
    po = polib.pofile(args.po_filepath)
    translations = {entry.msgid: entry.msgstr for entry in po.translated_entries()}
    for tiddler in tws['storyPanel']['widgets']:
        passage = tiddler['passage']
        if passage.tags == ['Twine.image'] or not passage.text:
            continue
        if passage.title not in translations:
            print passage.title + ' not translated'
            continue
        translated_text = translations[passage.title]
        diff = list(color_diff(difflib.ndiff(translated_text.splitlines(), passage.text.splitlines())))
        if diff:
            print '\n'.join(diff)
            print Style.BRIGHT + 'diff ' + passage.title + Style.NORMAL

def dump_tws(tws, tws_filepath):
    with open(tws_filepath, 'wb') as f:
        pickle.dump(tws, f)

def load_tws(tws_filepath):
    with open(tws_filepath, 'rb') as f:
        return pickle.load(f)

def color_diff(diff):
    'Ignore lines with no changes'
    for line in diff:
        if line.startswith('+'):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith('-'):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith('^'):
            yield Fore.BLUE + line + Fore.RESET


if __name__ == '__main__':
    main()
