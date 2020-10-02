import os

path = r"list.txt"

fr = open(path, 'r')
count = 1
for line in fr.readlines():
    temp_str = line.split(' ')
    img_name = '\"' + (temp_str[-3] + " - " + temp_str[-1])[:-1] + '\"'
    # print(img_name)
    os.system("mv " + img_name + " img_%03d.png" % count)
    count += 1
    # break
