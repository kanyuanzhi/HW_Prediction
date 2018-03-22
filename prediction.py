# *coding=utf8
from data_process import data_process
import matplotlib.pyplot as plt

period_data = data_process()
print period_data
for ps in period_data:
    print ps[2]
    print ps[0]
    print ps[1]
    plt.plot(ps[1], label=ps[2], linestyle="-")

plt.legend(loc='upper left')
plt.show()
