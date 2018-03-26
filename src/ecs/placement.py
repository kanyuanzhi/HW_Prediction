# coding=utf-8
from readtxt import InputTxtProcess
from writetxt import generate_output
import random


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
    print resource_used
    print resource_used_rate


def __placement_algorithm1(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict):
    """
    分配算法1
    :param flavor_queue: 待分配的所有flavor序列
    :param physical_server_CPU: 物理服务器CPU总大小
    :param physical_server_MEM: 物理服务器MEM总大小
    :param CPU_dict: flavor与CPU的映射字典
    :param MEM_dict: flavor与MEM的映射字典
    :return:
    """
    physical_server_cluster = []
    physical_server_cluster_resource_left = []  # 集群中各服务器资源剩余情况

    physical_server = {}
    residual_CPU = physical_server_CPU
    residual_MEM = physical_server_MEM
    for fq in flavor_queue:
        flag = False
        if CPU_dict[fq] <= residual_CPU and MEM_dict[fq] <= residual_MEM:
            residual_CPU = residual_CPU - CPU_dict[fq]
            residual_MEM = residual_MEM - MEM_dict[fq]
            if fq in physical_server:
                physical_server[fq] = physical_server[fq] + 1
            else:
                physical_server[fq] = 1
        else:
            if len(physical_server_cluster_resource_left) != 0:
                for index, resource_left in enumerate(physical_server_cluster_resource_left):
                    if CPU_dict[fq] <= resource_left[0] and MEM_dict[fq] <= resource_left[1]:
                        flag = True
                        physical_server_cluster_resource_left[index][0] = resource_left[0] - CPU_dict[fq]
                        physical_server_cluster_resource_left[index][1] = resource_left[1] - MEM_dict[fq]
                        if fq in physical_server_cluster[index]:
                            physical_server_cluster[index][fq] = physical_server_cluster[index][fq] + 1
                        else:
                            physical_server_cluster[index][fq] = 1
                        break
            if not flag:
                physical_server_cluster.append(physical_server)
                physical_server_cluster_resource_left.append([residual_CPU, residual_MEM])
                physical_server = {}
                physical_server[fq] = 1
                residual_CPU = physical_server_CPU - CPU_dict[fq]
                residual_MEM = physical_server_MEM - MEM_dict[fq]
    physical_server_cluster.append(physical_server)
    physical_server_cluster_resource_left.append([residual_CPU, residual_MEM])
    print physical_server_cluster
    print physical_server_cluster_resource_left

    return physical_server_cluster


def __placement_algorithm2(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict):
    physical_server = {}
    physical_server_cluster = [physical_server]
    residual_CPU = physical_server_CPU
    residual_MEM = physical_server_MEM
    physical_server_cluster_resource_left = [[physical_server_CPU, physical_server_MEM]]  # 集群中各服务器资源剩余情况

    for fq in flavor_queue:
        flag = False
        for index, resource_left in enumerate(physical_server_cluster_resource_left):
            if CPU_dict[fq] <= resource_left[0] and MEM_dict[fq] <= resource_left[1]:
                physical_server_cluster_resource_left[index][0] = physical_server_cluster_resource_left[index][0] - \
                                                                  CPU_dict[fq]
                physical_server_cluster_resource_left[index][1] = physical_server_cluster_resource_left[index][1] - \
                                                                  MEM_dict[fq]
                flag = True
                if fq in physical_server_cluster[index]:
                    physical_server_cluster[index][fq] = physical_server_cluster[index][fq] + 1
                else:
                    physical_server_cluster[index][fq] = 1
                break
        if not flag:
            physical_server_cluster_resource_left.append(
                [physical_server_CPU - CPU_dict[fq], physical_server_MEM - MEM_dict[fq]])
            physical_server_cluster.append({fq: 1})
    print physical_server_cluster
    print physical_server_cluster_resource_left
    return physical_server_cluster


def __placement_algorithm3(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict, resource):
    """
    伪贪心算法
    :param flavor_queue:
    :param physical_server_CPU:
    :param physical_server_MEM:
    :param CPU_dict:
    :param MEM_dict:
    :param resource :优化目标资源CPU或MEM
    :return:
    """
    physical_server = {}
    physical_server_cluster = []
    residual_CPU = physical_server_CPU
    residual_MEM = physical_server_MEM
    resource_dict = {"CPU": CPU_dict, "MEM": MEM_dict}[resource]
    for i in range(1, len(flavor_queue)):
        current_flavor = flavor_queue[i]
        for j in range(i)[::-1]:
            if resource_dict[current_flavor] < resource_dict[flavor_queue[j]]:
                temp = flavor_queue[j]
                flavor_queue[j] = current_flavor
                flavor_queue[j + 1] = temp
    for fq in flavor_queue:
        if CPU_dict[fq] <= residual_CPU and MEM_dict[fq] <= residual_MEM:
            residual_CPU = residual_CPU - CPU_dict[fq]
            residual_MEM = residual_MEM - MEM_dict[fq]
            if fq in physical_server:
                physical_server[fq] = physical_server[fq] + 1
            else:
                physical_server[fq] = 1
        else:
            physical_server_cluster.append(physical_server)
            physical_server = {}
            physical_server[fq] = 1
            residual_CPU = physical_server_CPU - CPU_dict[fq]
            residual_MEM = physical_server_MEM - MEM_dict[fq]
    physical_server_cluster.append(physical_server)
    return physical_server_cluster


def placement(input_lines, flavor_prediction_numbers):
    itp = InputTxtProcess(input_lines)
    resource_name = itp.resource_name()
    physical_server_specification = itp.physical_server_specification()
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
    # random.shuffle(flavor_queue)
    # print flavor_queue
    # flavor_queue = ['flavor12', 'flavor11', 'flavor9', 'flavor9', 'flavor11', 'flavor9', 'flavor14',
    #                 'flavor14', 'flavor15', 'flavor14', 'flavor11', 'flavor9', 'flavor10', 'flavor13',
    #                 'flavor12', 'flavor9', 'flavor15', 'flavor11', 'flavor14', 'flavor14']
    # physical_server_cluster1 = __placement_algorithm1(flavor_queue, physical_server_CPU, physical_server_MEM,
    #                                                  CPU_dict,
    #                                                  MEM_dict)
    # physical_server_cluster = __placement_algorithm2(flavor_queue, physical_server_CPU, physical_server_MEM,
    #                                                  CPU_dict, MEM_dict)

    physical_server_cluster = __placement_algorithm3(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict,
                                                     MEM_dict, resource_name)

    # __resource_used_watch(physical_server_cluster1, CPU_dict, MEM_dict, physical_server_CPU, physical_server_MEM)
    # __resource_used_watch(physical_server_cluster, CPU_dict, MEM_dict, physical_server_CPU, physical_server_MEM)
    # print flavor_prediction_numbers

    return generate_output(flavor_name, flavor_prediction_numbers, physical_server_cluster)
