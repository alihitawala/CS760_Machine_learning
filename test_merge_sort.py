__author__ = 'aliHitawala'
from Solution_merge import main
import sys

def test_empty():
    output = main([])
    compare(output, [])

def test_single_element():
    output = main([2])
    compare(output, [2])


def test_negative_values():
    output = main([-9, -4, -3, -2, -5])
    compare(output, [-9, -5, -4, -3, -2])


def test_duplicate_element():
    output = main([2, 2])
    compare(output, [2, 2])

def test_integer_overflow():
    output = main([sys.maxint, -sys.maxint])
    compare(output, [-sys.maxint, sys.maxint])

def test_large_input():
    a = []
    for i in open("test_large_input"):
        a.append(int(i))
    expected_output = []
    for i in open("test_large_output"):
        expected_output.append(int(i))

    output = main(a)
    compare(output, expected_output)


def compare(output_list, expected_array):
    a = []
    while output_list is not None:
        a.append(output_list.data)
        output_list = output_list.next
    if len(a) != len(expected_array):
        print "fail"
        return
    for i in range(len(expected_array)):
        if a[i] != expected_array[i]:
            print "fail"
            return
    print "pass"


test_duplicate_element()
test_empty()
test_negative_values()
test_single_element()
test_large_input()
test_integer_overflow()
