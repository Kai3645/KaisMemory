import wx


class MouseFrame(wx.Frame):
	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

		self.Bind(event = wx.EVT_ENTER_WINDOW, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_LEAVE_WINDOW, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_LEFT_DOWN, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_LEFT_UP, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_LEFT_DCLICK, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MIDDLE_DOWN, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MIDDLE_UP, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MIDDLE_DCLICK, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_RIGHT_DOWN, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_RIGHT_UP, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_RIGHT_DCLICK, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MOUSE_AUX1_DOWN, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MOUSE_AUX1_UP, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MOUSE_AUX1_DCLICK, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MOUSE_AUX2_DOWN, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MOUSE_AUX2_UP, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MOUSE_AUX2_DCLICK, handler = self.mouse_tmp)
		self.Bind(event = wx.EVT_MOTION, handler = self.on_mouse_move)
		self.Bind(event = wx.EVT_MOUSEWHEEL, handler = self.mouse_tmp)

	def mouse_tmp(self, event):
		print(event.GetEventType())
		pass

	def on_mouse_move(self, event):
		if event.Dragging() and event.LeftIsDown():
			pos = event.GetPosition()
			print(pos)


if __name__ == '__main__':
	app = wx.App()
	frm = MouseFrame(
			parent = None,
			title = "mouse test",
			pos = (30, 50),
			size = (720, 480),
	)
	frm.Show()
	app.MainLoop()
