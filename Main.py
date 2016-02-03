__author__ = 'aliHitawala'

import sys
import math

def main():
    filename_train = sys.argv[1]
    filename_test = sys.argv[2]
    m = sys.argv[3]
    file_train = open(filename_train, 'r')
    attributes = dict()
    attributes_list = []
    isData = False
    rows = []
    for line in file_train:
        wordList = line.split()
        first_word = wordList[0]
        if isData:
            values = [value.strip() for value in line.split(",")]
            attributeValues = dict()
            i = 0
            for value in values:
                attribute = attributes_list[i].name
                attributeValues[attribute] = value
                i += 1
            row = Row(attributeValues)
            rows.append(row)

        elif first_word == '@attribute':
            attribute_name = wordList[1].replace("'", "")
            isNumber = wordList[2].replace("'", "") == 'real'
            values = []
            if not isNumber:
                valuesEmbedded = line[line.find("{")+1:line.find("}")]
                values =[value.strip() for value in valuesEmbedded.split(",")]
            attrib = Attribute(attribute_name, isNumber, values)
            attributes[attribute_name] = attrib
            attributes_list.append(attrib)
        elif first_word == '@data':
            isData = True
    dataset = Dataset(attributes, rows)
    root = construct_dt(dataset, attributes_list)
    print root
    print_tree(root, dataset, 0)


def construct_dt(dataset, attr_list):
    length = len(dataset.rows)
    info_gain = 0
    selected_attribute = ""
    if length < 11:
        return get_leaf_node(dataset)
    entropy_dataset = get_entropy_dataset(dataset)
    num=0
    for attribute in attr_list:
        name = attribute.name
        if name == 'class':
            continue
        gain = information_gain(name, dataset, entropy_dataset)
        if gain[0] > info_gain:
            info_gain = gain[0]
            selected_attribute = name
            num = gain[1]
    if info_gain == 0:
        return get_leaf_node(dataset)
    isNumber = dataset.attributes[selected_attribute].isNumber
    attribute_info = dataset.attributes[selected_attribute]
    new_attr_list = []
    for a in attr_list:
        if a.name != selected_attribute:
            new_attr_list.append(a)
    count_positive = get_count_attribute_value(dataset, "class", "positive", "positive")
    count_negative = get_count_attribute_value(dataset, "class", "negative", "negative")
    if isNumber:
        dataset_less = get_new_dataset(dataset, selected_attribute, num, "lt")
        dataset_greater = get_new_dataset(dataset, selected_attribute, num, "gt")
        children = []
        children.append(construct_dt(dataset_less, attr_list))
        children.append(construct_dt(dataset_greater, attr_list))
        root = Tree(selected_attribute, children, num, count_positive, count_negative)
    else:
        values = attribute_info.values
        i = 0
        children = []
        for value in values:
            new_dataset = get_new_dataset(dataset, selected_attribute, value, "eq")
            children.append(construct_dt(new_dataset, new_attr_list))
            i += 1
        root = Tree(selected_attribute, children, 0, count_positive, count_negative)
    return root


def get_leaf_node (dataset) :
    count_positive = get_count_attribute_value(dataset, "class", "positive", "positive")
    count_negative = get_count_attribute_value(dataset, "class", "negative", "negative")
    return Tree(None, [], 0, count_positive, count_negative)


def get_new_dataset(dataset, attribute, value, cmp):
    rows = []
    for row in dataset.rows:
        if (cmp == "lt" and float(row.attributeValue[attribute]) <= value) or \
                (cmp == "gt" and float(row.attributeValue[attribute]) > value) or \
                (cmp == "eq" and row.attributeValue[attribute] == value):
            rows.append(row)
    return Dataset(dataset.attributes.copy(), rows)


def information_gain(attribute_name, dataset, entropy_dataset):
    isNumber = dataset.attributes[attribute_name].isNumber
    num = 0
    if isNumber:
        ret_value = get_best_number_split(attribute_name, dataset)
        entropy = ret_value[0]
        num = ret_value[1]
    else:
        entropy = get_entropy_descrete(attribute_name, dataset)
    return [entropy_dataset-entropy, num]


def get_entropy_dataset(dataset):
    count_positive = get_count_attribute_value(dataset, "class", "positive", "positive") * 1.0
    count_negative = get_count_attribute_value(dataset, "class", "negative", "negative") * 1.0
    total_attrib = count_negative + count_positive
    entropy = -1.0 * (((count_positive/total_attrib) * log(count_positive, total_attrib)) +
       ((count_negative/total_attrib) * log(count_negative, total_attrib)))
    return entropy


def get_entropy_descrete(attribute_name, dataset):
    isNumber = dataset.attributes[attribute_name].isNumber
    entropy = 0.0
    total_rows = len(dataset.rows)
    if not isNumber:
        values = dataset.attributes[attribute_name].values
        for value in values:
            count_positive = get_count_attribute_value(dataset, attribute_name, value, "positive") * 1.0
            count_negative = get_count_attribute_value(dataset, attribute_name, value, "negative") * 1.0
            total_attrib = count_negative + count_positive
            if total_attrib != 0:
                try :
                    entropy += -1.0 * (total_attrib/total_rows) * (((count_positive/total_attrib) * log(count_positive, total_attrib)) +
                       ((count_negative/total_attrib) * log(count_negative,total_attrib)))
                except Exception:
                    print "Error: either positive or negative count is zero for attribute " + attribute_name
    return entropy


def get_best_number_split(attribute_name, dataset) :
    tuples = get_datastructure_attribute(attribute_name, dataset)
    tuples.sort(key=lambda x: (x.value, x.token))
    size = len(tuples)
    min_entropy = 1.0
    split_num = 0
    for i in range(1, size):
        prev = tuples[i-1]
        curr = tuples[i]
        entropy = 0.0
        isConflict = False
        if prev.value != curr.value:
            if both_token_present(tuples, prev.value) or both_token_present(tuples, curr.value):
                isConflict = True
        if prev.token != curr.token or isConflict:
            num = (prev.value + curr.value) / 2.0
            # less
            count_positive = get_count_attribute_value_real(dataset, attribute_name, num, "positive", "lt") * 1.0
            count_negative = get_count_attribute_value_real(dataset, attribute_name, num, "negative", "lt") * 1.0
            total_num_less = count_negative+count_positive
            entropy += -1.0 * (total_num_less/size) * (((count_positive/total_num_less) * log(count_positive, total_num_less)) +
                       ((count_negative/total_num_less) * log(count_negative, total_num_less)))
            count_positive = get_count_attribute_value_real(dataset, attribute_name, num, "positive", "gt") * 1.0
            count_negative = get_count_attribute_value_real(dataset, attribute_name, num, "negative", "gt") * 1.0
            total_num_more = count_negative+count_positive
            if total_num_more != 0:
                entropy += -1.0 * (total_num_more/size) * (((count_positive/total_num_more) * log(count_positive, total_num_more)) +
                   ((count_negative/total_num_more) * log(count_negative, total_num_more)))
            if entropy < min_entropy:
                split_num = num
                min_entropy = entropy
    return [min_entropy, split_num]


def both_token_present(tuples, value):
    is_positive = False
    is_negative = False
    for t in tuples:
        if t.value == value:
            if t.token == "positive":
                is_positive = True
            if t.token == "negative":
                is_negative = True
    return is_positive and is_negative

def get_datastructure_attribute(attribute_name, dataset):
    tuples = []
    for row in dataset.rows:
        t = Tuple(float(row.attributeValue[attribute_name]), row.attributeValue['class'])
        tuples.append(t)
    return tuples


def log(num, den):
    if num == 0:
        return 0
    return math.log(num*1.0/den, 2)


def get_count_attribute_value_real(dataset, attribute_name, value, token, cmp="eq"):
    rows = dataset.rows
    count = 0
    for row in rows:
        if (cmp == 'lt' and float(row.attributeValue[attribute_name]) <= value and row.attributeValue['class'] == token)\
                or (cmp == 'gt'and float(row.attributeValue[attribute_name]) > value and row.attributeValue['class'] == token):
            count += 1
    return count


def get_count_attribute_value(dataset, attribute_name, value, token):
    rows = dataset.rows
    count = 0
    for row in rows:
        if row.attributeValue[attribute_name] == value and row.attributeValue['class'] == token:
            count += 1
    return count


def print_tree(root, dataset, num_tab):
    if root is None or root.attribute_name is None:
        return
    name = root.attribute_name
    values = dataset.attributes[name].values
    i=0
    isNumber = dataset.attributes[name].isNumber
    if isNumber:
        child = root.children[0]
        print_tab(num_tab)
        print_line(root.attribute_name, child, root.split_value, " <= ")
        print_tree(child, dataset, num_tab+1)
        child = root.children[1]
        print_tab(num_tab)
        print_line(root.attribute_name, child, root.split_value, " > ")
        print_tree(child, dataset, num_tab+1)
    else:
        for value in values:
            child = root.children[i]
            print_tab(num_tab)
            print_line(root.attribute_name, child, value, " = ")
            print_tree(child, dataset, num_tab+1)
            i += 1


def print_line(attribute_name, child, value, dim):
    sys.stdout.write(attribute_name + dim + str(value) + " [" + str(child.num_negative) + " " + str(child.num_positive) + "] \n")


def print_tab(num):
    for i in range(num):
        sys.stdout.write('|\t')

class Tree:
    def __init__(self, attribute_name, children, split_value, num_positive=0, num_negative=0):
        self.attribute_name = attribute_name
        self.children = children
        self.split_value = split_value
        self.num_positive = num_positive
        self.num_negative = num_negative

class Tuple:
    def __init__(self, value, token):
        self.value = value
        self.token = token


class Dataset:
    def __init__(self, attributes, rows):
        self.attributes = attributes
        self.rows = rows


class Attribute:
    def __init__(self, name, isNumber, value):
        self.name = name
        self.isNumber = isNumber
        self.values = value


class Row:
    def __init__(self, attributeValue):
        self.attributeValue = attributeValue

if __name__ == '__main__':
    main()