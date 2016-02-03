__author__ = 'aliHitawala'


import sys
import math


def main():
    filename_train = sys.argv[1]
    filename_test = sys.argv[2]
    dataset = get_dataset_structure(filename_train)
    calculate_p_x_y(dataset)
    calculate_p_x_x_y(dataset)
    test_data_naive_bayes(dataset, filename_test)


def test_data_naive_bayes(dataset_train, filename):
    dataset_test = get_dataset_structure(filename)
    calculate_p_y_x(dataset_train, dataset_test)
    print_naive(dataset_test)


def print_naive(dataset):
    for attribute in dataset.attribute_list:
        if attribute.name == 'class':
            continue
        sys.stdout.write(attribute.name + ' class\n')
    sys.stdout.write('\n')
    count = 0
    for row in dataset.rows:
        sys.stdout.write(row['prediction'][1] + ' ' + row['class'] + ' ' + str(row['prediction'][0]) + '\n')
        if row['prediction'][1] == row['class']:
            count += 1
    sys.stdout.write('\n')
    sys.stdout.write(str(count))


def get_dataset_structure(filename):
    file_train = open(filename, 'r')
    attribute_detail_map = dict()
    attributes_list = []
    is_data = False
    rows = []
    for line in file_train:
        word_list = line.split()
        first_word = word_list[0]
        if first_word == '%':
            continue
        if is_data:
            values = [value.strip() for value in line.split(",")]
            attribute_value_map = dict()
            i = 0
            for value in values:
                attribute = attributes_list[i].name
                attribute_value_map[attribute] = value
                i += 1
            rows.append(attribute_value_map)
        elif first_word == '@attribute':
            attribute_name = word_list[1].replace("'", "")
            values_embedded = line[line.find("{")+1:line.find("}")]
            values = [Value(value.strip()) for value in values_embedded.split(",")]
            attrib = Attribute(attribute_name, values)
            attribute_detail_map[attribute_name] = attrib
            attributes_list.append(attrib)
        elif first_word == '@data':
            is_data = True
    dataset = Dataset(attributes_list, attribute_detail_map, rows)
    return dataset


def calculate_p_y_x(dataset_train, dataset_test):
    attribute_class = dataset_train.attributes['class']
    param_yes = attribute_class.values[0].value
    param_no = attribute_class.values[1].value
    p_y_yes = attribute_class.values[0].get_p_x()
    p_y_no = attribute_class.values[1].get_p_x()
    for row in dataset_test.rows:
        p_x_y_yes = p_y_yes
        p_x_y_no = p_y_no
        for key in row:
            if key == 'class':
                continue
            attribute_info = dataset_train.attributes[key]
            values_train = attribute_info.values
            value_in_test_row = row[key]
            for value in values_train:
                if value.value == value_in_test_row:
                    p_x_y_yes *= value.get_p_x_y_yes()
                    p_x_y_no *= value.get_p_x_y_no()
                    break
        if p_x_y_yes > p_x_y_no:
            row['prediction'] = [p_x_y_yes/(p_x_y_yes + p_x_y_no), param_yes]
        else:
            row['prediction'] = [p_x_y_no/(p_x_y_yes + p_x_y_no), param_no]


def calculate_p_x_x_y(dataset):
    attribute_class = dataset.attributes['class']
    param_yes = attribute_class.values[0].value
    param_no = attribute_class.values[1].value
    p_y_yes = attribute_class.values[0].get_p_x()
    p_y_no = attribute_class.values[1].get_p_x()
    count_param_yes = get_count(dataset, 'class', param_yes, param_yes) * 1.0
    count_param_no = get_count(dataset, 'class', param_no, param_no) * 1.0
    count_total = count_param_yes + count_param_no
    for i in range(len(dataset.attribute_list)):
        attribute_x_1 = dataset.attribute_list[i]
        for j in range(i+1,len(dataset.attribute_list)):
            attribute_x_2 = dataset.attribute_list[j]
            if attribute_x_1.name == 'class' or attribute_x_2.name == 'class':
                continue
            attribute_x_1.i_x_x_y[attribute_x_2.name] = 0.0
            attribute_x_2.i_x_x_y[attribute_x_1.name] = 0.0
            for value_1 in attribute_x_1.values:
                for value_2 in attribute_x_2.values:
                    count_x_x_y_yes = get_count_x_x_y(dataset, attribute_x_1.name, value_1.value, attribute_x_2.name,
                                                  value_2.value, 'class', param_yes) * 1.0
                    count_x_x_y_no = get_count_x_x_y(dataset, attribute_x_1.name, value_1.value, attribute_x_2.name,
                                                  value_2.value, 'class', param_no) * 1.0
                    la_place_den = len(attribute_x_1.values) * len(attribute_x_2.values) * 2.0
                    la_place_den_X_X = len(attribute_x_1.values) * len(attribute_x_2.values) * 1.0
                    p_x_x_y_yes = (1 + count_x_x_y_yes)/(count_total + la_place_den)
                    p_x_x_y_no = (1 + count_x_x_y_no)/(count_total + la_place_den)
                    p_x_x_cond_y_yes = (1 + count_x_x_y_yes)/(la_place_den_X_X + count_param_yes)
                    p_x_x_cond_y_no = (1 + count_x_x_y_no)/(la_place_den_X_X + count_param_no)
                    p_x1_y_yes = value_1.get_p_x_y_yes()
                    p_x1_y_no = value_1.get_p_x_y_no()
                    p_x2_y_yes = value_2.get_p_x_y_yes()
                    p_x2_y_no = value_2.get_p_x_y_no()
                    attribute_x_1.i_x_x_y[attribute_x_2.name] += p_x_x_y_yes * math.log(p_x_x_cond_y_yes/(p_x1_y_yes * p_x2_y_yes ), 2)
                    attribute_x_1.i_x_x_y[attribute_x_2.name] += p_x_x_y_no * math.log(p_x_x_cond_y_no/(p_x1_y_no * p_x2_y_no), 2)
            attribute_x_2.i_x_x_y[attribute_x_1.name] = attribute_x_1.i_x_x_y[attribute_x_2.name]


def get_count_x_x_y(dataset, attribute_name_1, value_1, attribute_name_2, value_2, class_attribute, param) :
    count = 0
    for row in dataset.rows:
        if row[attribute_name_1] == value_1 and row[attribute_name_2] == value_2 and row['class'] == param:
            count += 1
    return count


def calculate_p_x_y(dataset):
    attribute_class = dataset.attributes['class']
    param_yes = attribute_class.values[0].value
    param_no = attribute_class.values[1].value
    count_param_yes = get_count(dataset, 'class', param_yes, param_yes) * 1.0
    count_param_no = get_count(dataset, 'class', param_no, param_no) * 1.0
    for key in dataset.attributes:
        if key == 'class':
            param_y = attribute_class.values[0]
            param_y.set_p_x((count_param_yes+1)/(count_param_yes+count_param_no+2))
            param_n = attribute_class.values[1]
            param_n.set_p_x((count_param_no+1)/(count_param_yes+count_param_no+2))
            continue
        attribute_info = dataset.attributes[key]
        num_values = len(attribute_info.values)
        for value in attribute_info.values:
            count_attribute_in_yes = get_count(dataset, attribute_info.name, value.value, param_yes) * 1.0
            count_attribute_in_no = get_count(dataset, attribute_info.name, value.value, param_no) * 1.0
            la_place_num = 1
            la_place_den = num_values
            p_x_y_yes = (count_attribute_in_yes + la_place_num) / (count_param_yes + la_place_den)
            p_x_y_no = (count_attribute_in_no + la_place_num) / (count_param_no + la_place_den)
            value.set_p_x_y_yes(p_x_y_yes)
            value.set_p_x_y_no(p_x_y_no)


def get_count(dataset, name, value, param):
    count = 0
    for row in dataset.rows:
        if row[name] == value and row['class'] == param:
            count += 1
    return count


class Tuple:
    def __init__(self, value, token):
        self.value = value
        self.token = token


class Dataset:
    def __init__(self, attribute_list, attributes, rows):
        self.attribute_list = attribute_list
        self.attributes = attributes
        self.rows = rows


class Attribute:
    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.p_x_y_yes = 0
        self.p_x_y_no = 0
        self.i_x_x_y = dict()


class Value:
    def __init__(self, value):
        self.value = value
        self.p_x_y_yes = 0
        self.p_x_y_no = 0
        self.p_x = 0

    def set_p_x(self, p_x):
        self.p_x = p_x

    def get_p_x(self):
        return self.p_x

    def set_p_x_y_yes(self, p_x_y):
        self.p_x_y_yes = p_x_y

    def get_p_x_y_yes(self):
        return self.p_x_y_yes

    def set_p_x_y_no(self, p_x_y):
        self.p_x_y_no = p_x_y

    def get_p_x_y_no(self):
        return self.p_x_y_no

main()