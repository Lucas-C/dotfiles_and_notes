#!/bin/bash
cd $( dirname "${BASH_SOURCE[0]}" )
mv Answer.py{,.bak}
python -m zipapp --main AutonomousRunner:main_with_defaults $PWD
mv Answer.py{.bak,}
echo Built:
ls -l $PWD.pyz
echo To try:
echo CAT \<\<EOF \> my_answer.py
cat static_answer.py
echo EOF
echo PYTHONPATH=. python $PWD.pyz

echo Now performing insta-test:
cp static_answer.py my_answer.py
# We change directory to really import modules in the ZIP and not directly files in here:
pyz=$PWD.pyz
cd ..
PYTHONPATH=. python $pyz --explicit --iteration-sleep 0
