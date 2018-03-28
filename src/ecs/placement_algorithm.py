# coding=utf-8


def placement_algorithm1(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict):
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


def placement_algorithm2(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict):
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


def placement_algorithm3(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict, resource):
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


def placement_algorithm4(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict, resource,
                         flavor_name, flavor_prediction_numbers):
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
    benchmarking = physical_server_CPU / float(physical_server_MEM)
    name_rate = {}
    for fn in flavor_name:
        name_rate[fn] = CPU_dict[fn] / float(MEM_dict[fn])
    name_numbers = dict(zip(flavor_name, flavor_prediction_numbers))
    print "benchmarking", benchmarking
    print "name_rate", name_rate
    print "name_numbers:", name_numbers

    flavor_name_sort_by_rate = []


    epoch = len(name_rate)
    while epoch > 0:
        max_value = 0
        flavor_name_sort_by_rate_temp = []
        for value in name_rate.itervalues():
            if value > max_value:
                max_value = value
        for key, value in name_rate.iteritems():
            if value == max_value and key not in flavor_name_sort_by_rate:
                flavor_name_sort_by_rate.append(key)
                flavor_name_sort_by_rate_temp.append(key)
        for fn in flavor_name_sort_by_rate_temp:
            del name_rate[fn]
        epoch = epoch - 1
    print "flavor_name_sort_by_rate", flavor_name_sort_by_rate



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