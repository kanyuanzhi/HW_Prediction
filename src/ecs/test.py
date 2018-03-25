from string_tools import str_to_date
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pylab as plb

fs_test = open("TrainData_1.txt")
train_lines = fs_test.readlines()
fs_test.close()

all_date = []
for line in train_lines:
    date = line.split('\t')[2].split(' ')[0]
    all_date.append(str_to_date(date))

date_count = []
count = 1

date_line = []
last_date = all_date[0]
date_line.append(last_date)

for i in range(1, len(all_date)):
    if all_date[i] == last_date:
        count = count + 1
    else:
        last_date = all_date[i]
        date_line.append(last_date)
        date_count.append(count)
        count = 1
date_count.append(count)

print all_date[0]
print all_date[-1]

print len(date_line)
print len(date_count)

# plb.plot_date(plb.date2num(date_line), date_count, linestyle='-')
# plb.grid(True)
# plb.show()

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.plot(date_line, date_count)
plt.gcf().autofmt_xdate()
plt.show()