import time

import numpy as np
import wx


class TestFrame(wx.Frame):
	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

		size = w, h = 1280, 720
		self.SetSize(w - 1, h + 21)

		img_shape = (size[1], size[0], 3)

		img = np.random.random(img_shape) * 255
		img = np.round(img).astype(np.uint8)
		img = wx.Image(w, h, img)
		self.bit_img = wx.Bitmap(img)

		self.sbm = wx.StaticBitmap(
				parent = self,
				# bitmap = wx.Bitmap(img)
		)

		self.st = wx.StaticText(
				parent = self,
				label = "waiting",
				size = self.GetSize(),
				style = wx.ALIGN_LEFT,
		)

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.timer_update, self.timer)

		fileMenu = wx.Menu()
		startItem = fileMenu.Append(
				id = -1,
				item = "start/stop\tCtrl-1",
		)
		menuBar = wx.MenuBar()
		menuBar.Append(menu = fileMenu, title = "&File")
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.on_start, startItem)

		self.count = 0
		self.flag = True
		self.t = 0

	def timer_update(self, event):
		self.count += 1
		self.sbm.SetBitmap(self.bit_img)
		info = "frame = %d" % self.count
		self.st.SetLabel(info)

		if self.count >= 300:
			dt = (time.time() - self.t)
			print(">> total time = %.4f .. " % dt)
			print(">> fps = %.2f .. " % (300 / dt))

			self.Close(False)

	def on_start(self, event):
		if self.flag:
			self.timer.Start(milliseconds = 200)
			self.flag = False
			self.t = time.time()
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
