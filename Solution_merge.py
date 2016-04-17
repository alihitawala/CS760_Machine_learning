__author__ = 'aliHitawala'


def main(a) :
    head = new_list(a)
    sorted_list = merge_sort(head)
    # print_list(sorted_list)
    return sorted_list


def print_list(linked_list):
    while linked_list is not None:
        print linked_list.data
        linked_list = linked_list.next


def new_list(a):
    if a is None or len(a) == 0:
        return None
    head = LinkedList(a[0])
    temp = head
    for i in range(1, len(a)):
        node = LinkedList(a[i])
        temp.next = node
        temp = node
    return head

# def sorted_merge(a,b):
#     if a is None: return b
#     if b is None: return a
#     result = None
#     if a.data <= b.data:
#         result = a
#         result.next = sorted_merge(a.next, b)
#     else:
#         result = b
#         result.next = sorted_merge(a, b.next)
#     return result

def sorted_merge_for(a,b):
    if a is None: return b
    if b is None: return a
    head = None
    if a.data <= b.data:
        result = a
        a = a.next
    else:
        result = b
        b = b.next
    head = result
    while a is not None and b is not None:
        if a.data <= b.data:
            result.next = a
            result = result.next
            a = a.next
        else:
            result.next = b
            result = result.next
            b = b.next
    while a is not None:
        result.next = a
        result = result.next
        a = a.next
    while b is not None:
        result.next = b
        result = result.next
        b = b.next
    return head


def merge_sort (linked_list):
    if linked_list is None or linked_list.next is None:
        return linked_list
    head1, head2 = front_back_split(linked_list)
    a = merge_sort(head1)
    b = merge_sort(head2)
    linked_list = sorted_merge_for(a, b)
    return linked_list


def front_back_split(linked_list) :
    if linked_list is None or linked_list.next is None:
        return linked_list, None
    slow = linked_list
    fast = linked_list.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    temp = slow.next
    slow.next = None
    return linked_list, temp


class LinkedList:
    def __init__(self, data):
        self.next = None
        self.data = data