<!-- To update this Table Of Contents:
    markdown-toc --indent "    " --maxdepth 3 -i DiagramsToolsAndRhetoric.md
-->

<!-- toc -->

- [Tools](#tools)
    * [Font effects](#font-effects)
    * [Markdown](#markdown)
    * [API specs : Open API, Swagger, API Blueprint, RAML...](#api-specs--open-api-swagger-api-blueprint-raml)
- [Diagrams](#diagrams)
    * [Word / tag clouds](#word--tag-clouds)
    * [UML](#uml)
    * [Sequence diagrams](#sequence-diagrams)
    * [Histograms](#histograms)
- [Command-line tips & tricks for demos](#command-line-tips--tricks-for-demos)
- [How to give presentations](#how-to-give-presentations)
    * [Benjamin G. advices](#benjamin-g-advices)
- [Rhetoric](#rhetoric)

<!-- tocstop -->

# Tools

- [Reveal.js](https://revealjs.com) & [Impress.js](https://github.com/impress/impress.js/) & [DZSlides](http://paulrouget.com/dzslides/) & [Eagle.js](https://github.com/Zulko/eagle.js)
    * extra Reveal.js themes : [by jefBinomed aka JF Garreau](https://github.com/binomed/binomed_docs/tree/master/Prez)
    * WebComponent to hightlight parts of the screen, like code: https://github.com/binomed/mask-highlighter
    * let audience vote during your presentation through SMS (or an online form) and display graphs: [Choose Your Own Adventure Presentations with Python & WebSockets](https://www.twilio.com/blog/2014/11/choose-your-own-adventure-presentations-with-reveal-js-python-and-websockets.html)
- [MathJax JS](https://www.mathjax.org)
- [pandoc](http://pandoc.org) : swiss-army knife that can convert documents in Markdown, reStructuredText, textile, HTML, DocBook, LaTeX, MediaWiki markup, TWiki markup, OPML, Emacs Org-Mode, Txt2Tags, Microsoft Word docx, LibreOffice ODT, EPUB...
- [JupyterLab](https://jupyter.org) : a web-based interactive development environment for Jupyter notebooks, code, and data

## Font effects
- [flamingtext](https://flamingtext.fr)

## Markdown

- `md2html` (NodeJS, based on `markdown-it` that implements CommonMark) cf. [my custom script](https://github.com/Lucas-C/linux_configuration/blob/master/bin/md2html.js)
- [markdown-toc](https://github.com/jonschlinkert/markdown-toc) : generate a markdown table of contents for READMEs (NodeJS)
There are many alternatives: in [bash](https://github.com/ekalinin/github-markdown-toc), [Python](https://github.com/rasbt/markdown-toclify)
- [grip](https://github.com/joeyespo/grip) : preview GitHub Markdown files like READMEs (Python), interactively on localhost or as a single HTML `--export`

Nice HTML collapsible panel: [`<details>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details)

To "anchorify" titles as Github does:
```javascript
['h2', 'h3'].forEach(function (selector) {
    document.querySelectorAll(selector).forEach(function (title) {
        if (!title.id) { title.id = title.textContent; }
        var a = document.createElement('a');
        a.href = document.location + '#' + title.id;
        a['aria-hidden'] = true;
        a.style.float = 'left';
        a.style['padding-right'] = '4px';
        a.style['margin-left'] = '-20px';
        a.style['line-height'] = 1;
        title.appendChild(a);
        var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('aria-hidden', true);
        svg.setAttribute('height', 16);
        svg.setAttribute('width', 16);
        svg.setAttribute('viewBox', '0 0 16 16');
        svg.style.color = '#1b1f23';
        svg.style['vertical-align'] = 'middle';
        svg.style.visibility = 'hidden';
        a.appendChild(svg);
        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttributeNS(null, 'fill-rule', 'evenodd');
        path.setAttributeNS(null, 'd', 'M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z');
        svg.appendChild(path);
        title.onmouseover = function () { this.getElementsByTagName('svg')[0].style.visibility = 'visible'; };
        title.onmouseout = function () { this.getElementsByTagName('svg')[0].style.visibility = 'hidden'; };
    });
});
```

## API specs : Open API, Swagger, API Blueprint, RAML...
Conversion tools: https://blog.codeship.com/documenting-microservices/#conversion


# Diagrams

- [Diagrams](https://diagrams.mingrammer.com/docs/getting-started/examples) : cloud system architectures in Python code
- [knsv/mermaid](https://github.com/knsv/mermaid) : graphs, GANTT diagrams and flowcharts from markdown-like syntax (Javascript, requires to embed `mermaid.css` & `mermaid.min.js`)
  Now support by GitHub!
- [asciiflow](http://asciiflow.com/#Draw) : online + OSS (Javascript) -> https://github.com/lewish/asciiflow2
- [mapio/GraphvizAnim](https://github.com/mapio/GraphvizAnim) : animated graph visualizations, based on graphviz (Python)
- [draw.io](https://www.draw.io) : diagrams stored as XML, online editor, OSS (Java) -> https://github.com/jgraph/draw.io
  It has a "scribble mode": [Introducing draw.io’s new sketch feature](https://drawio-app.com/introducing-draw-ios-new-sketch-feature/)
  Can be used for [floorplans](https://www.drawio.com/blog/floorplans)
- [kroki](https://kroki.io) : HTTP API to create diagrams from textual descriptions, with support for BlockDiag (BlockDiag, SeqDiag, ActDiag, NwDiag, PacketDiag, RackDiag), BPMN, Bytefield, C4 (with PlantUML), Ditaa, Erd, Excalidraw, GraphViz, Mermaid, Nomnoml, Pikchr, PlantUML, SvgBob, UMLet, Vega, Vega-Lite, WaveDrom...
- [ditaa](http://ditaa.sourceforge.net/) : ascii-art to images (Java) -> ne supporte pas les accents :(
- [blampe/goat](https://github.com/blampe/goat) : render ASCII art as SVG diagrams (Go)
- [Diagon](https://github.com/ArthurSonzogni/Diagon) : Markdown-style expression to ASCII-art - C++ with CLI & web interface
- [ivanceras/svgbobrus](https://github.com/ivanceras/svgbobrus) : convert ascii diagram scribbles into SVG (Rust)
- [gliffy](https://www.gliffy.com/examples/) : online, proprietary code
- [sketchviz](https://github.com/gpotter2/sketchviz) : command line clone of https://sketchviz.com that render Graphviz diagrams using [RoughJS](https://roughjs.com/) to get a hand-drawn, sketchy appearance

## Word / tag clouds

- [nuagesdemots.fr](https://www.nuagesdemots.fr) : uses [timdream/wordcloud2.js](https://github.com/timdream/wordcloud2.js)
- [https://github.com/ywng/Progressive-News-Cloud](Progressive-News-Cloud)
- [https://github.com/jasondavies/d3-cloud](jasondavies/d3-cloud)

## UML
- [nomnoml](http://www.nomnoml.com) : pretty UML diagrams based on a textual description
- [UMLet](http://www.umlet.com) : open-source, diagrams can be export to eps, pdf, jpg, svg + new web-based UMLet: called [UMLetino](http://www.umlet.com/umletino)
- [PlantUML](http://plantuml.com) -> conversion to PNG or SVG (Java) - [official online editor](http://www.plantuml.com/plantuml/uml/) - [alt online editor](https://plantuml-editor.kkeisuke.dev/) using `!theme sketchy-outline`:

    java -jar plantuml.jar -tsvg -nometadata diagram.plantuml.txt

```uml
@startuml
skinparam defaultTextAlignment center

artifact component1 as "Composant #1" {
    queue component1Queue as "Notifs" #YellowGreen
    boundary component1api as "REST API #1"
}
collections collec1 #YellowGreen [
    <b>MacroService #1</b>
    Kubernetes
]
collections collec2 #YellowGreen [
    <b>MacroService #2</b>
    Kubernetes
]

component service1 as "MicroService #1"
control Cron as cron

component service2 as "MicroService #2"

queue queue1 as "Queue (Event BUS)" #Beige

queue1 -> collec2

boundary api1 as "Websocket API" #Beige

database db1 #SkyBlue [
    <b>Database #1</b>
    ----
    Dynamodb
]
boundary api2 as "REST API #2" #SkyBlue

folder folder1 as "S3 bucket" #Violet

cron --> service1
service1 -u-> component1api : pull
service1 --> db1
service1 --> queue1 : push

component1api ---> collec1 : push
collec1 --> db1
collec1 --> queue1
queue1 --> service2

folder1 -u-> api2 : pull
api2 -u-> db1
api1 -> folder1 : push
service2 ---> api1 : consume

@enduml
```

## Sequence diagrams
- [WebSequenceDiagrams](https://www.websequencediagrams.com/embedding.html) : recommended by the IETF (web API)
- [UMLet](http://www.umlet.com)

## Histograms & other graphs
- [Chart.js](https://www.chartjs.org) : used on https://nf-co.re/stats#github_prs
- [tehmaze/diagram](https://github.com/tehmaze/diagram) : text mode utf8 diagrams in colors, in Python
- <https://plot.ly> examples: https://plot.ly/javascript/histograms/


## Command-line tips & tricks for demos

- use & abuse shell history command search : `CTRL`+`R`
  * make your you keep enough history: put `export HISTSIZE=20000` in your `.bashrc`
  * add a `#tag` at the end of long commands you want to retrieve easily, so that you can later on `CTRL`+`R` on this keyword. Exemple:
```
curl ... # rundeck
```
- if your terminal is broken (your prompt is broken, you cannot see what you type...) : `CTRL`+`L` and then type the command `reset`
- half-maximize a window on one side:
  * on Ubuntu: `CTRL`+`SUPER`+`Left`/`Right`
  * on Windows: `CMD`+`Left`/`Right`
- add the following in your `.bashrc` in order to display the return code of the last command executed on your prompt:
```
prompt_command() { EXIT_CODE=${?/#0/}; }; export PROMPT_COMMAND=prompt_command; export PS1='\[\e[0;34m\]\u\[\e[0m\]@\[\e[1;35m\]\h\[\e[0m\]:\[\e[0;32m\]\W\[\e[0m\]\[\e[1;31m\] $EXIT_CODE\[\e[0m\]\$ '
```
- know your `.inputrc`. Make sure your `HOME`/`END` keys work. Enable relaxed tab-completion:
```
set show-all-if-ambiguous on
set completion-ignore-case on
```


# How to give presentations
- Tell STORIES to inspire your audience and make them better remember what you said,
  _cf._ [Why Telling a Story is the Most Powerful Way to Activate Our Brains](https://lifehacker.com/the-science-of-storytelling-why-telling-a-story-is-the-5965703)
- [You Suck At PowerPoint! by @jessedee](https://www.slideshare.net/jessedee/you-suck-at-powerpoint)
  Mistakes to avoid:
  1. too much info
  2. not enough visuals
  3. crap quality
  4. visual vomit
  5. lack of prep
- [The smackdown learning model](http://blog.codinghorror.com/in-defense-of-the-smackdown-learning-model/):
  add heat & controversy to your presentations!
  **Ex:** Presentation Smackdown: 2 presenters, 2 frameworks, 1 guy with the big bell.

## Style: Lessons in Clarity and Grace
Based on [a 2-pages summary by Fabien Pinckaers](https://docs.google.com/document/d/1F8_p3bkzugTvkBd1Ja6bHLR2v_XXRWqtcq7jF2gu0EM/edit)
* A sentence is clear when **its important actions are in verbs**, and **main characters are subjects**
* Reassemble using conjunctions such as _if, although, because, when, how, why_
* When the character is not clear, use the word “you” as often as you can
* When writing paragraphs, the last few words of one sentence should set up information that appears in the first few words of the next.
* Begin sentences with what they are “about”; end with words that should receive a special emphasis.
* To motivate the reader, you should address **why your topic is important in the introduction**. A good introduction structure contains: a shared context, a problem, the solution
* Shorter is better. Short sentences are strong.

## Benjamin G. advices
- always **rehearse with someone**
- always prepare **a commands cheat-sheet**
- **do not think about people reading your slides later**: you will bloat them with too many words
- your speech must be != than the slides content
- it is more important to arouse interest and set off a desire to find more info, than to explain every detail
- contextualize (why you did this, how you discovered that...) the information you present
- logos > tools names, photos > people names (not in public slides, for legal reasons)
- avoid too many bullet points list
- 20min talk ? -> no need to display the plan
- slides titles are not always necessary


# Rhetoric
- [Arguments rhétologiques fallacieux](http://www.informationisbeautiful.net/visualizations/rhetological-fallacies/arguments-rhetologiques-fallacieux/)
- [Which Online Discussion Archetype Are You](http://blog.codinghorror.com/which-online-discussion-archetype-are-you/)
- [Bingo du troll](https://grisebouille.net/le-bingo-du-troll/)
- [American Chopper Meme](https://www.vox.com/2018/4/10/17207588/american-chopper-meme):
  * > Each panel comes complete with text, and makes for a mini debate — proposition, rebuttal, reaffirmation, second rebuttal, and a final statement.
  * > the Chopper offers a lighthearted way to demonstrate that you actually understand the viewpoints of people on both sides of an issue
  * > The meme functions, in this sense, as a miniature version of one of Plato’s dialogues.
    > Rather than a conventional prose argument, in these books, Plato gives us drama.
    > The dialogue format makes the line of argument more memorable and allows for the simultaneous presentation of a clear thesis and a deeper understanding of the issues.
