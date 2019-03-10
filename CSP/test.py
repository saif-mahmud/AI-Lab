x = [1, 2, 3, 4]

with open('test.txt', 'w') as f:
    for item in x:
        f.write("%s\n" % item)
