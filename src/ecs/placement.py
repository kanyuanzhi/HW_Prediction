# coding=utf-8
from readtxt import InputTxtProcess
from writetxt import generate_output
from placement_algorithm import *
import random
import math


def __resource_used_watch(physical_server_cluster, CPU_dict, MEM_dict, physical_server_CPU, physical_server_MEM):
    """
    查看各物理服务器资源使用情况
    :param physical_server_cluster:
    :param CPU_dict:
    :param MEM_dict:
    :param physical_server_CPU:
    :param physical_server_MEM:
    :return:
    """
    resource_used = []
    resource_used_rate = []
    for psc in physical_server_cluster:
        psc_CPU = 0
        psc_MEM = 0
        physical_server = psc.items()
        for ps in physical_server:
            psc_CPU = psc_CPU + CPU_dict[ps[0]] * ps[1]
            psc_MEM = psc_MEM + MEM_dict[ps[0]] * ps[1]
        psc_CPU_rate = round(psc_CPU / float(physical_server_CPU), 4)
        psc_MEM_rate = round(psc_MEM / float(physical_server_MEM), 4)
        resource_used_rate.append([psc_CPU_rate, psc_MEM_rate])
        resource_used.append([psc_CPU, psc_MEM])
    server_numbers = len(resource_used)
    CPU_total = server_numbers * physical_server_CPU
    MEM_total = server_numbers * physical_server_MEM
    CPU_used = 0.0
    MEM_used = 0.0
    for ru in resource_used:
        CPU_used = CPU_used + ru[0]
        MEM_used = MEM_used + ru[1]
    # print "CPU used rate =", round(CPU_used / CPU_total, 4)
    # print "MEM used rate =", round(MEM_used / MEM_total, 4)
    # print resource_used
    # print resource_used_rate

    server_numbers_min = max(math.ceil(CPU_used / physical_server_CPU), math.ceil(MEM_used / physical_server_MEM))
    CPU_used_rate_max = round(CPU_used / (server_numbers_min * physical_server_CPU), 4)
    MEM_used_rate_max = round(MEM_used / (server_numbers_min * physical_server_MEM), 4)
    print "CPU当前利用率 =", round(CPU_used / CPU_total, 4)
    print "CPU最大利用率 =", CPU_used_rate_max
    print "MEM当前利用率 =", round(MEM_used / MEM_total, 4)
    print "MEM最大利用率 =", MEM_used_rate_max
    print "物理服务器当前使用个数 =", server_numbers
    print "物理服务器最小使用个数 =", server_numbers_min

    return round(CPU_used / CPU_total, 4)


def placement(input_lines, flavor_prediction_numbers):
    itp = InputTxtProcess(input_lines)
    resource_name = itp.resource_name()
    physical_server_specification = itp.physical_server_specification()
    flavor_selected = itp.flavor_selected()
    flavor_specification = itp.flavor_specification()

    physical_server_CPU = int(physical_server_specification[0])  # 物理服务器CPU数量
    physical_server_MEM = int(physical_server_specification[1])  # 物理服务器内存大小

    flavor_name = []
    flavor_CPU = []
    flavor_MEM = []
    for fs in flavor_specification:
        flavor_name.append(fs[0])
        flavor_CPU.append(int(fs[1]))
        flavor_MEM.append(int(fs[2]) / 1024)
    CPU_dict = dict(zip(flavor_name, flavor_CPU))
    MEM_dict = dict(zip(flavor_name, flavor_MEM))

    # flavor_prediction_numbers = [45, 12, 53, 50, 30]  # 预测数量

    flavor_queue = []
    flavor_total = 0  # flavor总数
    for i, fn in enumerate(flavor_prediction_numbers):
        flavor_total = flavor_total + fn
        current_flavor_name = flavor_name[i]
        flavor_queue = flavor_queue + [current_flavor_name] * fn
    # print flavor_name
    # print flavor_queue
    random.shuffle(flavor_queue)
    # print flavor_queue
    # flavor_queue = ['flavor12', 'flavor11', 'flavor9', 'flavor9', 'flavor11', 'flavor9', 'flavor14',
    #                 'flavor14', 'flavor15', 'flavor14', 'flavor11', 'flavor9', 'flavor10', 'flavor13',
    #                 'flavor12', 'flavor9', 'flavor15', 'flavor11', 'flavor14', 'flavor14']
    # physical_server_cluster1 = placement_algorithm1(flavor_queue, physical_server_CPU, physical_server_MEM,
    #                                                  CPU_dict,
    #                                                  MEM_dict)
    # physical_server_cluster1 = placement_algorithm2(flavor_queue, physical_server_CPU, physical_server_MEM,
    #                                                CPU_dict, MEM_dict)
    #
    # print len(physical_server_cluster1)
    # physical_server_cluster = placement_algorithm_SA(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict,
    #                                                  MEM_dict, resource_name)
    result = placement_algorithm_SA_enhancement(flavor_queue, physical_server_CPU, physical_server_MEM,
                                                CPU_dict, MEM_dict, resource_name, flavor_name,
                                                flavor_prediction_numbers)

    physical_server_cluster = result[0]
    print physical_server_cluster
    flavor_prediction_numbers = result[1]
    print flavor_prediction_numbers
    # rate_temp = 0
    # for i in range(100000):
    #     random.shuffle(flavor_queue)
    #     physical_server_cluster = placement_algorithm1(flavor_queue, physical_server_CPU, physical_server_MEM,
    #                                                     CPU_dict,
    #                                                     MEM_dict)
    #     rate = __resource_used_watch(physical_server_cluster, CPU_dict, MEM_dict, physical_server_CPU,
    #                                  physical_server_MEM)
    #     if rate > rate_temp:
    #         rate_temp = rate
    #     print rate_temp

    # physical_server_cluster = placement_algorithm3(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict,
    #                                                  MEM_dict, resource_name)
    # physical_server_cluster = placement_algorithm3_enhance(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict,
    #                                                  MEM_dict, resource_name)
    # placement_algorithm4(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict, resource_name,
    #                     flavor_name, flavor_prediction_numbers)

    # __resource_used_watch(physical_server_cluster1, CPU_dict, MEM_dict, physical_server_CPU, physical_server_MEM)
    __resource_used_watch(physical_server_cluster, CPU_dict, MEM_dict, physical_server_CPU, physical_server_MEM)
    # print flavor_prediction_numbers

    return generate_output(flavor_name, flavor_prediction_numbers, physical_server_cluster)
