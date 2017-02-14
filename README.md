# lastfm-wallpaper
This is a simple script with the intention of dynamically changing the wallpaper with the details of the currently playing track.

I use a monitor with a transparent terminal, and the intention is to have the script changing the background according to the track.

## Platforms
Currently working on this for CentOS 7 and MacOS Sierra. All testing, unless otherwise specified will be on these platforms.
* **Linux:** Will *most likely* work on Ubuntu, Mint, Fedora, RHEL, and any other OS using GNOME 3 or derivatives. This hasn't been tested though.
* **Mac:** Should work on El Capitan as well. Might not work on any older versions.
* **Windows:** Not been currently implemented. I don't use Windows, and this script fulfills a very niche requirement, so I don't think I'll ever actually implement it. If anyone stumbles across this, and wants Windows support, let me know. Or if you're interested, go ahead and add support and send me a pull request. :)


## Requirements
I've built this with Python 2.7. Haven't tested any other versions.

You'll need to install Pillow, Requests, and Tkinter if you don't have them already.

## Usage
* Set your lastfm username at the USERNAME variable
* Run: python lastfm-wallpaper.py
* You might want to run it as a daemon (python lasfm-wallpaper.py &) if you want to close the terminal and don't want to see logs