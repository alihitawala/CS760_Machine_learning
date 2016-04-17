__author__ = 'aliHitawala'
import collections

def main():
    s = raw_input()
    dictionary = dict()
    for c in s:
        dictionary[c] = (dictionary[c] + 1) if c in dictionary else 1
    for c in s:
        if dictionary[c] > 1:
            return c


def gcd(p, q):
    while q != 0:
        temp = q
        q = p % q
        p = temp
    return p


def relatively_prime(a, b, dictionary):
    obj = Key(a, b)
    if obj in dictionary :
        return dictionary[obj] == 1
    else:
        dictionary[obj] = gcd(a, b)
        return dictionary[obj] == 1


def coprimeCount(a):
    dictionary = dict()
    b = []
    for i in range(len(a)):
        count = 0
        for j in range(1, a[i] + 1):
            if relatively_prime(j, a[i], dictionary):
                count += 1
        b.append(count)
    return b

class Key:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y) or (self.y, self.x) == (other.y, other.x)


def merge():
    values = raw_input()
    size = len(values)
    parent = []
    count = size
    for i in range(size):
        parent.append(i)
    for i in range(size):
        element = int(values[i]) - 1
        p = i
        q = element
        if is_connected(p, q, parent):
            continue
        count = union(p, q, parent, count)
    if parent[0] != 0:
        present = False
        for p in parent:
            if p == 0:
                present = True
                break
        if present:
            print count - 1
        else:
            print count
    else:
        print count-1


def find(p, parent):
    while p != parent[p]:
        p = parent[p]
    return p


def is_connected(p, q, parent):
    return find(p, parent) == find(q, parent)


def union(p,q,parent, count):
    rp = find(p, parent)
    rq = find(q, parent)
    if rp == rq:
        return count
    parent[rp] = rq
    return count-1



def tfidf(x_tok, y_tok, corpus_list = None):
    """
    Compute tfidf measures between two lists given the corpus information.
    This measure employs the notion of TF/IDF score commonly used in information retrieval (IR) to find documents that are relevant to keyword queries.
    The intuition underlying the TF/IDF measure is that two strings are similar if they share distinguishing terms.

    Args:
        x_tok, y_tok (list): Input lists
        corpus_list (list of lists): Corpus list (default is set to None). If set to None,
        the input list are considered the only corpus

    Returns:
        TF-IDF measure between the input lists

    """
    if corpus_list is None:
        corpus_list = [x_tok, y_tok]
    corpus_size = len(corpus_list)
    tf_x, tf_y = collections.Counter(x_tok), collections.Counter(y_tok)
    element_freq = {}
    total_unique_elements = set()
    for document in corpus_list:
        temp_set = set()
        for element in document:
            temp_set.add(element)
            total_unique_elements.add(element)
        for element in temp_set:
            element_freq[element] = element_freq[element]+1 if element in element_freq else 1
    idf, v_x, v_y, v_x_y, v_x_2, v_y_2 = {}, {}, {}, 0.0, 0.0, 0.0
    for element in total_unique_elements:
        idf[element] = corpus_size * 1.0 /element_freq[element]
        v_x[element] = idf[element] * tf_x[element]
        v_y[element] = idf[element] * tf_y[element]
        v_x_y += v_x[element] * v_y[element]
        v_x_2 += v_x[element] * v_x[element]
        v_y_2 += v_y[element] * v_y[element]
    return v_x_y/()

tfidf(['a', 'b', 'a'], ['a', 'c'],
      [['a', 'b', 'a'], ['a', 'c'], ['a']])
