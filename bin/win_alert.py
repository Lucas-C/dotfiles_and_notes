import sys
from win10toast import ToastNotifier  # pip install win10toast
if len(sys.argv) < 3:
    print('USAGE: win_alert $title $msg', file=sys.stderr)
    sys.exit(1)
ToastNotifier().show_toast(sys.argv[1], sys.argv[2])