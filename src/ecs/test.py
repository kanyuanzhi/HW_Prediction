import os


class Test:
    def __init__(self):
        file_path = "test/case6.txt"
        self.array = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as lines:
                for line in lines:
                    self.array.append(line)
        else:
            print 'file not exist: ' + file_path

    def get_cpu(self):
        return int(self.array[0].split(' ')[0])

    def get_mem(self):
        return int(self.array[0].split(' ')[1])

    def get_resource(self):
        return self.array[2][:3]

    def get_flavor_name(self):
        flavor_name = []
        for item in self.array[6:]:
            flavor_name.append(item.split(':')[0])
        return flavor_name

    def get_numbers(self):
        numbers = []
        for item in self.array[6:]:
            numbers.append(int(item.split(':')[1]))
        return numbers
