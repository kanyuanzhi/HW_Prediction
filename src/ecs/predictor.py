# from data_process import data_process
from placement import placement
from prediction import prediction


def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result

    flavor_prediction_numbers = prediction(ecs_lines, input_lines)

    return placement(input_lines, flavor_prediction_numbers)
