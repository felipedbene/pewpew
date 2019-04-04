#!/bin/bash
export DISPLAY=":0"
rm -rf $HOME/.config/chromium/Default/*Cache*
rm -rf $HOME/cache/*
WID=$(xdotool search --onlyvisible --class chromium|head -1)
xdotool windowactivate ${WID}
xdotool key ctrl+F5