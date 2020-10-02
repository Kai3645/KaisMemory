import wx

from X_support.F_funny.PyWave.C_wave import Wave

window_size = (300, 200)


class TestFrame(wx.Frame):

	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

		fileMenu = wx.Menu()
		startItem = fileMenu.Append(
				id = -1,
				item = "start/stop\tCtrl-1",
		)
		resetItem = fileMenu.Append(
				id = -1,
				item = "reset\tCtrl-2",
		)
		menuBar = wx.MenuBar()
		menuBar.Append(menu = fileMenu, title = "&File")
		self.SetMenuBar(menuBar)

		self.pnl = wx.Panel(self)
		self.sbm = wx.StaticBitmap(self.pnl)
		self.st = wx.StaticText(
				parent = self.pnl,
				label = "waiting",
				size = self.GetSize(),
				style = wx.ALIGN_LEFT,
		)
		self.pnl.Bind(wx.EVT_LEFT_DOWN, self.on_click)

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_MENU, self.on_start, startItem)
		self.Bind(wx.EVT_MENU, self.on_reset, resetItem)
		self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
		self.Bind(wx.EVT_CLOSE, self.on_close)

		self.count = 0
		self.flag = True

	wave = Wave(
			bit_size = (100, 150),
			img_size = window_size,
			K = 0.5,
			num = 0,
			dampening = 1 - 1e-9,
	)

	def on_timer(self, event):
		self.wave.update()
		img = self.wave.push_img()
		h, w, _ = img.shape
		img = wx.Image(w, h, img)
		self.sbm.SetBitmap(wx.Bitmap(img))

		self.count += 1
		info = "frame = %d" % self.count
		self.st.SetLabel(info)

	def on_close(self, event):
		self.timer.Stop()
		self.Destroy()

	def on_start(self, event):
		if self.flag:
			self.timer.Start(milliseconds = 35)
			self.flag = False
		else:
			self.timer.Stop()
			self.flag = True

	def on_reset(self, event):
		self.wave.reset()

	def on_click(self, event):
		pos = event.GetPosition()
		print(pos)
		self.wave.C_push_ripple(pos)


if __name__ == '__main__':
	app = wx.App()
	frm = TestFrame(
			parent = None,
			title = "wave test",
			pos = (30, 50),
			size = (window_size[0] - 1, window_size[1] + 21),
	)
	frm.Show()
	app.MainLoop()
