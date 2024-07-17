from z3 import If, Implies, Int, Not, Solver, Sum, sat  
from ablkit.reasoning import KBBase

class GO(KBBase):
    def __init__(self):
        # here the 0 is not the categories of the GO, need to change it
        super().__init__(pseudo_label_list=list(range(0)), use_cache= False)

        self.solver = Solver()

        # Load the information of GO dataset
        # TODO()

        # Define the variables and rule
        rules = []
        # TODO()

        # Define the weights and violated weights
        self.weights = {rule: 1 for rule in rules}
        self.total_violation_weight = Sum(
            [If(Not(rule), self.weights[rule], 0) for rule in self.weights]
        )
        # TODO()


    def logic_forward(self, pseudo_label, data_point):
        # Define the logical rules
        # TODO()

        # Steps as follow:
        # 1.Initial the variable 
        
        # 2.Reset the solver

        # 3.Add the attribute restrictions

        # 4.Add the aim restrictions

        # 5.Check the state of solver

        return 