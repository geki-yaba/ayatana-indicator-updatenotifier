#!/usr/bin/env python3

################################################################################
# Configuration Section Begins Here                                            #
################################################################################

import os
import sys

# prefix function from
# Copyright (C) 2010-2012  James Shubin
# https://purpleidea.com/blog/2012/09/20/finding-your-software-install-prefix-from-inside-python/
def prefix(join=None):
    """Returns the prefix that this code was installed into."""
    path = os.path.abspath(__file__)
    name = os.path.basename(os.path.dirname(path))
    this = os.path.basename(path)

    version_info = sys.version.split()
    major, minor, micro = version_info[0].split('.')

    # rule set
    rules = [
        lambda x: x == 'lib',
        lambda x: x == f'python{major}.{minor}',
        lambda x: x in ['site-packages', 'dist-packages'],
        lambda x: x == name,    # 'project'
        lambda x: x == this,    # '.py'
    ]

    # matching engine
    while len(rules) > 0:
        (path, token) = os.path.split(path)
        rule = rules.pop()
        if not rule(token):
            return False

    if join is None:
        return path

    return os.path.join(path, join)

config = dict(
    # The title to be shown in the pop-up.
    title = 'Updates Available',

    # The message to be shown in the pop-up.
    message = 'There are {0} updates available to install.\n\nPackage list:\n{1}',

    # Icon to use in the indicator and pop-up.
    icon = prefix('lib/ayatana-indicator-updatenotifier/updates.svg'),

    # Command to run to check for available updates, and the expected output
    # that indicates updates are available. Print count of updates available.
    pkg_check = prefix('lib/ayatana-indicator-updatenotifier/ayatana-indicator-updatecheck'),
    pkg_list = prefix('lib/ayatana-indicator-updatenotifier/ayatana-indicator-updatelist'),
    pkg_update = prefix('lib/ayatana-indicator-updatenotifier/ayatana-indicator-update-apt-get'),
    terminal = '/usr/bin/xterm',
    terminal_execute_flag = '-e',

    # Frequency to check for available updates.
    interval = 3600, # 1 hour
)

################################################################################
# Configuration Section Ends Here                                              #
################################################################################

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gio, GLib, Gtk
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator

    import subprocess
    from time import time
    from random import random
except ImportError:
    print("Failed to import Gio, GLib, Gtk or AyatanaAppIndicator3 or other helpers")
    raise NotImplementedError

class AyatanaUpdateNotifier:
    def __init__(self):
        # + 200 for cron job to run at boot
        self.next_check = int(time()) + 200 + int(random() * 300)

        # service to run only one instance and allow to functioning as-is
        self.app = Gio.Application.new('ayatana.update.notifier.app', Gio.ApplicationFlags.IS_SERVICE)

        try:
            if (self.app.register() == True):
                # keep application running
                self.app.hold()

                # application hide action
                action_hide = Gio.SimpleAction.new('hide')
                action_hide.connect('activate', self._on_action_hide)

                self.app.add_action(action_hide)

                # keep application running
                self.app.set_inactivity_timeout(180000)

                # hidden indicator app
                self.indicator = self._indicator_app()
                self._indicator_menu('0', "")

                self.timer_source_id = GLib.timeout_add_seconds(60, self._query_update)

                # keep application running
                self.app.release()
        except GLib.Error as e:
            print('Failed to register service: {0} ({1})'.format(e.message, e.code))

    # internal: get indicator icon
    def _get_icon_file(self, size):
        global config
        icon_file = config['icon']

        icon_theme = Gtk.IconTheme.get_default()
        icon_info = icon_theme.choose_icon(['system-software-update'], size, 0)
        if (icon_info != None):
            icon_file = icon_info.get_filename()
        return icon_file

    # internal: create indicator app
    def _indicator_app(self):
        global config
        indicator = appindicator.Indicator.new('ayatana.update.notifier.indicator',
            self._get_icon_file(Gtk.IconSize.LARGE_TOOLBAR), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_title(config['title'])
        indicator.connect('connection-changed', self._on_connect_changed)
        return indicator

    # internal: create indicator menu
    def _indicator_menu(self, count, pkgs):
        # minimalistic menu for indicator
        menu = Gtk.Menu()

        item_hide = Gtk.MenuItem.new_with_label('Hide')
        item_hide.connect('activate', self._on_menu_hide)
        menu.append(item_hide)

        item_update = Gtk.MenuItem.new_with_label('Update')
        item_update.connect('activate', self._on_menu_update)
        menu.append(item_update)

        if (count != '0'):
            menu.append(Gtk.SeparatorMenuItem())

            items = pkgs.splitlines()

            for item in items:
                item_pkg = Gtk.MenuItem.new_with_label(item)
                menu.append(item_pkg)

        menu.show_all()

        # register menu and secondary target to indicator
        self.indicator.set_menu(menu)
        self.indicator.set_secondary_activate_target(item_hide)

    # callback: timer
    def _query_update(self):
        global config

        # keep application running
        self.app.hold()

        if (int(time()) >= self.next_check):
            self.next_check = self.next_check + config['interval'] + int(random() * 300)

            count = subprocess.getoutput(config['pkg_check'])

            if (count != '0'):
                # show indicator icon and update count
                self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
                self.indicator.set_label('{0}'.format(count),'{0}'.format(count))

                pkgs = subprocess.getoutput(config['pkg_list'])

                # show notification popup
                icon = Gio.Icon.new_for_string(self._get_icon_file(-1))
                notifier = Gio.Notification.new(config['title'])
                notifier.set_body(config['message'].format(count, pkgs))
                notifier.set_default_action('app.hide')
                notifier.set_icon(icon)

                self.app.send_notification('ayatana-update-notifier-popup', notifier)

                # reset indicator menu
                self._indicator_menu(count, pkgs)

        # keep application running
        self.app.release()

        return GLib.SOURCE_CONTINUE

    # callback: hide indicator app from notification or secondary-activate mapping
    def _on_action_hide(self, action, parameter):
        self.indicator.set_status(appindicator.IndicatorStatus.PASSIVE)

    # callback: hide indicator app from indicator menu
    def _on_menu_hide(self, menu_item):
        self.indicator.set_status(appindicator.IndicatorStatus.PASSIVE)

    # callback: update indicator app from indicator menu
    def _on_menu_update(self, menu_item):
        self.indicator.set_status(appindicator.IndicatorStatus.PASSIVE)
        with subprocess.Popen([config['terminal'], config['terminal_execute_flag'], config['pkg_update']]) as p:
            p.wait()

    # callback: is application connected to ayatana service
    def _on_connect_changed(self, indicator, connected):
        if (connected == False):
            print('packages missing: ayatana-indicator-application and mate-indicator-applet for MATE or xfce4-indicator-plugin for XFCE not installed')
            self.app.quit()

    # run
    def run(self):
        try:
            exit_status = self.app.run(sys.argv)

            GLib.source_remove(self.timer_source_id)

            return exit_status
        except GLib.Error as e:
            print('Failed to run service: {0} ({1})'.format(e.message, e.code))

        return -1

if __name__ == '__main__':
    updater = AyatanaUpdateNotifier()

    exit_status = updater.run()

    sys.exit(exit_status)

# vim:expandtab
