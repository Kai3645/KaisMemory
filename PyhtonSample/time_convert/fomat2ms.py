from datetime import datetime

if __name__ == '__main__':

	date_src = "20201019_032711"

	t_utc = datetime.strptime(date_src, "%Y%m%d_%H%M%S").timestamp()
	print(t_utc)

	date_dst = datetime.fromtimestamp(t_utc)
	t_str = date_dst.strftime("%Y%m%d%H%M%S%f")
	print(t_str)
