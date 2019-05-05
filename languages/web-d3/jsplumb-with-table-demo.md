<!-- Generate HTML with md2html -->
# Demo JSPlumb with table

:::: grid
::: grid-box
- [ ] blabla
- [ ] blabla
:::

::: grid-box
- [ ] blabla
- [ ] blabla
:::

::: grid-box
- [ ] blabla
- [ ] blabla
:::

::: grid-box
- [ ] blabla
- [ ] blabla
:::

::: grid-box
|             | ~~⚀~~ ~~⚁~~ | ~~⚂~~ ~~⚃~~ | ~~⚄~~ ~~⚅~~ |
|-------------|-------------|-------------|-------------|
| ~~⚀~~ ~~⚁~~ |             |             |             |
| ~~⚂~~ ~~⚃~~ |             | Au choix    |             |
| ~~⚄~~ ~~⚅~~ |             |             |             |
:::

::: grid-box
- [ ] blabla
- [ ] blabla
:::

::: grid-box
- [ ] blabla
- [ ] blabla
:::

::: grid-box
- [ ] blabla
- [ ] blabla
:::

::: grid-box
- [ ] blabla
- [ ] blabla
:::
::::

<style type="text/css">
body {
  max-width: 36rem;
  margin: 0 auto;
  padding: 4rem;
  font-family: Calibri,Arial,sans-serif;
  font-size: .8rem;
  line-height: 1.4;
}
h1 {
  text-transform: uppercase;
  font-size: 4rem;
  text-align: center;
  line-height: 1;
  margin: 0;
}
s { text-decoration: none; font-size: 1.2rem; line-height: .8; vertical-align: bottom; }
table {
  border-spacing: 0;
  border-collapse: collapse;
  border-style: hidden; /* supprime les bordures autour du tableau */
  margin: 0 auto;
  page-break-inside: avoid;
}
th, td {
  padding: 0;
  border: 1px solid black;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  position: relative; /* pour JSPlumb */
}
.grid table, .grid thead, .grid tbody { width: 100%; }
.grid th:first-child, .grid td {
  width: 25%;
  height: 0;
  padding-bottom: 25%; /* pour forcer un ratio carré */
}
.grid th, .grid td:first-child, .grid tr:nth-child(2) td:nth-of-type(3) { padding-bottom: 0; }
.grid-box {
  flex: 1 0 33%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.grid-box > * {
  list-style: none;
  padding-inline-start: 0;
}
</style>

<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jsPlumb/2.9.2/css/jsplumbtoolkit-defaults.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jsPlumb/2.9.2/js/jsplumb.js"></script>
<script>
jsPlumb.ready(function() {
    jsPlumb.setContainer(document.querySelector('.grid'));
    var paintStyle = { stroke:'#456' };
    var endpointStyle = { radius: 5, fill: '#456' };
    jsPlumb.connect({
        source: document.querySelector('.grid .grid-box:nth-of-type(1) > *'),
        target: document.querySelector('.grid tr:nth-child(1) td:nth-child(2)'),
        connector: 'Straight', paintStyle: paintStyle,
        anchors: ['Bottom', 'Center'],
        endpoints: ['Blank', 'Dot'], endpointStyle: endpointStyle,
    });
    jsPlumb.connect({
        source: document.querySelector('.grid .grid-box:nth-of-type(2) > *'),
        target: document.querySelector('.grid tr:nth-child(1) td:nth-of-type(3)'),
        connector: 'Straight', paintStyle: paintStyle,
        anchors: ['Bottom', 'Center'],
        endpoints: ['Blank', 'Dot'], endpointStyle: endpointStyle,
    });
    jsPlumb.connect({
        source: document.querySelector('.grid .grid-box:nth-of-type(3) > *'),
        target: document.querySelector('.grid tr:nth-child(1) td:nth-of-type(4)'),
        connector: 'Straight', paintStyle: paintStyle,
        anchors: ['Bottom', 'Center'],
        endpoints: ['Blank', 'Dot'], endpointStyle: endpointStyle,
    });
    jsPlumb.connect({
        source: document.querySelector('.grid .grid-box:nth-of-type(4) > *'),
        target: document.querySelector('.grid tr:nth-child(2) td:nth-of-type(2)'),
        connector: 'Straight', paintStyle: paintStyle,
        anchors: ['Right', 'Center'],
        endpoints: ['Blank', 'Dot'], endpointStyle: endpointStyle,
    });
    jsPlumb.connect({
        source: document.querySelector('.grid .grid-box:nth-of-type(6) > *'),
        target: document.querySelector('.grid tr:nth-child(2) td:nth-of-type(4)'),
        connector: 'Straight', paintStyle: paintStyle,
        anchors: ['Left', 'Center'],
        endpoints: ['Blank', 'Dot'], endpointStyle: endpointStyle,
    });
    jsPlumb.connect({
        source: document.querySelector('.grid .grid-box:nth-of-type(7) > *'),
        target: document.querySelector('.grid tr:nth-child(3) td:nth-of-type(2)'),
        connector: 'Straight', paintStyle: paintStyle,
        anchors: ['Top', 'Center'],
        endpoints: ['Blank', 'Dot'], endpointStyle: endpointStyle,
    });
    jsPlumb.connect({
        source: document.querySelector('.grid .grid-box:nth-of-type(8) > *'),
        target: document.querySelector('.grid tr:nth-child(3) td:nth-of-type(3)'),
        connector: 'Straight', paintStyle: paintStyle,
        anchors: ['Top', 'Center'],
        endpoints: ['Blank', 'Dot'], endpointStyle: endpointStyle,
    });
    jsPlumb.connect({
        source: document.querySelector('.grid .grid-box:nth-of-type(9) > *'),
        target: document.querySelector('.grid tr:nth-child(3) td:nth-of-type(4)'),
        connector: 'Straight', paintStyle: paintStyle,
        anchors: ['Top', 'Center'],
        endpoints: ['Blank', 'Dot'], endpointStyle: endpointStyle,
    });
});
</script>
