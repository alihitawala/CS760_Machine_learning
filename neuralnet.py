__author__ = 'aliHitawala'

import sys
import math
import random, time
import matplotlib.pyplot as plt
import numpy as np

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

ROW_INDEX_ATTRIBUTE = '__i__'

def sigmoid_func(result):
    return 1.0 /(1+math.exp(-result))


def calculate_output(dataset, row, attribute_weights, bias_weight):
    result = 0
    for attribute in dataset.attribute_list:
        if attribute.name.lower() != 'class' and attribute.name.lower() != ROW_INDEX_ATTRIBUTE:
            result += float(row[attribute.name]) * attribute_weights[attribute.name]
    result += bias_weight
    return sigmoid_func(result)


def initialize_attribute_weights(dataset):
    result = dict()
    for attribute in dataset.attribute_list:
        if attribute.name.lower() != 'class' and attribute.name.lower() != ROW_INDEX_ATTRIBUTE:
            result[attribute.name] = 0.1
    return result


def get_actual_class_value_int(dataset, row):
    class_attribute = dataset.attribute_list[len(dataset.attribute_list) - 1]
    row_label_y = row[class_attribute.name]
    i = 0
    for value in class_attribute.values:
        if value == row_label_y:
            return i
        i += 1
    raise RuntimeError('this should not be reached!')


def update_attribute_weights(attribute_weights, row, o, y, n, bias_weight):
    delta_w = (y-o)*o*(1-o)
    for attribute_name in attribute_weights:
        w = attribute_weights[attribute_name]
        x = float(row[attribute_name])
        new_w = n*delta_w*x + w
        attribute_weights[attribute_name] = new_w
    return bias_weight + 1*n*delta_w


def merge(bucket_rows, exc):
    result = []
    for i in range(len(bucket_rows)):
        if i != exc:
            for row in bucket_rows[i]:
                result.append(row)
    return result


def calculate_nn(dataset, rows, learning_rate, attribute_weights, bias_weight) :
    for row in rows:
        row_output_value = get_actual_class_value_int(dataset, row)
        output = calculate_output(dataset, row, attribute_weights, bias_weight)
        bias_weight = update_attribute_weights(attribute_weights, row, output,
                                                   row_output_value, learning_rate, bias_weight)
    return bias_weight


def get_row_predictions(dataset, test_row, attribute_weights, bias_weight, fold_num):
    actual_class_value = get_actual_class_value_int(dataset, test_row)
    sigmoid_output = calculate_output(dataset, test_row, attribute_weights, bias_weight)
    predicted_class_value = 0 if sigmoid_output < 0.5 else 1
    class_values = dataset.attribute_list[len(dataset.attribute_list) - 1].values
    return Row(class_values[actual_class_value], class_values[predicted_class_value], sigmoid_output, fold_num, test_row[ROW_INDEX_ATTRIBUTE])


def print_prediction(test_row_predictions):
    test_row_predictions.sort(key=lambda x: x.index)
    # for row in test_row_predictions:
    #     print row.fold_num+1, row.actual_class, row.predicted_class, row.sigmoid_value, row.index
    return test_row_predictions


def neuralnet(dataset, num_folds, learning_rate, num_epoch):
    class_attribute = dataset.attribute_list[len(dataset.attribute_list) - 1]
    bucket_rows = StratifiedSampler(dataset.rows, class_attribute.name, class_attribute.values, num_folds).get_buckets()
    test_row_predictions = []
    for fold_num in range(num_folds):
        attribute_weights = initialize_attribute_weights(dataset)
        bias_weight = 0.1
        test_rows = bucket_rows[fold_num]
        train_rows = merge(bucket_rows, fold_num)
        random.shuffle(train_rows)
        for epoch in range(num_epoch):
            bias_weight = calculate_nn(dataset, train_rows, learning_rate, attribute_weights, bias_weight)
        for test_row in test_rows:
            test_row_predictions.append(get_row_predictions(dataset, test_row, attribute_weights, bias_weight, fold_num))
    return print_prediction(test_row_predictions)


def get_dataset_structure(filename):
    file_train = open(filename, 'r')
    attribute_detail_map = dict()
    attributes_list = []
    is_data = False
    rows = []
    entry_num = 1
    for line in file_train:
        word_list = line.split()
        first_word = word_list[0]
        if first_word == '%':
            continue
        if is_data:
            values = [value.strip().replace("'", "").replace('"', '') for value in line.split(",")]
            attribute_value_map = dict()
            i = 0
            for value in values:
                attribute = attributes_list[i].name
                attribute_value_map[attribute] = value
                i += 1
            attribute_value_map[ROW_INDEX_ATTRIBUTE] = entry_num
            entry_num += 1
            rows.append(attribute_value_map)
        elif first_word == '@attribute':
            attribute_name = word_list[1].replace("'", "").replace('"', '')
            if line.find("{") != -1:
                values_embedded = line[line.find("{")+1:line.find("}")]
                values = [value.strip().replace("'", "").replace('"', '') for value in values_embedded.split(",")]
            else:
                values = [word_list[2]]
            attrib = Attribute(attribute_name, values)
            attribute_detail_map[attribute_name] = attrib
            attributes_list.append(attrib)
        elif first_word == '@data':
            is_data = True
    dataset = Dataset(attributes_list, attribute_detail_map, rows)
    return dataset



class Row:
    def __init__(self, actual_class, predicted_class, sigmoid_value, fold_num, index):
        self.actual_class = actual_class
        self.predicted_class = predicted_class
        self.sigmoid_value = sigmoid_value
        self.fold_num = fold_num
        self.index = index


class Dataset:
    def __init__(self, attribute_list, attributes, rows):
        self.attribute_list = attribute_list
        self.attributes = attributes
        self.rows = rows


class Attribute:
    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.weight = 0.1


class Value:
    def __init__(self, value):
        self.value = value


class StratifiedSampler:
    def __init__(self, rows, class_attribute, target_values, num_buckets):
        self.rows = rows
        self.class_attribute = class_attribute
        self.target_values = target_values
        self.num_buckets = num_buckets


    @staticmethod
    def get_rows_with_class_value(rows, c_attribtue, value):
        result = []
        for row in rows:
            if row[c_attribtue] == value:
                result.append(row)
        random.shuffle(result)
        return result

    def get_buckets(self):
        rows_with_class_value_1 = self.get_rows_with_class_value(self.rows, self.class_attribute, self.target_values[0])
        rows_with_class_value_2 = self.get_rows_with_class_value(self.rows, self.class_attribute, self.target_values[1])
        bucket_of_rows = []
        for i in range(self.num_buckets):
            bucket_of_rows.append([])
        i=0
        for row in rows_with_class_value_1:
            bucket_of_rows[i].append(row)
            i = (i + 1) % self.num_buckets
        # i=0
        for row in rows_with_class_value_2:
            bucket_of_rows[i].append(row)
            i = (i + 1) % self.num_buckets
        return bucket_of_rows

def main(filename = 'sonar.arff', num_folds=10, lr=0.1, epochs=25):
    filename_train = sys.argv[1] if filename is None else filename
    num_folds = int(sys.argv[2]) if num_folds is None else num_folds
    learning_rate = float(sys.argv[3]) if lr is None else lr
    num_epochs = int(sys.argv[4]) if epochs is None else epochs

    dataset = get_dataset_structure(filename_train)
    return neuralnet(dataset, num_folds, learning_rate, num_epochs)


def plot_graphs():
    plot_epoch = [25, 50, 75, 100]
    plot_folds = [5, 10, 15, 20, 25]
    results = []
    for epoch in plot_epoch:
        rows = main(epochs=epoch)
        num_correct = 0
        total_num = 0
        for row in rows:
            if row.actual_class == row.predicted_class:
                num_correct += 1
            total_num += 1
        accuracy = float(1.0 * num_correct/total_num)
        print 'Epoch :: ' + str(epoch) + ' Accuracy :: ' + str(accuracy)
        results.append(epoch)
    plt.plot(plot_epoch, results, linestyle='--', marker='o', color='b')
    plt.ylabel('Accuracy')
    plt.grid(True)
    plt.xticks(np.arange(0, max(plot_epoch)+10, 5.0))
    plt.xlim(0, plot_epoch[len(plot_epoch) - 1] + 10)
    plt.xlabel('Number of Epoch')
    plt.title('Accuracy v/s Epoch')
    plt.show()
    results = []
    for fold in plot_folds:
        rows = main(num_folds=fold)
        num_correct = 0
        total_num = 0
        for row in rows:
            if row.actual_class == row.predicted_class:
                num_correct += 1
            total_num += 1
        accuracy = float(1.0 * num_correct/total_num)
        print 'Fold :: ' + str(fold) + ' Accuracy :: ' + str(accuracy)
        results.append(fold)
    plt.plot(plot_folds, results, linestyle='--', marker='o', color='b')
    plt.ylabel('Accuracy')
    plt.grid(True)
    plt.xticks(np.arange(0, max(plot_epoch)+10, 5.0))
    plt.xlim(0, plot_epoch[len(plot_epoch) - 1] + 10)
    plt.xlabel('Number of Epoch')
    plt.title('Accuracy v/s Epoch')
    plt.show()

# main()
plot_graphs()