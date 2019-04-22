ayatana-indicator-updatenotifier: A simple system packages update checker.

By default, this script will watch for available apt-get updates and show an
Ayatana Indicator and notification pop-up when updates are available. Set this
script to run on session startup, and it will check for updates every hour.

The command to run the update check and interval thereof is configurable in the
source code. Text to display in notification pop-up is also configurable.

This is intended for desktop environments like XFCE or MATE that don't have a
native PackageKit update watcher.

See the LICENSE file for how to be modified and distributed.

Requires: PyGObject, gi.Gio, gi.GLib, gi.Gtk and AyatanaAppIndicator3

Based on: https://dev1galaxy.org/viewtopic.php?id=2641
