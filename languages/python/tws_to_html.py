#!python2
# coding: utf-8
# DESCRIPTION: Replicates the behaviour of tweecode/twine/app.py "rebuild" functionnality without the need for wxPython.
#              This produces an output similar to the Twine 1 GUI app, but different from tweecode/twine/twee (e.g. it takes into account StorySettings)
# AUTHOR: Lucas Cimon
# REQUIRES: tweecode/twine in PYTHONPATH
# USAGE:
#   ./tws_to_html.py [--use-relative-imgs-dir img/] [--override-js-files js/{}.min.js] $tws_filepath $html_filepath
import argparse, os, pickle, tiddlywiki
from collections import namedtuple
from header import Header  # twine module


class TweeApp(object):
    NAME = 'tws_to_html.py'
    VERSION = '1.0'
    builtinTargetsPath = os.path.join(os.path.dirname(tiddlywiki.__file__), 'targets')
    def displayError(self, msg, **_):
        raise RuntimeError(msg)

def main():
    args = parse_args()
    app = TweeApp()
    with open(args.twsFilepath, 'rb') as tws:
        state = pickle.load(tws)
    widgetDict = {widget['passage'].title: widget for widget in state['storyPanel']['widgets']}
    if args.css_passage_from_file:
        if 'css' not in widgetDict:
            raise NotImplementedError('An existing "css" passage to update is currently required')
        with open(args.css_passage_from_file, 'rb') as css:
            widgetDict['css']['passage'].text = css.read().decode('utf8')
    if args.override_js_files:
        for script in [w['passage'] for w in widgetDict.values() if w['passage'].tags == ['script']]:
            script_path = args.override_js_files.format(script.title)
            if not os.path.exists(script_path):
                print 'Cannot override script, JS file not found: {}'.format(script_path)
                continue
            with open(script_path) as script_file:
                script.text = script_file.read()
    if args.use_relative_imgs_dir:
        for img in [w['passage'] for w in widgetDict.values() if w['passage'].tags == ['Twine.image']]:
            img_path = os.path.join(args.use_relative_imgs_dir, '{}.{}'.format(img.title, img.text[11:14]))
            if not os.path.exists(img_path):
                raise EnvironmentError('Relative image not found: {}'.format(img_path))
            img.text = img_path
    tw = build_tiddlywiki(widgetDict)
    storyFormat = state['target']
    header = Header.factory(storyFormat, os.path.join(app.builtinTargetsPath, storyFormat) + os.sep, app.builtinTargetsPath)
    with open(args.buildDestination, 'wb') as dest:
        dest.write(tw.toHtml(app, header=header,
                                  defaultName=widgetDict['StoryTitle']['passage'].text,
                                  metadata=state['metadata']).encode('utf-8-sig'))

def parse_args():
    parser = argparse.ArgumentParser(description='Export Twine 1 .tws to .html', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--use-relative-imgs-dir')
    parser.add_argument('--override-js-files')
    parser.add_argument('--css-passage-from-file')
    parser.add_argument('twsFilepath')
    parser.add_argument('buildDestination')
    return parser.parse_args()

def build_tiddlywiki(widgetDict):
    tw = tiddlywiki.TiddlyWiki()
    for widget in widgetDict.values():
        passage = widget['passage']
        if passage.title == 'StoryIncludes':
            raise NotImplementedError('"StoryIncludes" is not supported at the moment')
        if tiddlywiki.TiddlyWiki.NOINCLUDE_TAGS.isdisjoint(passage.tags):
            passage.pos = widget['pos']
            tw.addTiddler(passage)
    if 'StorySettings' in widgetDict:
        for line in widgetDict['StorySettings']['passage'].text.splitlines():
            if ':' in line:
                (skey, svalue) = line.split(':')
                skey = skey.strip().lower()
                svalue = svalue.strip()
                tw.storysettings[skey] = svalue
    return tw


if __name__ == '__main__':
    main()
