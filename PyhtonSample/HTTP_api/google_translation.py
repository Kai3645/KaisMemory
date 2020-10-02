import json
import requests


def translate(src: str, sl: str, tl: str, *, debug_mode: bool = False):
	"""
	@param src: sentence to be translated
	@param sl: input language code
	@param tl: output language code
	@param debug_mode: default False
	@return: translated sentence
	"""
	res = requests.get(
		url = "https://translate.google.com/translate_a/single",
		headers = {
			"Host": "translate.google.com",
			"Accept": "*/*",
			# "Cookie": "",
			"User-Agent": "GoogleTranslate/5.9.59004",
			# "Accept-Language": "",
			"Accept-Encoding": "gzip, deflate",
			"Connection": "close",
		}, params = {
			"client": "it",
			"dt": ["t", "rmt", "bd", "rms", "qca", "ss", "md", "ld", "ex"],
			"otf": "2",
			"dj": "1",
			"q": src,
			# "hl": "",
			# "ie": "",
			# "oe": "",
			"sl": sl,
			"tl": tl,
		},
	).json()
	if debug_mode: print(json.dumps(res, indent = 4))
	return res["sentences"][0]["trans"]


if __name__ == '__main__':
	"""
		English   : en
		Chinese   : zh / zh-CN
		Japanese  : ja
		Esperanto : eo
		French    : fr
		German    : de
		Korean    : ko
		Russian   : ru
	"""
	import sys

	args = sys.argv
	argc = len(args)
	if argc < 3:
		print("unknown input")
		exit(1)

	print(translate(src = " ".join(args[3:]), sl = args[1], tl = args[2]))
