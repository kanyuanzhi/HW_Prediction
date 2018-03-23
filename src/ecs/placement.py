# *coding=utf8
from readtxt import InputTxtProcess
from writetxt import generate_output

resource_name = InputTxtProcess().resource_name()
physical_server_specification = InputTxtProcess().physical_server_specification()
flavor_specification = InputTxtProcess().flavor_specification()

physical_server_CPU = int(physical_server_specification[0])  # 物理服务器CPU数量
physical_server_MEM = int(physical_server_specification[1]) * 1024  # 物理服务器内存大小

flavor_name = []
flavor_CPU = []
flavor_MEM = []

for fs in flavor_specification:
    flavor_name.append(fs[0])
    flavor_CPU.append(int(fs[1]))
    flavor_MEM.append(int(fs[2]))

CPU_dict = dict(zip(flavor_name, flavor_CPU))
MEM_dict = dict(zip(flavor_name, flavor_MEM))

flavor_prediction_numbers = [45, 12, 53, 50, 30]  # 预测数量

flavor_queue = []
flavor_total = 0  # flavor总数
for fn in flavor_prediction_numbers:
    flavor_total += fn
    current_flavor_name = flavor_name[flavor_prediction_numbers.index(fn)]
    flavor_queue += [current_flavor_name] * fn
print flavor_queue

physical_server_cluster = []
physical_server = {}
residual_CPU = physical_server_CPU
residual_MEM = physical_server_MEM
for fq in flavor_queue:
    if CPU_dict[fq] <= residual_CPU and MEM_dict[fq] <= residual_MEM:
        residual_CPU -= CPU_dict[fq]
        residual_MEM -= CPU_dict[fq]
        if fq in physical_server:
            physical_server[fq] += 1
        else:
            physical_server[fq] = 1
    else:
        physical_server_cluster.append(physical_server)
        physical_server = {}
        residual_CPU = physical_server_CPU
        residual_MEM = physical_server_MEM
physical_server_cluster.append(physical_server)

generate_output(flavor_name, flavor_prediction_numbers, physical_server_cluster)

print physical_server_cluster
test = physical_server_cluster[0]
print test.items()[0][0]
