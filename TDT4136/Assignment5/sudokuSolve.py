#!/usr/bin/python

import copy
import itertools
import timeit

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [ (i, j) for i in self.constraints for j in self.constraints[i] ]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [ (i, var) for i in self.constraints[var] ]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)


####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################


    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        #print assignment
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        newAssignment = copy.deepcopy(assignment)
        return self.backtrack(newAssignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        #Test for completeness: If all domains have length 1 we are done, this means that all variables have a unique value associated to it.
        global numOfCalls
        global numOfFailures
        numOfCalls += 1
        if all(len(item) == 1 for item in assignment.values()):
            return assignment
        
        #This returns name of a variable with domain length greater than 1, i.e. a variable that is yet undecided
        var = self.select_unassigned_variable(assignment)
        #Loop through the values in the domain of the chosen variable
        for value in assignment[var]:
            #deep copy of assignment for each iteration, see note
            newAssignment = copy.deepcopy(assignment)
            #check if the variable and value pair is consistent
            if self.consistent(newAssignment, var, value):
                #If the pair is consistent, we want to try to assign it, but keep the old temporarily
                temp = newAssignment[var]
                newAssignment[var] = [value]
                #If this new assignment does not lead to an inference failure (i.e. arc inconsistency), we continue by recursion if the assignment is valid
                if self.inference(newAssignment, self.get_all_arcs()):
                    result = self.backtrack(newAssignment)
                    if result != 'failure':
                        return result
                #We have an arc inconsistency, so we reset the assignment we tried.
                newAssignment[var] = temp
        #If none of the values in the domain of the chosen variable are consistent, return failure; we need to backtrack.
        numOfFailures+=1
        return 'failure'
        pass

    def consistent(self, assignment, var, value):
        #Any assignment where two or more variables have the same value falsifies the constraint.
        return all(assignment[constraint] != value for constraint in self.constraints[var])

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        #Return the name of one of the variables with smallest domain
        return min([var for var in  assignment.keys() if len(assignment[var])>1], key=assignment.get)
        pass

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        while queue:
            #while queue is not empty pop first arc from queue
            (i,j) = queue.pop(0)
            #If the domain of i is reduced (i.e. revise returns true), we might be able to revise neighbours of i as well,
            #so we need to update neighbours of i (i.e. run inference on the neighbouring arcs)
            if self.revise(assignment, i, j):
                #if revision removes all possible values from domain, return false. This would imply no (arc) consistent solution.
                if len(assignment[i]) == 0:
                    return False
                #loop through neighbouring arcs of i different from j, add to queue at end.
                for k in self.get_all_neighboring_arcs(i):
                    if k != (i,j):
                        queue.append(k)
            #If the arc is not revised, continue to next option in queue.
        #looped through the whole of queue without any false => return true
        return True
        pass

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        revised = False
        #loop through the values in the domain of i
        for x in assignment[i]:
            relationFound = False
            #The following snippet evaluates if there exists an y in the domain of j such that 
            #(x,y) satisfies the constraint between variable i and variable j. 
            #If that is the case relationFound is set to True and we continue with next x in the domain of i.
            #If not, then x is removed from the domain of i, because no pair (x,y) is valid.
            for y in assignment[j]:
                if (x,y) in self.constraints[i][j]:
                    relationFound = True
                    break
            if relationFound == False:
                assignment[i].remove(x)
                revised = True
        #function returns True/False based on whether or not the domain of i is revised or not.
        return revised
        pass


####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = [ 'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T' ]
    edges = { 'SA': [ 'WA', 'NT', 'Q', 'NSW', 'V' ], 'NT': [ 'WA', 'Q' ], 'NSW': [ 'Q', 'V' ] }
    colors = [ 'red', 'green', 'blue' ]
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [ board[row][col] ])

    for row in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for col in range(9) ])
    for col in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for row in range(9) ])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print solution['%d-%d' % (row, col)][0],
            if col == 2 or col == 5:
                print '|',
        print
        if row == 2 or row == 5:
            print '------+-------+------'

userInput = input('Choose board (1-4): ')
while userInput not in [1,2,3,4]:
    userInput = input('Choose board (1-4): ')
if userInput == 1:
    choice = 'easy'
elif userInput == 2:
    choice = 'medium'
elif userInput == 3:
    choice = 'hard'
elif userInput == 4:  
    choice = 'veryhard'

start = timeit.default_timer()
csp = create_sudoku_csp(choice + '.txt')
numOfCalls = 0
numOfFailures = 0
if csp.backtracking_search() != 'failure':
    print_sudoku_solution(csp.backtracking_search())
else:
    print 'Error: Failed'
stop = timeit.default_timer()

print '\n'
print 'Number of calls: %d' % numOfCalls
print 'Number of failures: %d' % numOfFailures
print 'Runtime: %f seconds' % (stop - start)
