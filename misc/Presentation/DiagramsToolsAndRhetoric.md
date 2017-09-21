# Tools

- `md2html` (NodeJS, based on `markdown-it` that implements CommonMark)
- Reveal.js & Impress.js & DZSlides
- [MathJax JS](https://www.mathjax.org)
- [markdown-toc](https://github.com/jonschlinkert/markdown-toc) : generate a markdown table of contents for READMEs (NodeJS)
There are many alternatives: in [bash](https://github.com/ekalinin/github-markdown-toc), [Python](https://github.com/rasbt/markdown-toclify)
- [grip](https://github.com/joeyespo/grip) : preview GitHub Markdown files like READMEs (Python)


# Diagrams

- [knsv/mermaid](https://github.com/knsv/mermaid) : graphs, GANTT diagrams and flowcharts from markdown-like syntax (Javascript, requires to embed `mermaid.css` & `mermaid.min.js`)
- [asciiflow](http://asciiflow.com/#Draw) : online + OSS (Javascript) -> https://github.com/lewish/asciiflow2
- [mapio/GraphvizAnim](https://github.com/mapio/GraphvizAnim) : animated graph visualizations, based on graphviz (Python)
- [draw.io](https://www.draw.io) : diagrams stored as XML, online editor, OSS (Java) -> https://github.com/jgraph/draw.io
- [ditaa](http://ditaa.sourceforge.net/) : ascii-art to images (Java)
- [blampe/goat](https://github.com/blampe/goat) : render ASCII art as SVG diagrams (Go)
- [ivanceras/svgbobrus](https://github.com/ivanceras/svgbobrus) : convert ascii diagram scribbles into SVG (Rust)
- [gliffy](https://www.gliffy.com/examples/) : online, proprietary code

## UML
- [PlantUML](http://plantuml.com) -> conversion to PNG or SVG (Java):

    java -jar plantuml.jar -tsvg -nometadata diagram.plantuml.txt

## Sequence diagrams
- [WebSequenceDiagrams](https://www.websequencediagrams.com/embedding.html) : recommended by the IETF (web API)

## Histograms
- [tehmaze/diagram](https://github.com/tehmaze/diagram) : text mode utf8 diagrams in colors, in Python


# Command-line tips & tricks for demos

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


# Rhetoric
- Tell STORIES to inspire your audience and make them better remember what you said
- [The smackdown learning model](http://blog.codinghorror.com/in-defense-of-the-smackdown-learning-model/)
- [Arguments rhétologiques fallacieux](http://www.informationisbeautiful.net/visualizations/rhetological-fallacies/arguments-rhetologiques-fallacieux/)
- [Which Online Discussion Archetype Are You](http://blog.codinghorror.com/which-online-discussion-archetype-are-you/)

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
