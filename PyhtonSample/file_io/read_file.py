import numpy as np


def main():
	path = "/Users/kaismbp/MELCO_save/MMS Sample Data/Output/output_201801060653.n_0843_10Hz.dat"
	fr = open(path, "r")
	count = 10
	for line in fr:
		row = line.split("\t")
		time = np.float64(row[0])
		if time < 539450 - err: continue
		count -= 1
		print(line[:-1])
		if count == 0: break
	fr.close()


if __name__ == '__main__':
	err = 1e-10
	main()
