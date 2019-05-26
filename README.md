ayatana-indicator-updatenotifier: A simple system packages update checker.

The python module will show an Ayatana Indicator and notification pop-up when
updates are available. Set this script to run on session startup, and it will
check for updates every hour by default.

The icon and text to display in notification pop-up and the update check
interval is configurable in the python module.

This is intended for desktop environments like XFCE or MATE that don't have a
native PackageKit update watcher.

___
Use the distribution-specific cron jobs from package cron-apt or apticron or
these hand-crafted ones:

$ cat /etc/cron.d/ayatana_indicator_updatenotifier
@reboot root /etc/cron.hourly/ayatana_indicator_updatenotifier

$ cat /etc/cron.hourly/ayatana_indicator_updatenotifier
#!/bin/sh

MAILTO=""

test -x /usr/bin/apt-get || exit 0

TIME_MIN="60"
TIME_MAX="180"
TIME_INT="$(/usr/bin/shuf -i $TIME_MIN-$TIME_MAX -n 1)"

/bin/sleep $TIME_INT
/usr/bin/apt-get update

exit $?

___
Use the usr-share helper script to watch for available package updates.

___
See the LICENSE file for how to be modified and distributed.

Requires: PyGObject, gi.Gio, gi.GLib, gi.Gtk and AyatanaAppIndicator3

Based on: https://dev1galaxy.org/viewtopic.php?id=2641
