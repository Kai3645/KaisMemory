"""
this is a statement for nothing
----------- Dividing line -----------
"""


def foo():
	return


def main():
	# say something
	fr = open("file_io name", 'r')
	fr.close()
	fw = open("file_io name", 'w')
	fw.write("print something .. \n")
	fw.close()

	print(">> process finished ..")
	return


if __name__ == '__main__':
	main()
