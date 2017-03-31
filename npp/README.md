**Life saving** : `%APPDATA%\Notepad++\backup`


# Install

As admin:
```
h=/cydrive/c/Users/$USER
for f in $BASHRC_DIR/npp/*.xml; do cmd /c mklink $(cygpath -w $h/AppData/Roaming/Notepad++/)$(basename $f) $(cygpath -w $f); done
cmd /c mklink /d $(cygpath -w $h/AppData/Roaming/Notepad++/themes) $(cygpath -w $BASHRC_DIR/npp/themes)
```

## config.xml

Sadly, Notepad++ `config.xml` includes user history, hence it cannot be easily versionned / shared.

Instead, you can perform XML changes to this file, while Notepad++ is shut down, using `xmlstarlet` (`apt-cyg install xmlstarlet`) :

    # Setting defaul EOL to NL
    xmlstarlet ed --inplace --update '/NotepadPlus/GUIConfigs/GUIConfig[@name="NewDocDefaultSettings"]/@format' --value 2 $h/AppData/Roaming/Notepad++/config.xml
    # Substituting tabs by whitespaces
    xmlstarlet ed --inplace --update '/NotepadPlus/GUIConfigs/GUIConfig[@name="TabSetting"]/@replaceBySpace' --value yes $h/AppData/Roaming/Notepad++/config.xml


# Tips & tricks

If you initially installed an old NPP version, manually remove `stylers.xml` and `langs.xml` to use the new `javascript.js` lexer: https://github.com/notepad-plus-plus/notepad-plus-plus/issues/2133#issuecomment-236373170

Setting > Style Configure > select Javascript > add "json" User ext

Edit > Line Operations > Sort Lines in Ascending / Descending Order

`<ALT>+<SHIFT>` : vertical selection -> useful to comment at the beggining of the line


## Plugins

- XML Tools -> can validate XML

## Under the hood

Link between a theme `LexerType name` and its lexer, e.g. `SCLEX_CPP` for `javascript.js` : https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/PowerEditor/src/ScitillaComponent/ScintillaEditView.cpp#L142

C++ / C / Java / Javascript lexer: https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/scintilla/lexers/LexCPP.cxx

`SCE_C` indices definitions to use as `WordsStyle styleID` : https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/scintilla/include/SciLexer.h#L166

Default `javascript.js` keywords: https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/PowerEditor/src/langs.model.xml#L130
`type2` keywords are not supported, and neither `require`, `module`, `exports`... cf. https://github.com/notepad-plus-plus/notepad-plus-plus/issues/3117
