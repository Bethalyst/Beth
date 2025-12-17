
import graphviz
import pandas
import os


def save_graph_as_jpg(graph, filename):
    graph.save('temp.dot')
    src = graphviz.Source.from_file('temp.dot')
    src.render(filename, format="jpg")
    os.remove(filename)
    os.remove('temp.dot')

class Node:
    def __init__(self, data, left = None, right = None):
        self.left = left
        self.right = right
        self.data = data

print("Reading CSV file")
df = pandas.read_csv('decisionTree.csv', index_col = "ID") # df is "data frame"

#replace all occurances of "Not A Number" (NaN) with "Nothing" (None)
df.replace({float("nan"): None}, inplace=True) 

#print("Data Frame: ")
#print(df.to_string())

# Create Nodes for all entries in dataframe
nodeMap = {None:None}

#process your data frame from the bottom up 
print("Creating Nodes for Tree")
for index in reversed(df.index.values):
    #print("Creating Node for: ",index)
    nodeMap[index] = Node(df.loc[index]["Label"],nodeMap[df.loc[index]["Left Child"]],nodeMap[df.loc[index]["Right Child"]])
    


print("Building the Tree")
graph = graphviz.Digraph('structs', filename='structs.gv', node_attr={'shape': 'plaintext', 'ordering':'out'})

# Assemble the tree top-down
for node in reversed(nodeMap.values()):
    if(node == None):
        break

    print("Inserting node for: ",node.data)
    graph.node(node.data)
    if node.left:
        graph.edge(node.data, node.left.data)
    if node.right:
        graph.edge(node.data, node.right.data)

print("Saving the Tree to JPEG")
save_graph_as_jpg(graph, "Decisiontree")




