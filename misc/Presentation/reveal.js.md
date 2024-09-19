Doc: https://revealjs.com
Online visual editor: http://slid.es

# Markdown Demo
<link rel="stylesheet" href="md-tags.css"/>

<span class=red>RED red Red</span>

<span class=ocre>OCRE ocre Ocre</span>

<span class=yellow>YELLOW yellow Yellow</span>

<span class=green>GREEN green Green</span>

<span class=blue>BLUE blue Blue</span>

### Some code

    <style>
    code {
        font-size: xx-large !important;
    }
    </style>

    ```
    function monNomDeFonction(paramètre1, paramètre2) {
        // ... code ...
    }
    ```

Add a class on the first slide only:

    <!-- .element: data-state="first-slide" -->

Change the background on a slide:

    <!-- .slide: data-background="#ff0000" -->

Add class one slide:

    <!-- .slide: class="poll" -->

## Features
Le nombre de sauts de ligne (2 ou 3) entre chaque ##section indique la direction du slide suivant (bas/droite)

    <ul>
        <li class="fragment">Uno</li>
        <li class="fragment">Dos</li>
        <li class="fragment">Tres</li>
    </ul>

    Note: Coucou ! This will only be displayed in the speaker window

## Down to the rabbit hole...
With *bold*, **italics** and ~~striked~~ text.

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

## Multimedia era
<video data-autoplay src="http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"></video>

## Back to start
<a href="#/">Click me !</a>

## Shortcuts:
* Press `s` to open speaker-notes pop-up window
* Press `ESC` to enter the slide overview
* Press `b` to fade out to black screen

## Poll
https://github.com/jschildgen/reveal.js-poll-plugin (used on chezsoi.org)

## PDF export
Using Chrome: https://github.com/hakimel/reveal.js/#pdf-export

+ append 'index.html?print-pdf&showNotes' and scroll to the end before printing

## Script

    if (/showNotes/.test(location.search)) {
        options.showNotes = true; // for PDF export to include notes
    }
    Reveal.initialize(options);
    document.addEventListener('ready', function(event) { // RevealJS finished rendering
        // Open all links in a new tab:
        [].forEach.call(document.getElementsByTagName('a'), a => a.target = '_blank')
        // Any click on the page should trigger a slide change:
        document.onclick = (event) => { if (event.target.tagName.toLocaleLowerCase() != 'a') { Reveal.next() } }
        // Drawing histograms:
        const data = {
          "git": 3.3333333333333335,
          "modules Puppet": 2.25,
          "Hesperides": 2.0833333333333335,
          "Docker": 3.25,
          "Ansible": 2.5833333333333335,
          "CloudFormation": 1.6666666666666667,
          "Terraform": 1.6666666666666667,
          "Tosca": 1.0
        }
        Plotly.plot('technos-histograms', [{
          histfunc: "sum",
          x: Object.keys(data),
          y: Object.values(data),
          type: "histogram",
          name: "count"
        }])
        Reveal.layout() // re-compute slides height ("top" CSS attribute)
    })
