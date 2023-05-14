

from re import X
# Base Classes

# PREDICATE - ON, ONTABLE, CLEAR, HOLDING, ARMEMPTY
class PREDICATE:
    def _str_(self):
        pass

    def _repr_(self):
        pass

    def _eq_(self, other):
        pass

    def _hash_(self):
        pass   

    def get_action(self, world_state): 
        pass
# OPERATIONS - Stack, Unstack, Pickup, Putdown
class Operation:
    def _str_(self):
        pass

    def _repr_(self):
        pass

    def _eq_(self, other):
        pass

    def precondition(self):
        pass

    def delete(self):
        pass

    def add(self):
        pass
class ON(PREDICATE):
    def _init_(self, X, Y):
        self.X = X
        self.Y = Y

    def ___str__(self):
        return "ON({X},{Y})".format(X=self.X, Y=self.Y)
    
    def __repr__(self):
        return self. str ()
    
    def ___eq__(self, other):
        return self. _dict_ == other. __dict__ and self. __class__ == other. __class___ 

    def __hash__(self):
        return hash(str(self))

    def get_action(self, world_state):
        return StackOp (self.X, self.Y)

class ONTABLE(PREDICATE):

    def _init_(self, X):
        self.X = X

    def ___str__(self):
        return "CLEAR ({X})".format(X=self.X)
        self.X = X
    
    def __repr__(self):
        return self.__str__()

    def ___eq__(self, other):
        return self._dict_== other. __dict__ and self.__class__== other.__class____
    
    def ___hash__(self):
        return hash(str(self))

    def get_action(self, world_state):
        for predicate in world_state:
            # If Block is on another block, unstack
            if isinstance (predicate, ON)  and predicate.Y == self.X:
                return UnstackOp (predicate.X, predicate.Y)
            return None

class HOLDING (PREDICATE):
    def _init_(self, X):
        self.X =X

    def ___str__(self):
        return "HOLDING({X})".format(X=self.X)
    
    def __repr__(self):
        return self.__str__()

    def ___eq__(self, other):
        return self._dict_== other.__dict__ and self.__class__== other.__class___
    
    def ___hash_(self):
        return hash(str(self))

    def get_action(self, world_state):
        X = self.X
        # If block is on table, pick up 
        if ONTABLE (X) in world_state:
            return PickupOp(X)
        # If block is on another block, unstack 
        else:
            for predicate in world_state:
                if isinstance(predicate, ON) and predicate.X == X:
                    return UnstackOp(X, predicate)

class ARMEMPTY(PREDICATE):
    def _init_(self):
        pass

    def _str__(self):
        return "ARMEMPTY"

    def __repr__(self):
        return self.__str__()

    def ___eq__(self, other):
        return self._dict__ == other. __dict__ and self.__class__== other.__class__

    def ___hash__(self):
        return hash(str(self))

    def get_action(self, world_state=[]) :
        for predicate in world_state:
            if isinstance(predicate, HOLDING): 
                return PutdownOp(predicate.X)
            return None

class StackOp(Operation):

    def _init_(self, X, Y):
        self.X = X
        self.Y = Y
    
    def ___str__(self):
        return "STACL({X}, {Y})".format(X=self.X, Y=self.Y)

    def __repr__(self):
        return self.__str__()

    def ___eq__(self, other):
        return self._dict_ == other.__dict__ and self.__class__== other.__class___

    def precondition(self):
        return [CLEAR(self.Y), HOLDING(self.X)]

    def delete(self):
        return [CLEAR(self.Y), HOLDING(self.X)] 

    def add(self):
        return [ARMEMPY(), ON(self.X, self.Y)]

class UnstackOp (Operation):

    def _init_(self, X, Y):
        self.X = X
        self.Y = Y

    def ___str__(self):
        return "UNSTACK({X},{Y})".format(X=self.X, Y=self.Y)

    def ___repr__(self):
        return self.__str__()

    def ___eq__(self, other) :
        return self.__dict__ == other.__dict__ and self.__class__== other.__class___ 
    def precondition(self):
        return [ARMEMPTY(), ON(self.X, self.Y), CLEAR(self.X)]
    def delete(self):
        return [ARMEMPTY(), ON(self.X, self.Y)]
    def add(self):
        return [CLEAR(self.Y), HOLDING(self.X)]

class PickupOp (Operation) :
    def __init__(self, X):
        self.X = X
    
    def ___str__(self):
        return "PICKUP({X})".format(X=self.X)
    
    def __repr__(self):
        return self.__str__()
    
    def ___eq__(self, other):
        return self._dict_ == other.__dict__ and self.__class__== other.__class__

    def precondition(self):
        return [CLEAR(self.X), ONTABLE(self.X), ARMEMPTY()]
    
    def delete(self):
        return [ARMEMPTY(), ONTABLE(self.X)]

    def add(self):
        return [HOLDING(self.X)]
    
class PutdownOp (Operation):

    def __init__(self, X):
        self.X = X
    def ___str__(self):
        return "PUTDOWN({X})".format(X=self.X)

    def __repr__(self):
        return self. str ()
    
    def ___eq__(self, other):
        return self._dict_ == other.__dict__ and self.__class__== other.__class__
    
    def precondition(self):
        return [HOLDING(self.X)]
    
    def delete(self):
        return [HOLDING(self.X)]
    
    def add(self):
        return [ARMEMPTY(), ONTABLE(self.X)]
    
def inPredicate(obj):
    predicates = [ON, ONTABLE, CLEAR, HOLDING, ARMEMPTY]
    for predicate in predicates:
        if isinstance(obj, predicate): return True
    return False

def isOperation(obj):
    operations = [StackOp, UnstackOp, PickupOp, PutdownOp]
    for operation in operations:
        if isinstance(obj, operation): return True
    return False

def arm_status(world_state):
    for predicate in world_state:
        if isinstance(predicate, HOLDING):
            return predicate
        return ARMEMPTY()

class GoalStackPlanner:
    def init (self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def get_steps(self):

        # Store Steps
        steps = []

        # Program Stack
        stack = []

        # World State/Knowledge Base
        world_state = self.initial_state.copy()

        # Initially push the goal_state as compound goal onto the stack
        stack.append(self.goal_state.copy())

        # Repeat until the stack is empty
        while len(stack) != 0:

            # Get the top of the stack
            stack_top = stack[-1]

            if type(stack_top) is list:
                compound_goal = stack.pop()
                for goal in compound_goal:
                    if goal not in world_state:
                        stack.append(goal)

            elif isOperation(stack_top):

                # Peek the operation
                operation = stack[-1]
                
                all_preconditions_satisfied = True

                # Check if any precondition is unsatisfied and push it onto program stack

                for predicate in operation.delete():
                    if predicate not in world_state:
                        all_preconditions_satisfied = False
                        stack.append(predicate)

                # If all preconditions are satisfied, pop operation from stack and execute it
                if all_preconditions_satisfied:

                    stack.pop()
                    steps.append(operation)

                    for predicate in operation.delete():
                        world_state.remove(predicate)
                    for predicate in operation.add():
                        world_state.append(predicate)

            # If Stack Top is a single satisfied goal
            elif stack_top in world_state:
                stack.pop()

            # If Stack Top is a single unsatisfied goal
            else:
                unsatisfied_goal = stack.pop()

                action = unsatisfied_goal.get_action(world_state)

                stack.append(action)

                # Push Precondition on the stack
                for predicate in action.precondition():
                    if predicate not in world_state:
                        stack.append(predicate)
        return steps

if __name__== '_main_' :
    initial_state = [
        ON('B', 'A'),
        ONTABLE('A'), ONTABLE('C'), ONTABLE('D'),
        CLEAR('B'), CLEAR('C'), CLEAR('D'),
        ARMEMPTY()
    ]

    goal_state = [
        ON('B', 'D'), ON('C', 'A'),
        ONTABLE('D'), ONTABLE('A'),
        CLEAR('B'), CLEAR('C'),
        ARMEMPTY()
    ]
#tugas 05-1A
if __name__== '_main_' :
    initial_state = [
        ON('3', '2'), ON('6', '5'), ON('5', '4'),
        ONTABLE('1'), ONTABLE('3'), ONTABLE('6'),
        CLEAR('1'), CLEAR('2'), CLEAR('4'),
        ARMEMPTY()
    ]

    goal_state = [
        ON('3', '1'), ON('6', '3'), ON('5', '4'), ON('2', '5'),
        ONTABLE('1'), ONTABLE('4'),
        CLEAR('2'), CLEAR('6'),
        ARMEMPTY()
    ]
#tugas 05-1B
if __name__== '_main_' :
    initial_state = [
        ON('Y', 'B'), ON('G', 'R'), ON('R', 'B'),
        ONTABLE('R'), ONTABLE('Y'), ONTABLE('G'),
        CLEAR('R'), CLEAR('B'), CLEAR('B'),
        ARMEMPTY()
    ]

    goal_state = [
        ON('R', 'R'), ON('B', 'R'),
        ONTABLE('B'), ONTABLE('G'), ONTABLE('R'), ONTABLE('Y'),
        CLEAR('Y'), CLEAR('Y'), CLEAR('B'), CLEAR('G'), CLEAR('B'), 
        ARMEMPTY()
    ]
#tugas 05-1C
if __name__== '_main_' :
    initial_state = [
        ON('b', 'a'), ON('d', 'e'), ON('b', 'd'),
        ONTABLE('b'), ONTABLE('d'), ONTABLE('c'),
        CLEAR('a'), CLEAR('e'), CLEAR('c'),
        ARMEMPTY()
    ]

    goal_state = [
        ON('b', 'a'), ON('c', 'b'), ON('a', 'c'), ON('e', 'a'),
        ONTABLE('d'),
        CLEAR('e'),
        ARMEMPTY()
    ]
    
    goal_stack = GoalStackPlanner(initial_state=initial_state,goal_state=goal_state)
    steps = goal_stack.get_steps()
    print(steps)