import csv

import numpy as np

from b_KaisCore._a_global_para import KaisPara


def calc_AB(mat22, vector2):
	AB = np.linalg.inv(mat22) * vector2
	return AB[0, 0], AB[1, 0]


def calc_normal_sub(pos2, pos1, rule):
	mat = np.asmatrix([[pos1[rule[0]], pos1[rule[1]]], [pos2[rule[0]], pos2[rule[1]]]])
	vector = np.asmatrix([[-1 * pos1[rule[2]]], [-1 * pos2[rule[2]]]])
	if KaisPara.error * -1 < np.linalg.det(mat) < KaisPara.error: return None
	a, b = calc_AB(mat, vector)
	
	normal = np.asmatrix(np.zeros((3, 1)))
	normal[rule[0], 0] = a
	normal[rule[1], 0] = b
	normal[rule[2], 0] = 1
	
	r = np.linalg.norm(normal)
	return normal / r


def calc_normal(pos2, pos1):
	rule_list = ((0, 1, 2),
	             (1, 2, 0),
	             (2, 0, 1))
	for rule in rule_list:
		normal = calc_normal_sub(pos1, pos2, rule)
		if normal is not None: return normal
	return None


def main():
	path = "L:/MELCO data/MMS Data/objects/roadMarking.csv"
	with open(path, "r") as fr_csv:
		rows_csv = csv.reader(fr_csv)
		for i, row in enumerate(rows_csv):
			pos0 = np.asarray(row[0:3], dtype = np.float64)
			pos1 = np.asarray(row[4:7], dtype = np.float64) - pos0
			pos2 = np.asarray(row[8:11], dtype = np.float64) - pos0
			pos3 = np.asarray(row[12:15], dtype = np.float64) - pos0
			print(row[16], end = ", ")
			
			normal = calc_normal(pos1, pos2)
			if normal is None:
				print("is None .. ")
				continue
			
			err = ((np.asmatrix(pos1) * normal)[0, 0],
			       (np.asmatrix(pos2) * normal)[0, 0],
			       (np.asmatrix(pos3) * normal)[0, 0])
			
			if abs(max(err)) < 0.0001: print("-------", end = " ")
			else: print("False, ", end = " ")
			
			print(err[0], end = ", ")
			print(err[1], end = ", ")
			print(err[2], end = ", ")
			print()


if __name__ == '__main__':
	main()
