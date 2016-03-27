import matplotlib.pyplot as plt

pt_no = [1,2,3]
coord_x = [6035763.111, 6035765.251, 6035762.801]
coord_y = [6439524.100, 6439522.251, 6439518.298]

fig, ax = plt.subplots()
ax.scatter(coord_y, coord_x, marker='x')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
for i, txt in enumerate(pt_no):
    ax.annotate(txt, (coord_y[i], coord_x[i]))

# ax.format_coord = lambda x, y: "({0:f}, ".format(y) +  "{0:f})".format(x)
plt.show()