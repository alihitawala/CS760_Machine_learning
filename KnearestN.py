import math

def main() :
    feature_1 = [2,4,4,6,8,8]
    feature_2 = [3,4,5,3,3,4]
    class_label = ['Positive','Positive','Negative','Positive','Negative','Negative']
    ks = [1,2,3]
    instances = []
    for i in range(len(feature_1)) :
        instances.append(Instance(feature_1[i], feature_2[i], class_label[i]))
    for k in ks:
        print
        print "k = " + str(k) + "\\\\"
        for i in range(len(instances)):
            weights = []
            for j in range(len(instances)):
                if i == j:
                    continue
                dist = get_distance(instances[i].x, instances[i].y, instances[j].x, instances[j].y)
                weights.append(Weight(instances[j], dist, j))
            sorted_weights = sorted(weights, key=lambda x:x.distance)
            print "Instance = " + str(i+1) + " Class = " + str(instances[i].label) + "\\\\"
            for p in range(k):
                obj = sorted_weights[p]
                classification = "correctly " if instances[obj.index].label == instances[i].label else "incorrectly"
                print "Closest instance is Instance - " + str(obj.index + 1) + " with Manhattan distance " + str(obj.distance) + " Classified " + classification+ "\\\\ "

def run() :
    entries = []
    entries.append(Table(1,1,1,36))
    entries.append(Table(1,1,0,4))
    entries.append(Table(1,0,1,2))
    entries.append(Table(1,0,0,8))
    entries.append(Table(0,1,1,9))
    entries.append(Table(0,1,0,1))
    entries.append(Table(0,0,1,8))
    entries.append(Table(0,0,0,32))
    #XZ
    values = [(1,1), (1,0), (0,1), (0,0)]
    i_y_z = 0.0
    i_x_z = 0.0
    for value in values:
        p_xandz = 0.0
        p_yandz = 0.0
        p_x = 0.0
        p_y = 0.0
        p_z = 0.0
        for entry in entries:
            if entry.x == value[0] and entry.z == value[1]:
                p_xandz += entry.count
            if entry.y == value[0] and entry.z == value[1]:
                p_yandz += entry.count
        for entry in entries:
            if entry.x == value[0]:
                p_x += entry.count
            if entry.y == value[0]:
                p_y += entry.count
            if entry.z == value[1]:
                p_z += entry.count
        i_x_z += (p_xandz * math.log(p_xandz*100/(p_x*p_z), 2) / 100)
        i_y_z += (p_yandz * math.log(p_yandz*100/(p_y*p_z), 2) / 100)
    print i_x_z, i_y_z

class Table :
    def __init__(self, x,y,z,count):
        self.x = x
        self.y = y
        self.z = z
        self.count = count


def get_distance(x1,y1,x2,y2):
    return  abs(x1-x2) + abs(y2-y1)


class Instance:
    def __init__(self,x,y,label):
        self.x = x
        self.y = y
        self.label = label

class Weight:
    def __init__(self, instance, distance, index):
        self.instance = instance
        self.distance = distance
        self.index = index

run()