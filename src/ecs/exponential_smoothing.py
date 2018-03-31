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


def twotimes_exponential_smoothing(prediction_numbers, date_list, delta):
    date_delta = date_list[1] - date_list[0]
    if date_delta.days != 1:
        t = 1
    else:
        t = delta
    prediction_accumulate_numbers = []
    for i in range(len(prediction_numbers)):
        prediction_accumulate_numbers.append(sum(prediction_numbers[:i + 1]))
    alpha = 1.2
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

    num = int(round(a + b * t - prediction_accumulate_numbers[len(prediction_accumulate_numbers) - 1]))

    if num < 0:
        num = 0
    return num


def onetime_exponential_smoothing_enhanced(prediction_numbers):
    alpha = 0.7
    beta = 0.8
    s1 = prediction_numbers[0]
    s2 = prediction_numbers[1]
    s_list = [s1, s2]
    for i in range(1, len(prediction_numbers)):
        s = (alpha * prediction_numbers[i] + (1 - alpha) * s_list[i - 1] + beta * prediction_numbers[i - 1] + (
            1 - beta) * s_list[i - 2]) / 2
        s_list.append(s)

    num = int(round(s_list[len(s_list) - 1]))
    if num < 0:
        num = 0
    return num
