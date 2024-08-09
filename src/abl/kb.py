from numpy import percentile
from z3 import If, Implies, Int, Not, Solver, Sum, Or, sat, Bool
from ablkit.reasoning import KBBase
import pandas as pd
import time

class GO(KBBase):
    def __init__(self, rule_path, annotation_path, dom_path):

        ''' Define pseudo label convertion list & z3 solver '''
        super().__init__(pseudo_label_list=list(range(0,4807)), use_cache=False)
        self.solver = Solver()

        ''' Load GO rules and annotations '''
        rule_df = pd.read_csv(rule_path)

        self.annotation = pd.read_csv(annotation_path, header=None, index_col=0)
        print(self.annotation)


        ''' Define disjunction rules 
            and z3 constraint variables used in rules '''
        rules = []

        dom_set = pd.read_csv(dom_path, header=None)[0]
        for c in dom_set:
            globals().update( {c : Bool(c)} )

        self.concept_dom = set()
        for idx, row in rule_df.iterrows():
            rule = row

            self.concept_dom.add(rule.iloc[1])
            self.concept_dom.add(rule.iloc[3])

            globals().update( { rule.iloc[1] : Bool(rule.iloc[1]) } )
            globals().update( { rule.iloc[3] : Bool(rule.iloc[3]) } )
            ''' Define z3 variables '''

            rules.append(Or( eval(rule.iloc[1]) == rule.iloc[0], eval(rule.iloc[3]) == rule.iloc[2] ))
            ''' Translate disjunction rule '''

        self.cwa_constraints = set(eval(c)==False for c in self.concept_dom)


        ''' Define violated weights '''
        self.weights = {rule: 1 for rule in rules} 

        self.total_violation_weight = Sum(
            [If(Not(rule), self.weights[rule], 0) for rule in self.weights]
        )



    def logic_forward(self, pseudo_label, x):
        # 
        '''
        Define the logical rules.

        List related concepts of pseudo labels, by GO annotations.
        Check if input concepts and pseudo label concepts (converted from annotation)
        conform with rules (in disjunction form, mined from GO).

        NOTE: Truth values are interpreted under CWA (i.e. False if not in pseudo_label).
        '''

        solver = self.solver
        total_violation_weight = self.total_violation_weight
        self.solver.reset()


        ''' definie pseudo label and input concept set '''
        gene_pred       = [f'SO_{st:04}' for st in pseudo_label]
        concept_expand  = set(f'GO_{st:07}' for st in x[0])
        concept_pred = set()


        ''' convert pseudo label genes to GO concepts '''
        for g in gene_pred:
            if g not in self.annotation.index:
                continue

            for c in self.annotation.loc[g]:
                concept_pred.add(c)


        ''' Set unmentioned concepts as False (CWA) '''
        #spec_constraints = set(eval(c)==False for c in concept_expand.union(concept_pred))
        spec_constraints = set(eval(c)==False for c in concept_expand.union(concept_pred) if c in globals().keys()) #NOTE: temp

        solver.add(self.cwa_constraints - spec_constraints)


        ''' Set concepts in input and (converted) pseudo label as True '''
        for c in concept_expand.union(concept_pred):
            if c not in globals().keys():#NOTE:temp
                continue
            solver.add( eval(c) == True )


        if solver.check() == sat:
            ''' Satisfiable '''

            model = solver.model()
            total_weight = model.evaluate(total_violation_weight)
            return total_weight.as_long()

        else:
            ''' No solutions found '''

            return 1e10
