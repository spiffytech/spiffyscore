import pdb

class Tree():
    def __init__(self, name):
        self.nodes = []
        self.name = name

    def traverse_depth_first(self):
        all_nodes = []
        for node in self.nodes:
            if isinstance(node, Node):
                all_nodes.append(node)
            elif isinstance(node, Tree):
#                pdb.set_trace()
                all_nodes.extend(node.traverse_depth_first())
        return all_nodes

    def __str__(self):
        return str(self.__unicode__())
    def __unicode__(self):
        return self.nodes


class Node():
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data

    def __str__(self):
        return str(self.__unicode__())
    def __unicode__(self):
        return self.data
