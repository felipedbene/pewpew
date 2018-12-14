#!/bin/bash
export DISPLAY=":0"
rm -rf $HOME/.config/chromium/Default/*Cache*
WID=$(xdotool search --onlyvisible --class chromium|head -1)
xdotool windowactivate ${WID}
xdotool key ctrl+F5