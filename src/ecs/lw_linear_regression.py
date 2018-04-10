# coding=utf8
import matplotlib.pyplot as plt
from numpy import *


class lwlrclass:
    def __init__(self, data_series):
        self.data_series_new = []
        for i in range(len(data_series)):
            self.data_series_new.append(sum(data_series[:i + 1]))

    def get_data_series_new(self):
        return self.data_series_new


def lwlr(testPoint, xArr, yArr, k=1.0):
    # 读入数据并创建所需矩阵
    xMat = mat(xArr).T
    yMat = mat(yArr).T
    # np.shape()函数计算传入矩阵的维数
    m = shape(xMat)[0]
    # 权重，创建对角矩阵，维数与xMat维数相同
    weights = mat(eye((m)))  # m维的单位对角矩阵
    '''
    权重矩阵是一个方阵,阶数等于样本点个数。也就是说,该矩阵为每个样本点初始
        化了一个权重。接着,算法将遍历数据集,计算每个样本点对应的权重值,
    '''
    for j in range(m):
        diffMat = testPoint - xMat[j, :]
        # 采用高斯核函数进行权重赋值，样本附近点将被赋予更高权重
        weights[j, j] = exp(diffMat * diffMat.T / (-2.0 * k ** 2))
    xTx = xMat.T * (weights * xMat)  # (2*2) = (2*n) * ( (n*n)*(n*2) )
    if linalg.det(xTx) == 0.0:
        print ("This matrix is singular,cannot do inverse")
        return
    ws = xTx.I * (xMat.T * (weights * yMat))  # (2*1) = (2*2) * ( (2*n) * (n*n) * (n*1))
    # print(ws)
    return testPoint * ws


# 样本点依次做局部加权
def lwlrTest(testArr, xArr, yArr, k=1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):  # 为样本中每个点，调用lwlr()函数计算ws值以及预测值yHat
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat


def twotimes_exponential_smoothing(prediction_numbers):
    prediction_accumulate_numbers = []
    for i in range(len(prediction_numbers)):
        prediction_accumulate_numbers.append(sum(prediction_numbers[:i + 1]))
    alpha = 0.001
    minsse = 10000.0
    while alpha < 1.5:
        s1 = prediction_accumulate_numbers[0]
        s2 = prediction_accumulate_numbers[0]
        s1_list = [s1]
        s2_list = [s2]
        for i in range(1, len(prediction_accumulate_numbers)):
            s1 = (alpha * prediction_accumulate_numbers[i] + (1 - alpha) * s1_list[i - 1])
            s2 = alpha * s1 + (1 - alpha) * s2_list[i - 1]
            s1_list.append(s1)
            s2_list.append(s2)

        result = []
        for i in range(len(s1_list)):
            s1 = s1_list[i]
            s2 = s2_list[i]
            a = 2 * s1 - s2
            b = (alpha / (1 - alpha)) * (s1 - s2)
            result.append(a + b)
        sse = compare(prediction_accumulate_numbers, result)
        if minsse > sse:
            minsse = sse
            result1 = result
            bestalpha = alpha
        alpha = alpha + 0.001
    print bestalpha
    print result1
    print prediction_accumulate_numbers
    return result1


def onetime_exponential_smoothing(prediction_numbers):
    minsse = 10000
    alpha = 0.1
    result = []
    while alpha <= 1.5:
        s1 = sum(prediction_numbers[0:3]) / 3.0
        s_list = [s1]
        for i in range(1, len(prediction_numbers)):
            s = (alpha * prediction_numbers[i] + (1 - alpha) * s_list[i - 1])
            s_list.append(s)
        sse = compare(prediction_numbers, s_list)
        if minsse > sse:
            minsse = sse
            result = s_list
            bestalpha = alpha
        alpha = alpha + 0.01
    print bestalpha
    return result


def compare(real, prediction):
    sum = 0
    for i in range(len(real)-1, len(real)):
        sum = sum + pow(real[i] - prediction[i-1], 2)
    return pow(sum, 0.5)


if __name__ == "__main__":
    data_series1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0022447411707178008, 1.6983674012193175, 1.25467416953602,
                    0.06215804681523405, 2.26014745678547, 0.722314000258019, 0.0012165548005811046, 0.8459462225177903,
                    1.0001883684304445, 2.418704655117109, 1.8869598621813901, 0.8459561505825489,
                    0.0012165548005811048,
                    0.6417996539274076, 2.9464625022916193, 2.044545175773018, 2.2021894781335978, 3.416638935567579,
                    3.847867239807609, 3.063275453368214]
    data_series2 = [2.0534333854284, 0.0012215188329604634, 0.01743939470890965, 1.8931332291432006, 0.135263434807194,
                    1.793645135739508, 2.5864545980184457, 2.2490174778885046, 3.870902260071695, 11.36666494343233,
                    0.08747952619021486, 0.0, 0.008719697354454825, 0.9465666145716003, 0.04471368807394504,
                    4.964032379359032e-06,
                    0.3670142276422695, 1.2144074850195377, 16.079797910366793, 5.622949754149927, 13.68605814397561,
                    12.593995925074665, 6.253461987473333, 9.167978051984235, 4.009842067939814]
    x2 = [i for i in range(len(data_series2))]
    lwlr11 = lwlrclass(data_series2)
    data_series_new = lwlr11.get_data_series_new()
    # result1 = onetime_exponential_smoothing(data_series1)
    result2 = twotimes_exponential_smoothing(data_series2)
    # y2 = lwlrTest(x2, x2, lwlr11.get_data_series_new(), 1)

    plt.figure("data & model")
    plt.plot(x2, result2)
    plt.scatter(x2, data_series_new)
    plt.show()
