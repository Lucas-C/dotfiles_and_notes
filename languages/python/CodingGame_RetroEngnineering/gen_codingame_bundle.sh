#!/bin/bash
cat gis.py Answer.py > CG_Answer.py
sed -i '/from gis import .*/d' CG_Answer.py
