# coding=utf-8
def generate_output(flavor_name, flavor_prediction_numbers, physical_server_cluster):
    flavor_total = 0  # flavor总数
    for fn in flavor_prediction_numbers:
        flavor_total += fn
    output_str = [str(flavor_total)]

    for fn in flavor_name:
        numbers_str = str(flavor_prediction_numbers[flavor_name.index(fn)])
        item = fn + ' ' + numbers_str
        output_str.append(item)

    output_str.append('')
    output_str.append(str(len(physical_server_cluster)))

    for psc in physical_server_cluster:
        psc_str = str(physical_server_cluster.index(psc) + 1)
        physical_server = psc.items()
        for ps in physical_server:
            psc_str += ' ' + ps[0] + ' ' + str(ps[1])
        output_str.append(psc_str)

    return output_str

    # f_output = open('output.txt', 'w')
    # f_output.writelines(output_str)
    # f_output.close()
