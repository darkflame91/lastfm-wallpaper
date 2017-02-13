#!/bin/sh

one="tell application \"System Events\" to set picture of every desktop to (\""
two=$1
twotwo=$2
three="\" as POSIX file as alias)"
main="${one}${two}default.jpg${three}"
echo $main
osascript -e "$main"
killall Dock
main="${one}${two}${twotwo}${three}"
echo $main
osascript -e "$main"
killall Dock