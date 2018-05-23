#!python2
# coding: utf-8
# DESCRIPTION: Replicates the behaviour of tweecode/twine/app.py "rebuild" functionnality without the need for wxPython.
#              This produces an output similar to the Twine 1 GUI app, but different from tweecode/twine/twee (e.g. it takes into account StorySettings)
# AUTHOR: Lucas Cimon
# REQUIRES: tweecode/twine in PYTHONPATH
# USAGE:
#   ./tws_to_html.py $tws_filepath $html_filepath
#   ./tws_to_html.py --use-relative-imgs-dir img/ $tws_filepath $html_filepath
import os, pickle, sys, tiddlywiki
from collections import namedtuple
from header import Header  # twine module


class TweeApp(object):
    NAME = 'tws_to_html.py'
    VERSION = '1.0'
    builtinTargetsPath = os.path.join(os.path.dirname(tiddlywiki.__file__), 'targets')
    def displayError(self, msg, **_):
        raise RuntimeError(msg)

def main(argv):
    if sys.argv[1] == '--use-relative-imgs-dir':
        relative_img_dir, twsFilepath, buildDestination = sys.argv[2:5]
    else:
        relative_img_dir = None
        twsFilepath, buildDestination = sys.argv[1:3]
    app = TweeApp()
    with open(twsFilepath, 'rb') as tws:
        state = pickle.load(tws)
    widgetDict = {widget['passage'].title: widget for widget in state['storyPanel']['widgets']}
    if relative_img_dir:
        for img in [w['passage'] for w in widgetDict.values() if w['passage'].tags == ['Twine.image']]:
            img_path = os.path.join(relative_img_dir, '{}.{}'.format(img.title, img.text[11:14]))
            if not os.path.exists(img_path):
                raise EnvironmentError('Relative image not found: {}'.format(img_path))
            img.text = img_path
    tw = build_tiddlywiki(widgetDict)
    storyFormat = state['target']
    header = Header.factory(storyFormat, os.path.join(app.builtinTargetsPath, storyFormat) + os.sep, app.builtinTargetsPath)
    with open(buildDestination, 'wb') as dest:
        dest.write(tw.toHtml(app, header=header,
                                  defaultName=widgetDict['StoryTitle']['passage'].text,
                                  metadata=state['metadata']).encode('utf-8-sig'))

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
    main(sys.argv)
