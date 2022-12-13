# USAGE: python win_alert.py $message [$header]
# Require win10toast installed with a Windows version of Python => does not work in WSL2
import sys
from win10toast import ToastNotifier  # pip install win10toast
if len(sys.argv) < 3:
    print('USAGE: win_alert $message [$header]', file=sys.stderr)
    sys.exit(1)
title = sys.argv[2] if len(sys.argv) > 2 else 'ALERT'
ToastNotifier().show_toast(title, sys.argv[1])