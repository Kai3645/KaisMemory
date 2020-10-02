class MyModule:
	def __init__(self, sth):
		self.a = sth
		pass

	def __str__(self):
		return str(self.a)

	def foo_01(self):
		print("foo 01 .. ")
		print(self)
