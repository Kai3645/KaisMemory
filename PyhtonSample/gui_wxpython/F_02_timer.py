import wx


class TestFrame(wx.Frame):
	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

		fileMenu = wx.Menu()
		startItem = fileMenu.Append(
				id = -1,
				item = "start/stop\tCtrl-1",
		)
		menuBar = wx.MenuBar()
		menuBar.Append(menu = fileMenu, title = "&File")
		self.SetMenuBar(menuBar)
		self.Bind(wx.EVT_MENU, self.OnStart, startItem)

		frame_size = self.GetSize()
		pnl = wx.Panel(self)

		self.sbm = wx.StaticBitmap(pnl)

		self.st = wx.StaticText(
				parent = pnl,
				label = "-- waiting --",
				pos = (0, 20),
				size = frame_size,
				style = wx.ALIGN_CENTRE_HORIZONTAL,
		)

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.timer_update, self.timer)

		self.count = 0
		self.flag = True

	def timer_update(self, event):
		self.count += 1
		info = "-- frame = %d --" % self.count
		self.st.SetLabel(info)

	def OnStart(self, event):
		if self.flag:
			self.timer.Start(milliseconds = 30)
			self.flag = False
		else:
			self.timer.Stop()
			self.flag = True


if __name__ == '__main__':
	app = wx.App()
	frm = TestFrame(
			parent = None,
			title = "timer test",
			pos = (30, 50),
	)
	frm.Show()
	app.MainLoop()
