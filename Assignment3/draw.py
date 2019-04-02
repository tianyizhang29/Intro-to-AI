import numpy as np
import matplotlib.pyplot as plt

data = np.load('./res/q4.npy')

x = []
for i in range(20):
    x.append(i)

# print(sum(data[0]) / 20)
# print(sum(data[1]) / 20)

# plt.xlabel('Index')
# plt.ylabel('# of visited points')
# # plt.title('Comparison of two strategy')
# plt.plot(x, data[0], label='Target in cell')
# plt.plot(x, data[1], label='Target found in cell')
# plt.legend(loc='upper right')
# plt.show()
x = [[1,2]]
print([1,2] in x)