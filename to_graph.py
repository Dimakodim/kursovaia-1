import matplotlib.pyplot as mb

f = open("data_sprint.txt").readlines()

data = [(int(x.split(" ")[0]), int(x.split(" ")[1])) for x in f]

data_y = []
data_x = []

for i in data:
    for y in range(len(data_y)):
        data_y[y] += i[0]
    data_y.append(i[0])
    data_y.append(i[0])
    for x in range(len(data_x)):
        data_x[x] += i[1]
    data_x.append(i[1] + 0.001)
    data_x.append(i[1])

data_y.append(0)
data_x.append(0)
data_x.reverse()

print(data_y)
print(data_x)

mb.plot(data_x, data_y)
mb.plot((data_x[0], data_x[-1]), (data_y[0], data_y[-1]))
mb.xlabel("Время, дни")
mb.ylabel("Вес, сторипоинты")
mb.show()