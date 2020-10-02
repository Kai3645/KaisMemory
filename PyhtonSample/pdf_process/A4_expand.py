import copy
from pprint import pprint

import PyPDF2 as pypfd

from Para import KaisPara


def main():
	backs = pypfd.PdfFileReader(f_in + "background.pdf")
	# pprint(backs.documentInfo)
	back = backs.getPage(0)
	back["/Contents"].idnum = 5

	pprint(back)
	# obj = back["/Contents"]
	# pprint(obj)
	# x = obj.getObject()
	# pprint(x)
	print()

	pages = pypfd.PdfFileReader(f_in + "test.pdf")
	pprint(pages.getPage(0))
	print()
	pprint(pages.getPage(2))
	print()

	fw = pypfd.PdfFileWriter()
	fw.addPage(back)

	for i in range(1, 30):
		page = pages.getPage(i)

		pprint(pages.getPage(i))
		print()

		page["/Contents"][0] = back["/Contents"]
		# page["/Resources"] = back["/Resources"]

		fw.addPage(page)

	fw.write(open(KaisPara.f_out + "out.pdf", "wb"))

	pass


if __name__ == '__main__':
	f_in = KaisPara.f_python + "Core/pdf_process/input/"

	main()
