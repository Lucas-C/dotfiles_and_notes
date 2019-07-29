#!/bin/bash
set -o errexit
cd $( dirname "${BASH_SOURCE[0]}" )
mv answer.py{,.bak}
python -m zipapp --main AutonomousRunner:main_with_defaults $PWD
mv answer.py{.bak,}
echo Built:
ls -l $PWD.pyz
echo To try:
echo CAT \<\<EOF \> answer.py
cat answer_empty.py
echo EOF
echo python $PWD.pyz
echo
echo Now performing insta-test:
# We change directory to really import modules in the ZIP and not directly files in here:
pyz=$PWD.pyz
cp answer_empty.py ../answer.py
cd ..
python $pyz "$@" || true
rm answer.py
