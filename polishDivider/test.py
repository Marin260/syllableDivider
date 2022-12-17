with open("needed_res.txt") as f:
    x = [x.rstrip("\n") for x in f.readlines()]

with open("./output/test_output.txt") as f:
    y = [x.rstrip("\n") for x in f.readlines()]
revision = []
#print(*x, sep="\n")
counter = 0
for i in range(len(x)):
    if x[i] == y[i]:
        counter += 1
    else:
        revision.append(y[i] + " | should be? -> |" + x[i])

with open('./output/revision.txt', 'w') as f:
        for item in revision:
            # write each item on a new line
            f.write("%s\n" % item)
print(counter)