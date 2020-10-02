#!/Users/kaismbp/virtualenvs/sysEnv/bin python

from Core.terminal_python.Module import MyModule


def main():
	tmp = MyModule("hello, module .. ")
	tmp.foo_01()
	pass


if __name__ == '__main__':
	main()
