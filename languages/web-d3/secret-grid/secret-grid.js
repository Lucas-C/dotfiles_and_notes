const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
const DEFAULT_KEY_LETTER = () => ({value: ''});
const DEFAULT_GRID_LETTER = () => ({value: '', checked: false});

var app = new Vue({
  el: '#app',
  data: {
    key: [],
    grid: [],
    showControls: true
  },
  methods: {
    addLetterToKey: function () {
      this.key.push(DEFAULT_KEY_LETTER());
      while (this.grid && this.grid[0].length < this.key.length) {
        this.grid.forEach(row => row.push(DEFAULT_GRID_LETTER()));
      }
    },
    removeLetterFromKey: function () {
      this.key.splice(-1, 1);
      this.saveKey();
      while (this.grid && this.grid[0].length > this.key.length) {
        this.grid.forEach(this.removeRow);
      }
    },
    addRow: function () {
      this.grid.push([...Array(this.key.length)].map(DEFAULT_GRID_LETTER));
    },
    removeRow: function () {
      this.grid.splice(-1, 1);
      this.saveGrid();
    },
    gridCellClicked: function (row, i) {
      row[i].checked = !row[i].checked;
      this.saveGrid();
    },
    fillGridLetters: function () {
      this.grid.forEach((row, i) => {
        row.forEach((letter, j) => {
          var c = this.nthCharAfter(this.key[j].value, i);
          letter.value = (letter.checked) ? c : this.randCharExcept(c);
        });
      });
      this.saveGrid();
    },
    nthCharAfter: function (c, i) {
      return CHARS[(CHARS.indexOf(c.toUpperCase()) + i + 1) % CHARS.length];
    },
    randCharExcept: function (notChar) {
      var c;
      do {
        c = CHARS[Math.floor(Math.random() * CHARS.length)];
      } while (c === notChar);
      return c;
    },
    saveKey: function () {
      localStorage.setItem('SecretGridKey', this.key.map(l => l.value).join(''));
    },
    saveGrid: function () {
      localStorage.setItem('SecretGridGrid', JSON.stringify(this.grid));
    },
  },
  created: function () {
    this.showControls = document.location.search !== '?nocontrols';
    // Restore initial values from local storage or use some default ones
    this.key = (localStorage.getItem('SecretGridKey') || 'password').split('').map(l => ({value: l}));
    if (localStorage.getItem('SecretGridGrid') !== null) {
        this.grid = JSON.parse(localStorage.getItem('SecretGridGrid'));
    } else {
        [...Array(10)].forEach(this.addRow);
    }
  }
});
