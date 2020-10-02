def foo(x, y, z, func, *args, **keywords):
	print("para init: ", x, y, z)

	print("para args: ", args)

	print("para keys: ")
	for kw in keywords.keys():
		print(kw, ":", keywords[kw])

	print("------------------------------")
	func(x, y, **keywords)


def main():
	def sub_foo(a, b, **keywords):
		print("para init: ", a, b)

		print("para keys: ")
		for kw in keywords.keys():
			print(kw, ":", keywords[kw])

		print("test key [key1]: ", keywords.get("key1", None))
		print("test key [key6]: ", keywords.get("key6", None))

	foo(1, 2, 3, sub_foo, 4, 5, 6, 7,
	    key1 = "a",
	    key2 = 10,
	    key3 = 1.5)


if __name__ == '__main__':
	main()
