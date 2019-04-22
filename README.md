ayatana-indicator-updatenotifier: A simple system packages update checker.

The python module will show an Ayatana Indicator and notification pop-up when
updates are available. Set this script to run on session startup, and it will
check for updates every hour by default.

Use the distribution-specific cron jobs and usr-share helper script to watch
for available package updates.

The icon and text to display in notification pop-up and the update check
interval is configurable in the python module.

This is intended for desktop environments like XFCE or MATE that don't have a
native PackageKit update watcher.

See the LICENSE file for how to be modified and distributed.

Requires: PyGObject, gi.Gio, gi.GLib, gi.Gtk and AyatanaAppIndicator3

Based on: https://dev1galaxy.org/viewtopic.php?id=2641
