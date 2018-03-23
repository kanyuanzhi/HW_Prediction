# *coding=utf8
def generate_output(flavor_name, flavor_prediction_numbers, physical_server_cluster):
    flavor_total = 0  # flavor总数
    for fn in flavor_prediction_numbers:
        flavor_total += fn
    output_str = [str(flavor_total) + '\n']

    for fn in flavor_name:
        numbers_str = str(flavor_prediction_numbers[flavor_name.index(fn)])
        item = fn + ' ' + numbers_str + '\n'
        output_str.append(item)

    output_str.append('\n')
    output_str.append(str(len(physical_server_cluster)) + '\n')

    for psc in physical_server_cluster:
        psc_str = str(physical_server_cluster.index(psc) + 1)
        physical_server = psc.items()
        for ps in physical_server:
            psc_str += ' ' + ps[0] + ' ' + str(ps[1])
        psc_str += '\n'
        output_str.append(psc_str)

    f_output = open('output.txt', 'w')
    f_output.writelines(output_str)
    f_output.close()
