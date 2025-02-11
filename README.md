#### ayatana-indicator-updatenotifier: A simple system packages update checker.

The python module will show an Ayatana Indicator and notification pop-up when updates are available and checks for updates every hour. By default, it will not be started with autostart.

The fallback icon and text to display in notification pop-up and the update check interval is configurable in the python module.

This is intended for desktop environments like XFCE or MATE that don't have a native PackageKit update watcher.
___
The _ayatana-indicator-updatenotifier.desktop_ file is installed to _{prefix}/share/applications_. Link to _/etc/xdg/autostart_, if it should be started automatically.
___
Use the distribution-specific cron jobs from package _cron-apt_ or _apticron_ or something like these hand-crafted ones:

##### $ cat /etc/cron.d/ayatana_indicator_updatenotifier
```
@reboot root /etc/cron.hourly/ayatana_indicator_updatenotifier
```
##### $ cat /etc/cron.hourly/ayatana_indicator_updatenotifier
```
#!/bin/sh

MAILTO=""

test -x /usr/bin/apt-get || exit 0

TIME_MIN="60"
TIME_MAX="180"
TIME_INT="$(/usr/bin/shuf -i $TIME_MIN-$TIME_MAX -n 1)"

/bin/sleep $TIME_INT
/usr/bin/apt-get update

exit $?
```
___
See the LICENSE file for how to be modified and distributed.

Requires: [PyGObject](https://lazka.github.io/pgi-docs/GObject-2.0/index.html), [gi.Gio](https://lazka.github.io/pgi-docs/Gio-2.0/index.html), [gi.GLib](https://lazka.github.io/pgi-docs/GLib-2.0/index.html), [gi.Gtk](https://lazka.github.io/pgi-docs/Gtk-3.0/index.html) and [AyatanaAppIndicator3](https://lazka.github.io/pgi-docs/AyatanaAppIndicator3-0.1/index.html)

Based on: [Dev1Galaxy - Software update notifications in XFCE](https://dev1galaxy.org/viewtopic.php?id=2641)
