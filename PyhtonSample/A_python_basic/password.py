import random

char_list = "2Aa3Bb4Cc5Dd6Ee7Ff8Gg9Hh" \
            "2Jj3Kk4Mm5Nn6Pp7q8Rr9Ss" \
            "2Tt3Uu4Vv5Ww6Xx7Yy8Zz9"


def create_password(num = 8, count = 5, repeatable = False):
	for _ in range(count):
		n, pw = num, ""
		while n > 0:
			a = random.choice(char_list)
			if a in pw and not repeatable: continue
			pw += a
			n -= 1
		print(pw)


if __name__ == '__main__':
	create_password()
