#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import GObject as gobject

import signal #Calling signal for killing application
import os
import urllib.request
import time

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


class JioApp:
	APPINDICATOR_ID = "JioFi2App"
	indicator = None
	icon = os.path.dirname(os.path.realpath(__file__)) + '/jio_blue.png'
	low_battery_icon = 'low_batt.png'
	connected_icon = 'jio_blue.png'
	disconnected_icon = 'jio_red.png'
	refresh_time_in_seconds = 5

	def __init__(self, indicator_id='JioFi2'):
		self.indicator = appindicator.Indicator.new(self.APPINDICATOR_ID, self.icon, appindicator.IndicatorCategory.COMMUNICATIONS)
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)


		

		# Call to loop for checking connection
		self.check_connection()
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		gtk.main()

	def quit(self, source):
		gtk.main_quit()

	def set_icon(self, icon_path):
		self.icon = os.path.dirname(os.path.realpath(__file__)) + '/' + icon_path

	def get_icon(self):
		return self.icon

	def check_connection(self):

		try:
			request = urllib.request.Request("http://jiofi.local.html/")
			urllib.request.urlopen(request,timeout=2)
		except urllib.error.HTTPError as e:
			self.set_icon(self.disconnected_icon)
			#Creating Menu
			self.indicator.set_menu(self.no_connection())
		
		except urllib.error.URLError as e:
			self.set_icon(self.disconnected_icon)
			#Creating Menu
			self.indicator.set_menu(self.no_connection())
		
		else:
			self.set_icon(self.connected_icon)
			#Creating Menu
			self.indicator.set_menu(self.build_menu())	
		

		self.change_app_icon()

	def change_app_icon(self):
		import modules.dev_status as dev_status
		self.indicator.set_label(dev_status.get_batt_status(), "")


		self.indicator.set_icon(self.get_icon())
		gobject.timeout_add_seconds( self.refresh_time_in_seconds, self.check_connection )

	def common_menu(self, menu):

		menu.append(gtk.SeparatorMenuItem())

		item_about = gtk.MenuItem('About')
		item_about.connect('activate', self.onabout)
		menu.append(item_about)

		item_quit = gtk.MenuItem('Quit JioFi2 Indicator') #Label for quit
		item_quit.connect('activate', quit) #call quit function
		menu.append(item_quit)

	def no_connection(self):
		menu = gtk.Menu()
		
		item_no_connection = gtk.MenuItem("Unable to connect to JioFi Device!")
		menu.append(item_no_connection)

		self.common_menu(menu)

		menu.show_all()
		return menu

	def build_menu(self):
		menu = gtk.Menu()
		import modules.dev_status as dev_status
		item_label_battery_status = gtk.MenuItem(dev_status.get_batt_status_full())
		menu.append(item_label_battery_status)

		self.common_menu(menu)

		menu.show_all()
		return menu

	def onabout(self,widget):
		widget.set_sensitive(False)
		ad=gtk.AboutDialog()
		ad.set_logo_icon_name(None)
		ad.set_program_name("JioFi 2 Applet")
		ad.set_name("aboutdialog")
		ad.set_version("Version : 0.1")
		ad.set_license(''+
		'This program is free software: you can redistribute it and/or modify it\n'+
		'under the terms of the GNU General Public License as published by the\n'+
		'Free Software Foundation, either version 3 of the License, or (at your option)\n'+
		'any later version.\n\n'+
		'This program is distributed in the hope that it will be useful, but\n'+
		'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n'+
		'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n'+
		'more details.\n\n'+
		'You should have received a copy of the GNU General Public License along with\n'+
		'this program.  If not, see <http://www.gnu.org/licenses/>.')
		ad.set_authors(['','Kunal Gautam <kunal@abhashtech.com>', 'Anurag Upadhaya <anurag@eanurag.com>', 'Abhash Tech <http://abhashtech.com>'] )
		ad.run()
		ad.destroy()
		widget.set_sensitive(True)


if __name__ == '__main__':
	ap = JioApp('jioapp')
