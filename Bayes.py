__author__ = 'aliHitawala'


import sys
import math


def main():
    filename_train = sys.argv[1]
    filename_test = sys.argv[2]
    m = sys.argv[3]
    file_train = open(filename_train, 'r')
    attribute_detail_map = dict()
    attributes_list = []
    isData = False
    rows = []
    for line in file_train:
        wordList = line.split()
        first_word = wordList[0]
        if first_word == '%':
            continue
        if isData:
            values = [value.strip() for value in line.split(",")]
            attribute_value_map = dict()
            i = 0
            for value in values:
                attribute = attributes_list[i].name
                attribute_value_map[attribute] = value
                i += 1
            rows.append(attribute_value_map)
        elif first_word == '@attribute':
            attribute_name = wordList[1].replace("'", "")
            values_embedded = line[line.find("{")+1:line.find("}")]
            values = [Value(value.strip()) for value in values_embedded.split(",")]
            attrib = Attribute(attribute_name, values)
            attribute_detail_map[attribute_name] = attrib
            attributes_list.append(attrib)
        elif first_word == '@data':
            isData = True
    dataset = Dataset(attribute_detail_map, rows)
    calculate_p_x_y(dataset, attribute_detail_map['class'])


def calculate_p_x_y(dataset, attribute_class):
    param_yes = attribute_class.values[0].value
    param_no = attribute_class.values[1].value
    for key in dataset.attributes:
        attribute_info = dataset.attributes[key]
        for value in attribute_info.values:
            count_yes = get_count(dataset, attribute_info.name, value, param_yes) * 1.0
            count_no = get_count(dataset, attribute_info.name, value, param_no) * 1.0
            value.set_p_x_y_yes(count_yes/(count_no+count_yes))
            value.set_p_x_y_no(count_no/(count_no+count_yes))



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
    def __init__(self, attributes, rows):
        self.attributes = attributes
        self.rows = rows


class Attribute:
    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.p_x_y_yes = 0
        self.p_x_y_no = 0


class Value:
    def __init__(self, value):
        self.value = value
        self.p_x_y_yes = 0
        self.p_x_y_no = 0

    def set_p_x_y_yes(self, p_x_y):
        self.p_x_y_yes = p_x_y

    def get_p_x_y_yes(self):
        return self.p_x_y_yes

    def set_p_x_y_no(self, p_x_y):
        self.p_x_y_no = p_x_y

    def get_p_x_y_no(self):
        return self.p_x_y_no