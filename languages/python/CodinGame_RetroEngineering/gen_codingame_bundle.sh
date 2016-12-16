#!/bin/bash
cat hero_utils.py hero_ghostcloseby.py hero_explorerinstinct.py Answer.py > CG_Answer.py
sed -i -e '/from hero_utils import .*/d' -e '/from hero_ghostcloseby import .*/d' -e '/from hero_explorerinstinct import .*/d' CG_Answer.py

