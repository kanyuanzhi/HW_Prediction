# coding=utf-8


import random
import math


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
    # print physical_server_cluster
    # print physical_server_cluster_resource_left
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


def placement_algorithm3_enhance(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict, resource):
    """
    :param flavor_queue:
    :param physical_server_CPU:
    :param physical_server_MEM:
    :param CPU_dict:
    :param MEM_dict:
    :param resource :优化目标资源CPU或MEM
    :return:
    """
    physical_server = {}
    physical_server_cluster = [physical_server]
    residual_CPU = physical_server_CPU
    residual_MEM = physical_server_MEM
    resource_dict = {"CPU": CPU_dict, "MEM": MEM_dict}[resource]
    physical_server_cluster_resource_left = [[physical_server_CPU, physical_server_MEM]]  # 集群中各服务器资源剩余情况
    for i in range(1, len(flavor_queue)):
        current_flavor = flavor_queue[i]
        for j in range(i)[::-1]:
            if resource_dict[current_flavor] > resource_dict[flavor_queue[j]]:
                temp = flavor_queue[j]
                flavor_queue[j] = current_flavor
                flavor_queue[j + 1] = temp
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

    # if CPU_dict[fq] <= residual_CPU and MEM_dict[fq] <= residual_MEM:
    #         residual_CPU = residual_CPU - CPU_dict[fq]
    #         residual_MEM = residual_MEM - MEM_dict[fq]
    #         if fq in physical_server:
    #             physical_server[fq] = physical_server[fq] + 1
    #         else:
    #             physical_server[fq] = 1
    #     else:
    #         physical_server_cluster.append(physical_server)
    #         physical_server = {}
    #         physical_server[fq] = 1
    #         residual_CPU = physical_server_CPU - CPU_dict[fq]
    #         residual_MEM = physical_server_MEM - MEM_dict[fq]
    # physical_server_cluster.append(physical_server)
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


def placement_algorithm_SA(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict, resource):
    """
    Simulated Annealing模拟退火
    :param flavor_queue:
    :param physical_server_CPU:
    :param physical_server_MEM:
    :param CPU_dict:
    :param MEM_dict:
    :param resource:
    :param flavor_name:
    :param flavor_prediction_numbers:
    :return:
    """
    SA_T = 1000
    SA_T_min = 1
    r = 0.9999
    length = len(flavor_queue)
    mark_min = length
    physical_server_cluster_final = []
    physical_server_cluster_final2 = []
    resource_dict = {"CPU": CPU_dict, "MEM": MEM_dict}[resource]
    mark_temp = 0
    mark_temp_min = 1000
    # for i in range(1, len(flavor_queue)):
    #     current_flavor = flavor_queue[i]
    #     for j in range(i)[::-1]:
    #         if resource_dict[current_flavor] < resource_dict[flavor_queue[j]]:
    #             temp = flavor_queue[j]
    #             flavor_queue[j] = current_flavor
    #             flavor_queue[j + 1] = temp
    dice = []
    for i in range(len(flavor_queue)):
        dice.append(i)

    while SA_T > SA_T_min:
        flavor_queue_new = flavor_queue[:]
        random.shuffle(dice)
        flavor1 = flavor_queue_new[dice[0]]
        flavor2 = flavor_queue_new[dice[1]]
        flavor_queue_new[dice[0]] = flavor2
        flavor_queue_new[dice[1]] = flavor1
        # index1 = random.randint(0, length - 1)
        # index2 = random.randint(0, length - 1)
        # flavor1 = flavor_queue_new[index1]
        # flavor2 = flavor_queue_new[index2]
        # flavor_queue_new[index1] = flavor2
        # flavor_queue_new[index2] = flavor1


        physical_server = {}
        physical_server_cluster = [physical_server]
        residual_CPU = physical_server_CPU
        residual_MEM = physical_server_MEM
        physical_server_cluster_resource_left = [[physical_server_CPU, physical_server_MEM]]  # 集群中各服务器资源剩余情况

        for fq in flavor_queue_new:
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

        physical_server_numbers = len(physical_server_cluster_resource_left) - 1
        target_resource = {"CPU": physical_server_CPU, "MEM": physical_server_MEM}[resource]
        target_resource_index = {"CPU": 0, "MEM": 1}[resource]
        last_rate = physical_server_cluster_resource_left[physical_server_numbers][target_resource_index] / float(
            target_resource)

        # mark = 1
        # for resource_left in physical_server_cluster_resource_left:
        #     mark = mark*(1-resource_left[target_resource_index]/float(target_resource))
        mark = physical_server_numbers + last_rate
        mark_temp = mark
        if mark_temp < mark_temp_min:
            mark_temp_min = mark_temp
            physical_server_cluster_final2 = physical_server_cluster
        # if mark - 33.14285 <0.0000001:
        #     print physical_server_cluster_resource_left
        #     print len(physical_server_cluster_resource_left)
        #     print len(physical_server_cluster_final)
        #     break
        if mark < mark_min:
            # physical_server_cluster_final = physical_server_cluster
            mark_min = mark
            flavor_queue = flavor_queue_new
        else:
            # p = 1 / (1 + math.exp(-(mark - mark_min) / SA_T))
            p = math.exp((mark_min - mark) / SA_T)
            if random.random() > p:
                # physical_server_cluster_final = physical_server_cluster
                mark_min = mark
                flavor_queue = flavor_queue_new
        print mark_min
        print round(SA_T, 1)
        SA_T = SA_T * r
    # print physical_server_cluster_resource_left
    print mark_temp_min
    # print physical_server_cluster_final
    return physical_server_cluster_final2


def placement_algorithm_SA_enhancement(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict,
                                       resource, flavor_name, flavor_prediction_numbers):
    """
    Simulated Annealing模拟退火增强版
    :param flavor_queue:
    :param physical_server_CPU:
    :param physical_server_MEM:
    :param CPU_dict:
    :param MEM_dict:
    :param resource:
    :param flavor_name:
    :param flavor_prediction_numbers:
    :return:
    """
    SA_T = 100
    SA_T_min = 1
    r = 0.9999
    length = len(flavor_queue)
    mark_min = length
    physical_server_cluster_final = []

    mark_temp = 0
    mark_temp_min = 10000
    dice = []
    for i in range(len(flavor_queue)):
        dice.append(i)

    flavor_information = []
    for i in range(len(flavor_name)):
        item = {'name': flavor_name[i], 'numbers': flavor_prediction_numbers[i], 'cpu': CPU_dict[flavor_name[i]],
                'mem': MEM_dict[flavor_name[i]],
                'cpu_mem': CPU_dict[flavor_name[i]] / float(MEM_dict[flavor_name[i]]),
                'mem_cpu': MEM_dict[flavor_name[i]] / float(CPU_dict[flavor_name[i]])}
        flavor_information.append(item)
    flavor_information.sort(key=lambda x: (x['numbers']), reverse=True)

    backup_flavor = flavor_information[:4]
    backup_flavor.sort(key=lambda x: (x["cpu"]))

    max_cpu_mem_all = max(flavor_information, key=lambda x: x['cpu_mem'])['cpu_mem']
    max_mem_cpu_all = max(flavor_information, key=lambda x: x['mem_cpu'])['mem_cpu']
    max_cpu_mem = max(backup_flavor, key=lambda x: x['cpu_mem'])['cpu_mem']
    min_cpu_mem = min(backup_flavor, key=lambda x: x['cpu_mem'])['cpu_mem']
    max_mem_cpu = max(backup_flavor, key=lambda x: x['mem_cpu'])['mem_cpu']
    min_mem_cpu = min(backup_flavor, key=lambda x: x['mem_cpu'])['mem_cpu']
    max_mem = max(flavor_information, key=lambda x: x['mem'])['mem']
    min_mem = min(flavor_information, key=lambda x: x['mem'])['mem']
    max_cpu = max(flavor_information, key=lambda x: x['cpu'])['cpu']
    min_cpu = min(flavor_information, key=lambda x: x['cpu'])['cpu']

    resource_dict = {"CPU": CPU_dict, "MEM": MEM_dict}[resource]
    resource_dict_opposite = {"CPU": MEM_dict, "MEM": CPU_dict}[resource]
    resource_index = {"CPU": 0, "MEM": 1}[resource]
    resource_index_opposite = {"CPU": 1, "MEM": 0}[resource]
    if resource == "CPU":
        add_flavor = []
        for fi in flavor_information:
            if fi['cpu_mem'] == max_cpu_mem_all:
                add_flavor.append(fi)
        add_flavor.sort(key=lambda x: x['cpu'], reverse=True)

        while SA_T > SA_T_min:
            flavor_queue_new = flavor_queue[:]
            random.shuffle(dice)
            flavor1 = flavor_queue_new[dice[0]]
            flavor2 = flavor_queue_new[dice[1]]
            flavor_queue_new[dice[0]] = flavor2
            flavor_queue_new[dice[1]] = flavor1

            physical_server = {}
            physical_server_cluster = [physical_server]
            residual_CPU = physical_server_CPU
            residual_MEM = physical_server_MEM
            physical_server_cluster_resource_left = [[physical_server_CPU, physical_server_MEM]]  # 集群中各服务器资源剩余情况

            for fq in flavor_queue_new:
                flag = False
                for index, resource_left in enumerate(physical_server_cluster_resource_left):
                    if CPU_dict[fq] <= resource_left[0] and MEM_dict[fq] <= resource_left[1]:
                        cpu_resource_left = resource_left[0] - CPU_dict[fq]
                        mem_resource_left = resource_left[1] - MEM_dict[fq]
                        if mem_resource_left == 0 and cpu_resource_left != 0:
                            break
                        if mem_resource_left != 0 and cpu_resource_left / float(mem_resource_left) > max_cpu_mem_all:
                            break

                        physical_server_cluster_resource_left[index][0] = physical_server_cluster_resource_left[index][
                                                                              0] - CPU_dict[fq]
                        physical_server_cluster_resource_left[index][1] = physical_server_cluster_resource_left[index][
                                                                              1] - MEM_dict[fq]
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

            physical_server_numbers = len(physical_server_cluster_resource_left) - 1
            target_resource = {"CPU": physical_server_CPU, "MEM": physical_server_MEM}[resource]
            target_resource_index = {"CPU": 0, "MEM": 1}[resource]
            last_rate = physical_server_cluster_resource_left[physical_server_numbers][0] / float(
                physical_server_CPU)

            # mark = 1
            # for resource_left in physical_server_cluster_resource_left:
            #     mark = mark*(1-resource_left[target_resource_index]/float(target_resource))
            mark = physical_server_numbers + last_rate
            mark_temp = mark
            if mark_temp < mark_temp_min:
                mark_temp_min = mark_temp
                physical_server_cluster_final = physical_server_cluster
                physical_server_cluster_resource_left_final = physical_server_cluster_resource_left
            # if mark - 33.14285 <0.0000001:
            #     print physical_server_cluster_resource_left
            #     print len(physical_server_cluster_resource_left)
            #     print len(physical_server_cluster_final)
            #     break
            if mark < mark_min:
                mark_min = mark
                flavor_queue = flavor_queue_new
            else:
                # p = 1 / (1 + math.exp(-(mark - mark_min) / SA_T))
                p = math.exp((mark_min - mark) / SA_T)
                if random.random() > p:
                    mark_min = mark
                    flavor_queue = flavor_queue_new
            print mark_min
            print round(SA_T, 1)
            SA_T = SA_T * r
        # print physical_server_cluster_resource_left
        print physical_server_cluster_resource_left_final
        special_add_counts = []
        for af in add_flavor:
            apecial_flavor = af["name"]
            special_cpu = af["cpu"]
            special_mem = af["mem"]
            for index, resource_left in enumerate(physical_server_cluster_resource_left_final):
                for i in range(1, 100):
                    if i * special_cpu > resource_left[0] and (i - 1) * special_mem < resource_left[1]:
                        physical_server_cluster_resource_left_final[index][0] = \
                            physical_server_cluster_resource_left_final[index][0] - (i - 1) * special_cpu
                        physical_server_cluster_resource_left_final[index][1] = \
                            physical_server_cluster_resource_left_final[index][1] - (i - 1) * special_mem
                        special_add_counts.append([index, i - 1, apecial_flavor])
                        break
        print mark_temp_min
        print add_flavor
        print physical_server_cluster_resource_left_final
        print special_add_counts
        print physical_server_cluster_final
        count = 0
        flavor_prediction_numbers_add = {}
        for sad in special_add_counts:
            if sad[1] != 0:
                count = count + sad[1]
                if sad[2] in flavor_prediction_numbers_add:
                    flavor_prediction_numbers_add[sad[2]] = flavor_prediction_numbers_add[sad[2]] + sad[1]
                else:
                    flavor_prediction_numbers_add[sad[2]] = sad[1]
                if sad[2] in physical_server_cluster_final[sad[0]]:
                    physical_server_cluster_final[sad[0]][sad[2]] = physical_server_cluster_final[sad[0]][sad[2]] + sad[
                        1]
                else:
                    physical_server_cluster_final[sad[0]][sad[2]] = sad[1]
        print count
        print flavor_prediction_numbers_add
        flavor_prediction_numbers_new = flavor_prediction_numbers[:]
        for key in flavor_prediction_numbers_add:
            index = flavor_name.index(key)
            flavor_prediction_numbers_new[index] = flavor_prediction_numbers_new[index] + flavor_prediction_numbers_add[
                key]

        # for pscl in physical_server_cluster_final:
        print flavor_prediction_numbers
        print flavor_prediction_numbers_new
        print physical_server_cluster_final

        result = []
        for pscf in physical_server_cluster_final:
            physical_server = pscf.items()
            cpu = 0
            mem = 0
            for ps in physical_server:
                cpu = cpu + CPU_dict[ps[0]] * ps[1]
                mem = mem + MEM_dict[ps[0]] * ps[1]
            result.append([56 - cpu, 128 - mem])
        print result

        return [physical_server_cluster_final, flavor_prediction_numbers_new]
    else:
        add_flavor = []
        for fi in flavor_information:
            if fi['mem_cpu'] == max_mem_cpu_all:
                add_flavor.append(fi)
        add_flavor.sort(key=lambda x: x['mem'], reverse=True)

        while SA_T > SA_T_min:
            flavor_queue_new = flavor_queue[:]
            random.shuffle(dice)
            flavor1 = flavor_queue_new[dice[0]]
            flavor2 = flavor_queue_new[dice[1]]
            flavor_queue_new[dice[0]] = flavor2
            flavor_queue_new[dice[1]] = flavor1

            physical_server = {}
            physical_server_cluster = [physical_server]
            residual_CPU = physical_server_CPU
            residual_MEM = physical_server_MEM
            physical_server_cluster_resource_left = [[physical_server_CPU, physical_server_MEM]]  # 集群中各服务器资源剩余情况

            for fq in flavor_queue_new:
                flag = False
                for index, resource_left in enumerate(physical_server_cluster_resource_left):
                    if CPU_dict[fq] <= resource_left[0] and MEM_dict[fq] <= resource_left[1]:
                        mem_resource_left = resource_left[1] - MEM_dict[fq]
                        cpu_resource_left = resource_left[0] - CPU_dict[fq]
                        # if cpu_resource_left == 0 and mem_resource_left != 0:
                        #     break
                        # if cpu_resource_left != 0 and mem_resource_left / float(cpu_resource_left) > max_mem_cpu_all:
                        #     break

                        physical_server_cluster_resource_left[index][0] = physical_server_cluster_resource_left[index][
                                                                              0] - CPU_dict[fq]
                        physical_server_cluster_resource_left[index][1] = physical_server_cluster_resource_left[index][
                                                                              1] - MEM_dict[fq]
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

            physical_server_numbers = len(physical_server_cluster_resource_left) - 1
            target_resource = {"CPU": physical_server_CPU, "MEM": physical_server_MEM}[resource]
            target_resource_index = {"CPU": 0, "MEM": 1}[resource]
            last_rate = physical_server_cluster_resource_left[physical_server_numbers][1] / float(physical_server_MEM)

            # mark = 1
            # for resource_left in physical_server_cluster_resource_left:
            #     mark = mark*(1-resource_left[target_resource_index]/float(target_resource))
            mark = physical_server_numbers + last_rate
            mark_temp = mark
            if mark_temp < mark_temp_min:
                mark_temp_min = mark_temp
                physical_server_cluster_final = physical_server_cluster
                physical_server_cluster_resource_left_final = physical_server_cluster_resource_left
            if mark < mark_min:
                mark_min = mark
                flavor_queue = flavor_queue_new
            else:
                # p = 1 / (1 + math.exp(-(mark - mark_min) / SA_T))
                p = math.exp((mark_min - mark) / SA_T)
                if random.random() > p:
                    mark_min = mark
                    flavor_queue = flavor_queue_new
            print mark_min
            print round(SA_T, 1)
            SA_T = SA_T * r
        return [physical_server_cluster_final, flavor_prediction_numbers]
        # print physical_server_cluster_resource_left
        # print physical_server_cluster_resource_left_final
        # special_add_counts = []
        # for af in add_flavor:
        #     apecial_flavor = af["name"]
        #     special_cpu = af["cpu"]
        #     special_mem = af["mem"]
        #     for index, resource_left in enumerate(physical_server_cluster_resource_left_final):
        #         for i in range(1, 100):
        #             # if i * special_mem > resource_left[1] and (i - 1) * special_cpu < resource_left[0]:
        #             if i * special_mem > resource_left[1]:
        #                 physical_server_cluster_resource_left_final[index][1] = \
        #                     physical_server_cluster_resource_left_final[index][1] - (i - 1) * special_mem
        #                 physical_server_cluster_resource_left_final[index][0] = \
        #                     physical_server_cluster_resource_left_final[index][0] - (i - 1) * special_cpu
        #                 special_add_counts.append([index, i - 1, apecial_flavor])
        #                 break


