import urllib.request
from xml.etree import ElementTree
import time


def rshift(val, n): return val>>n if val >= 0 else (val+0x100000000)>>n

def get_batt_status():
	try:
		url = "http://jiofi.local.html/st_dev.w.xml"
		request = urllib.request.Request(url)
		urllib.request.urlopen(request)
	except urllib.error.HTTPError as e:
		bat_val = "N/A"
	except urllib.error.URLError as e:
		bat_val = "N/A"
	else:
		response = urllib.request.urlopen(request,timeout=2)
		xml = response.read()
		batt_per = ElementTree.XML(xml).find("batt_per").text
		batt_status = rshift(int(ElementTree.XML(xml).find("batt_st").text),8)
		if batt_status < 4 :
			status = "D"

		if batt_status == 4 :
			status = "C"

		if batt_status == 5 :
			status = "F"

		bat_val = batt_per + "%(" + status + ")"
	return bat_val

def get_batt_status_full():
	try:
		url = "http://jiofi.local.html/st_dev.w.xml"
		request = urllib.request.Request(url)
		urllib.request.urlopen(request)
	except urllib.error.HTTPError as e:
		bat_val = "N/A"
	except urllib.error.URLError as e:
		bat_val = "N/A"
	else:
		response = urllib.request.urlopen(request,timeout=2)
		xml = response.read()
		batt_per = ElementTree.XML(xml).find("batt_per").text
		batt_status = rshift(int(ElementTree.XML(xml).find("batt_st").text),8)
		if batt_status < 4 :
			status = "Discharging"

		if batt_status == 4 :
			status = "Charging"

		if batt_status == 5 :
			status = "is Fully charged"

		bat_val = "Battery is at " + batt_per + "% "+"and " + status
	return bat_val
