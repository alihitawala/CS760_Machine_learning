import math

def main() :
    feature_1 = [2,4,4,6,8,8]
    feature_2 = [3,4,5,3,3,4]
    class_label = [1,1,0,1,0,0]
    ks = [1,2,3]
    instances = []
    for i in range(len(feature_1)) :
        instances.append(Instance(feature_1[i], feature_2[i], class_label[i]))
    for k in ks:
        for i in range(len(instances)):
            weights = []
            for j in range(len(instances)):
                if i == j:
                    continue
                dist = get_distance(instances[i].x, instances[i].y, instances[j].x, instances[j].y)
                weights.append(Weight(instances[j], dist))
            sorted_weights = sorted(weights, key=lambda x:x.distance)
            print "k = " + str(k) + " Instance = " + str(i+1)
            for i in range(k):
                print str(sorted_weights[i].distance) + "  Feature 1 = " + str(sorted_weights[i].instance.x) \
                      + "  Feature 2 = " + str(sorted_weights[i].instance.y) + "  Class = " + str(sorted_weights[i].instance.label)


def get_distance(x1,y1,x2,y2):
    temp = ((x1-x2) * (x1-x2)) * 1.0 + ((y1-y2) * (y1-y2)) * 1.0
    return math.sqrt(temp)


class Instance:
    def __init__(self,x,y,label):
        self.x = x
        self.y = y
        self.label = label

class Weight:
    def __init__(self, instance, distance):
        self.instance = instance
        self.distance = distance

main()