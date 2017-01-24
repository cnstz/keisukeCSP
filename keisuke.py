from csp import *
import sys
import timeit

def keisuke_constraints(A, a, B, b):
    """ 2 maura kelia den mporoun na sunoreuoun metaksi tous ektos ki an vriskontai diagwnia """
    blackA=[0,0]
    blackB =[0,0]
    if A[0] == 'H':
        blackA[0] = len(A) - 1 + a[0]
        blackA[1] = a[1]
    else:
        blackA[0] = a[0]
        blackA[1] = len(A) - 1 +a[1]
    if B[0] == 'H':
        blackB[0] = len(B) - 1 + b[0]
        blackB[1] = b[1]
    else:
        blackB[0] = b[0]
        blackB[1] = len(B) - 1 + b[1]
    if (blackA[0] + 1 == blackB[0] 
        and blackA[1] == blackB[1]) or (blackA[0] - 1 == blackB[0] 
                                        and blackA[1] == blackB[1]) or (blackA[1] + 1 == blackB[1] 
                                                                        and blackA[0] == blackB[0]) or (blackA[1] - 1 == blackB[1] 
                                                                                                        and blackA[0] == blackB[0]):
        return False
    """ 2 orizonties h 2 kathetes metavlhes den mporoun na peftoun h mia panw sthn allh """   
    if A[0] == 'H' and B[0] == 'H':
        if a[0] != b[0]:
            return True
        else:
            if a[1] < b[1]:
                if (a[1] + len(A) - 1) <= b[1]:
                    return True
                else:
                    return False
            else:
                if (b[1] + len(B) - 1) <= a[1]:
                    return True
                else:
                    return False
    if A[0] == 'V' and B[0] == 'V':
        if a[1] != b[1]:
            return True
        else:
            if a[0] < b[0]:
                if (a[0] + len(A) - 1) <= b[0]:
                    return True
                else:
                    return False
            else:
                if (b[0] + len(B) - 1) <= a[0]:
                    return True
                else:
                    return False
    """ 1 orizontia kai 1 katheti metavliti den mporoun na temonontai se psifia pou den periexoun kai oi 2 """
    coordA = dict()
    coordB = dict()
    i=0
    if A[0] == 'H':
        for letter in A[1:]:
            coordA[tuple([a[0], a[1]+i])] = letter
            i+=1
    else:
        for letter in A[1:]:
            coordA[tuple([a[0] + i, a[1]])] = letter
            i+=1
    i=0
    if B[0] == 'H':
        for letter in B[1:]:
            coordB[tuple([b[0], b[1] + i])] = letter
            i+=1
    else:
        for letter in B[1:]:
            coordB[tuple([b[0] + i, b[1]])] = letter
            i+=1
    for key in coordA:
        for key2 in coordB:
            if key == key2:
                if coordA[key] == coordB[key2]:
                    return True
                else:
                    return False
    """ An de temnontai katholou bainoun kanonika """
    return True
                              
class Keisuke(CSP):
    def __init__(self, horizontal_variables, vertical_variables, size):
        self.size = size + 1
        """ CREATING VARIABLES LIST """
        horizontal_variables = ['H' + str(var) + 'B' for var in horizontal_variables]
        vertical_variables = ['V' + str(var) + 'B' for var in vertical_variables]
        self.variables = horizontal_variables + vertical_variables
        """ CREATING DOMAINS DICT """
        list_of_positions = []
        for i in range(size):
            for j in range(size):
                list_of_positions.append([i,j])
        self.domains = dict()
        for var in self.variables:
            temp_list = []
            """ Periorismos gia tis sidetagmenes apo tis opoies borei na arxizei kathe akolouthia analoga me to megethos ths """
            temp_list = [i for i in list_of_positions if i[0] < self.size and i[1] < self.size and var[0] == 'V' and (len(var)-1 + i[0]) <= self.size or var[0] == 'H' and (len(var)-1 + i[1]) <= self.size ]
            self.domains[var] = (temp_list)
        """ CREATING NEIGHBORS DICT """
        self.neighbors = dict()
        neig = []
        for var in self.variables:
            neig = [i for i in self.variables if i!=var]
            self.neighbors[var] = neig
        CSP.__init__(self, self.variables, self.domains, self.neighbors,
                     keisuke_constraints)
    
    def display(self, assignment):
        for i in range(self.size):
            for j in range(self.size):
                    for k in assignment:
                        if assignment[k] == [i,j]:
                            if k[0]=='V':
                                print "Vertical", k[1:-1], "position:", assignment[k]  
                            else:
                                print "Horizontal", k[1:-1], "position:", assignment[k]                              


k = Keisuke([23, 32, 233], [333, 23], 3)
print "Horizontal: [23, 32, 233], Vertical:[333, 23], Size:3"
print "Running Keisuke with BT"
start = timeit.default_timer()
backtracking_search(k);
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with BT+MRV"
start = timeit.default_timer()
backtracking_search(k, select_unassigned_variable=mrv)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with FC"
start = timeit.default_timer()
backtracking_search(k, inference=forward_checking)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with FC+MRV"
start = timeit.default_timer()
backtracking_search(k, select_unassigned_variable=mrv, inference=forward_checking)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with Min-Conflicts"
start = timeit.default_timer()
min_conflicts(k)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

k = Keisuke([322, 233, 2122], [22, 3313, 232, 21], 4)
print "Horizontal: [322, 233, 2122], Vertical:[22, 3313, 232, 21], Size:4"
print "Running Keisuke with BT"
start = timeit.default_timer()
backtracking_search(k);
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with BT+MRV"
start = timeit.default_timer()
backtracking_search(k, select_unassigned_variable=mrv)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with FC"
start = timeit.default_timer()
backtracking_search(k, inference=forward_checking)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with FC+MRV"
start = timeit.default_timer()
backtracking_search(k, select_unassigned_variable=mrv, inference=forward_checking)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with Min-Conflicts"
start = timeit.default_timer()
min_conflicts(k)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

k = Keisuke([13, 23, 233, 3221, 21222], [12, 21, 22, 232, 3132, 33313], 5)
print "Horizontal: [13, 23, 233, 3221, 21222], Vertical:[12, 21, 22, 232, 3132, 33313], Size:5"
print "Running Keisuke with BT"
start = timeit.default_timer()
backtracking_search(k);
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with BT+MRV"
start = timeit.default_timer()
backtracking_search(k, select_unassigned_variable=mrv)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with FC"
start = timeit.default_timer()
backtracking_search(k, inference=forward_checking)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with FC+MRV"
start = timeit.default_timer()
backtracking_search(k, select_unassigned_variable=mrv, inference=forward_checking)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

print "Running Keisuke with Min-Conflicts"
start = timeit.default_timer()
min_conflicts(k)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print