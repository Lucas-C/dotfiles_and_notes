# Install

    apm install atom-typescript
    apm install language-batch
    apm install language-gherkin-i18n
    apm install symbol-gen

```
h=/cydrive/c/Users/$USER
for f in $BASHRC_DIR/.atom/*; do
    newf=$h/.atom/$(basename $f)
    [ -f $newf ] && mv $newf{,.bak}
    cmd /c mklink $(cygpath -w $newf) $(cygpath -w $f)
done
```
