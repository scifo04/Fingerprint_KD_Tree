class Node:

    def __init__(self,points,left,right):
        self.points = points
        if left == None:
            self.left = None
        else:
            self.left = left
        if right == None:
            self.right = None
        else:
            self.right = right

    def printDataTree(self):
        print("["+str(self.points[0])+","+str(self.points[1])+"]",end="")
    
    def printTree(self):
        if self != None:
            print("(",end="")
            self.printDataTree()
            if self.left != None:
                self.left.printTree()
            if self.right != None:
                self.right.printTree()
            print(")",end="")

    def printTreeIndentation(self,n):
        if self != None:
            self.printDataTree()
            if self.left != None:   
                print()     
                for i in range(n):
                    print(" ",end="")
                self.left.printTreeIndentation(2+n)
            if self.right != None:
                print()
                for i in range(n):
                    print(" ",end="")
                self.right.printTreeIndentation(2+n)

class KDTree:
    def __init__ (self, minutiae,d=0):
        if not minutiae:
            self.root = None
        else:
            length = len(minutiae[0])
            axis = d % length
            s_points = sorted(minutiae,key=lambda x: x[axis])
            med_id = len(s_points) // 2
            self.root = Node(s_points[med_id],None,None)
            self.root.left = KDTree(s_points[:med_id], d+1)
            self.root.right = KDTree(s_points[med_id+1:],d+1)

    def printDataTree_KD(self):
        print(str(self.root.points),end="")

    def printTreeIndentation_KD(self,n):
        if self.root != None:
            self.printDataTree_KD()
            if self.root.left != None:
                print()
                for i in range(n):
                    print(" ",end="")
                self.root.left.printTreeIndentation_KD(2+n)
            if self.root.right != None:
                print()
                for i in range(n):
                    print(" ",end="")
                self.root.right.printTreeIndentation_KD(2+n)

    def printTree_KD(self):
        if self.root != None:
            print("(",end="")
            self.printDataTree_KD()
            if self.root.left != None:
                self.root.left.printTree_KD()
            if self.root.right != None:
                self.root.right.printTree_KD()
            print(")",end="")

    def find_nearest_neighbor(self,q_point):
        best = None
        best_dist = float('inf')

        def find_nearest_neighbor_helper(node, depth=0):
            nonlocal best, best_dist
            if node is None:
                return
            k =  len(q_point)
            axis = depth % k
            closer_subtree = None
            farther_subtree = None
            if q_point[axis] < node.points[axis]:
                closer_subtree = node.left
                farther_subtree = node.right
            else:
                closer_subtree = node.right
                farther_subtree = node.left
            find_nearest_neighbor_helper(closer_subtree.root,depth+1)
            dist = sum((q_point[i]-node.points[i]) ** 2 for i in range(k))
            if dist < best_dist:
                best = node.points
                best_dist = dist
            if abs(q_point[axis] - node.points[axis]) < best_dist:
                find_nearest_neighbor_helper(farther_subtree.root,depth+1)
        find_nearest_neighbor_helper(self.root)
        return best