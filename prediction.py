f = open('TrainData_2015.1.1_2015.2.19.txt')
data = f.readlines()

dataMatrix = []
for d in data:
    dataMatrix.append(d.split('\t'))

startDate = dataMatrix[0][2].split(' ')[0]
endDate = dataMatrix[len(dataMatrix) - 1][2].split(' ')[0]

print dataMatrix
flavorName = []
flavorNameTemp = []
flavorID = []

for d in dataMatrix:
    if (d[1] not in flavorNameTemp):
        flavorNameTemp.append(d[1])
        flavorID.append(int(d[1][6:]))

flavorID.sort()
for i in flavorID:
    for fname in flavorNameTemp:
        if int(fname[6:]) == i:
            flavorName.append(fname)
