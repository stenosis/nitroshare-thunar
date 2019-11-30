"""
The MIT License (MIT)

Copyright (c) 2019 Tim Rieck

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
import json
import requests
import gi
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class MessageBox(QMainWindow):
	"""
	Simple error message box.
	"""

	def __init__(self, txt):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		msg.setText('Error')
		msg.setInformativeText(txt)
		msg.setWindowTitle('Error')
		msg.exec_()

class NitroShareHandler():
	"""
	Handler for menu item "Send with NitroShare" action.
	"""

	def __init__(self):
		nitroShareApiFile = Path(str(Path.home()) + '/.NitroShare')
		if nitroShareApiFile.is_file():
		
			with open(str(nitroShareApiFile), 'r') as f:
				config = json.load(f)

			if len(sys.argv) <= 1:
				# make sure we got an file/dir to send
				app = QtWidgets.QApplication(sys.argv)
				MessageBox('Argument file is missing')

			else:
		   		# determine the input file/dir, port and the NitroShare token
				inputFile = sys.argv[1];
				port = config['port']
				token = config['token']

				# construct the POST request
				payload = {}
				payload['items'] = [inputFile]
				json_data = json.dumps(payload)
				url = 'http://localhost:' + str(port) + '/sendItems'
				hdr = { 'X-Auth-Token' : token }
				req = requests.post(url=url, data=json_data, headers=hdr)

		else:
			app = QtWidgets.QApplication(sys.argv)
			MessageBox('NitroShare API file not found. Make sure NitroShare is up and running.')

if __name__ == "__main__":
	nitroSharehandler = NitroShareHandler()
