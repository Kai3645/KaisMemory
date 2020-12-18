import csv
import json


def csv_reader(path, hasHead = True):
	with open(path, "r") as fr_csv:
		rows_csv = csv.reader(fr_csv)
		if hasHead: next(rows_csv)
		for row in rows_csv:
			print(row)
			pass


def json_reader(path):
	fr_json = open(path, "r")
	data = json.load(fr_json)[0]["name"]
	for i in data:
		print(data[i]["name"])
	pass


# def file_length_(path, rep = 1):
# 	print("func 01:")  # sys memory killer
# 	t0 = time.time()
# 	for _ in range(rep):
# 		fr = open(path, "r")
# 		count = len(fr.readlines())
# 		print(count)
# 		fr.close()
# 	print("time = " + str(time.time() - t0))
# 	print()
#
# 	print("func 02:")
# 	t0 = time.time()
# 	for _ in range(rep):
# 		fr = open(path, "r")
# 		count = 0
# 		for _ in fr.readlines(): count += 1
# 		print(count)
# 		fr.close()
# 	print("time = " + str(time.time() - t0))
# 	print()
#
# 	print("func 03:")  # best
# 	t0 = time.time()
# 	for _ in range(rep):
# 		fr = open(path, "r")
# 		count = -1
# 		for count, _ in enumerate(fr): pass
# 		count += 1
# 		print(count)
# 		fr.close()
# 	print("time = " + str(time.time() - t0))
# 	print()


# def csv_file_length(path, rep = 1):
# 	file_length(path, rep)
#
# 	print("func 04:")
# 	t0 = time.time()
# 	for _ in range(rep):
# 		fr_csv = open(path, "r")
# 		csv_rows = csv.reader(fr_csv)
# 		count = len(list(csv_rows)) - 1
# 		print(count)
# 		fr_csv.close()
# 	print("time = " + str(time.time() - t0))
# 	print()
