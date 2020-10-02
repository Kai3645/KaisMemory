#!/usr/bin/env python
"""
Hello World, but with more meat.
"""

import wx


class HelloFrame(wx.Frame):
	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)
		# self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTIONTEXT))

		# create a panel in the frame
		pnl = wx.Panel(self)

		# put some text with a larger bold font on it
		sub_size = self.GetSize()
		print(sub_size)
		wx.StaticText(
				parent = pnl,
				label = "<< Hello Text!",
				# pos = (20, 20),
				size = sub_size,
				style = wx.ALIGN_LEFT,

		)
		wx.StaticText(
				parent = pnl,
				label = "-- Hello Text! --",
				# pos = (20, 20),
				size = sub_size,
				style = wx.ALIGN_CENTRE_HORIZONTAL,
		)
		wx.StaticText(
				parent = pnl,
				label = "Hello Text! >>",
				# pos = (20, 20),
				size = sub_size,
				style = wx.ALIGN_RIGHT,
		)
		# font = st.GetFont()  # todo: get bug
		# font.PointSize += 10
		# font = font.Bold()
		# st.SetFont(font)

		# and create a sizer to manage the layout of child widgets
		# sizer = wx.BoxSizer(wx.VERTICAL)
		# sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 20))
		# pnl.SetSizer(sizer)

		# create a menu bar
		self.makeMenuBar()

		# and a status bar
		self.CreateStatusBar()
		self.SetStatusText("welcome to wxPython .. ")

	def makeMenuBar(self):
		"""
		A menu bar is composed of menus, which are composed of menu items.
		This method builds a set of menus and binds handlers to be called
		when the menu item is selected.
		"""

		# Make a file menus
		fileMenu = wx.Menu()

		# fileMenu.AppendSeparator() # todo: find why
		exitItem = fileMenu.Append(
				id = wx.ID_EXIT,
				helpString = "Exit",
		)

		aboutItem = fileMenu.Append(
				id = wx.ID_ABOUT,
				helpString = "help string for about"
		)

		helloItem = fileMenu.Append(
				id = -1,  # empty
				item = "&Hello\tCtrl-h",  # short key
				helpString = "help string for hello"
		)

		helpMenu = wx.Menu()

		testItem = helpMenu.Append(
				id = -1,
				item = "test\tCtrl-t",
		)

		menuBar = wx.MenuBar()
		menuBar.Append(menu = fileMenu, title = "&File")
		menuBar.Append(menu = helpMenu, title = "&Help")

		# Give the menu bar to the frame
		self.SetMenuBar(menuBar)

		# Finally, menu event
		self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
		self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
		self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
		self.Bind(wx.EVT_MENU, self.OnTest, testItem)

	def OnExit(self, event):
		"""Close the frame, terminating the application."""
		self.Close()

	def OnHello(self, event):
		"""Say hello to the user."""
		wx.MessageBox(
				message = "Hello again from wxPython",
				parent = self,
		)

	def OnAbout(self, event):
		"""Display an About Dialog"""
		wx.MessageBox(
				caption = "About",
				message = "This is a wxPython Hello World sample",
				style = wx.OK,
				parent = self,
		)

	def OnTest(self, event):
		answer = wx.MessageBox(
				caption = "select",
				message = "yes or no",
				style = wx.YES_NO | wx.CANCEL,
				parent = self,
		)

		if answer == wx.YES:
			print(">> yes ")
			self.OnTest(event)
		elif answer == wx.NO:
			print(">> no ")
			self.Close()
		elif answer == wx.CANCEL:
			print(">> cancel ")
		else:
			print(">> ?? ")
			self.OnTest(event)


if __name__ == '__main__':
	# When this module is run (not imported) then create the app,
	# the frame, show it, and start the event loop.
	app = wx.App()
	frm = HelloFrame(
			parent = None,
			title = "hello, window",
			pos = (30, 50),
			# size = wx.DefaultSize  # (400, 250)
	)
	frm.Show()
	app.MainLoop()
