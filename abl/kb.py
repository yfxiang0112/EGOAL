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
        # TODO()

        # Define the weights and violated weights
        # TODO()

    def logic_forward(self, pseudo_label, data_point):
        # Define the logical rules
        # TODO()
        return 