# coding=utf-8


def onetime_exponential_smoothing(prediction_numbers):
    alpha = 1.1
    s1 = sum(prediction_numbers[0:3]) / 3.0
    s_list = [s1]
    for i in range(1, len(prediction_numbers)):
        s = (alpha * prediction_numbers[i] + (1 - alpha) * s_list[i - 1])
        s_list.append(s)

    num = int(round(s_list[len(s_list) - 1]))
    if num < 0:
        num = 0
    return num


def twotimes_exponential_smoothing(prediction_numbers):
    prediction_accumulate_numbers = []
    for i in range(len(prediction_numbers)):
        prediction_accumulate_numbers.append(sum(prediction_numbers[:i + 1]))
    alpha = 0.8
    s1 = prediction_accumulate_numbers[0]
    s2 = prediction_accumulate_numbers[0]
    s1_list = [s1]
    s2_list = [s2]
    for i in range(1, len(prediction_accumulate_numbers)):
        s1 = (alpha * prediction_accumulate_numbers[i] + (1 - alpha) * s1_list[i - 1])
        s2 = alpha * s1 + (1 - alpha) * s2_list[i - 1]
        s1_list.append(s1)
        s2_list.append(s2)

    s1_last = s1_list[len(s1_list) - 1]
    s2_last = s2_list[len(s2_list) - 1]
    a = 2 * s1_last - s2_last
    b = (alpha / (1 - alpha)) * (s1_last - s2_last)

    num = int(round(a + b - prediction_accumulate_numbers[len(prediction_accumulate_numbers) - 1]))

    if num < 0:
        num = 0
    return num


def onetime_exponential_smoothing_enhanced(prediction_numbers):
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
    num = int(round(result[len(result) - 1]))
    if num < 0:
        num = 0
    return num


def twotimes_exponential_smoothing_enhanced(prediction_numbers):
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

    num = int(round(result1[len(result1) - 1]) - prediction_accumulate_numbers[len(prediction_accumulate_numbers) - 1])

    if num < 0:
        num = 0
    return num


def compare(real, prediction):
    sum = 0
    for i in range(len(real) - 1, len(real)):
        sum = sum + pow(real[i] - prediction[i - 1], 2)
    return pow(sum, 0.5)


def onetime_exponential_smoothing_delta(prediction_numbers):
    delta_list = []
    for i in range(1, len(prediction_numbers)):
        delta = prediction_numbers[i] - prediction_numbers[i - 1]
        # if delta < 0:
        #     delta = 0
        delta_list.append(delta)
    alpha = 0.3
    s1 = delta_list[0]
    s_list = [s1]
    for i in range(1, len(delta_list)):
        s = (alpha * delta_list[i] + (1 - alpha) * s_list[i - 1])
        s_list.append(s)

    num = int(round(prediction_numbers[len(prediction_numbers) - 1] + s_list[len(s_list) - 1]))
    if num < 0:
        num = 0
    return num
