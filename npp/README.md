**Life saving** : `%APPDATA%\Notepad++\backup`


# Install

As admin:
```
h=/cydrive/c/Users/$USER
for f in $BASHRC_DIR/npp/*.xml; do cmd /c mklink $(cygpath -w $h/AppData/Roaming/Notepad++/)$(basename $f) $(cygpath -w $f); done
cmd /c mklink /d $(cygpath -w $h/AppData/Roaming/Notepad++/themes) $(cygpath -w $BASHRC_DIR/npp/themes)
```


# Tips & tricks

Setting > Style Configure > select Javascript > add "json" User ext

Edit > Line Operations > Sort Lines in Ascending / Descending Order

`<ALT>+<SHIFT>` : vertical selection -> useful to comment at the beggining of the line


## Plugins

- XML Tools -> can validate XML
