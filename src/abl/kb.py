from numpy import percentile
from z3 import If, Implies, Int, Not, Solver, Sum, Or, sat, Bool
from ablkit.reasoning import KBBase
import pandas as pd

class GO(KBBase):
    def __init__(self, rule_path, annotation_path, dom_path, max_depth):

        super().__init__(pseudo_label_list=list(range(0,4807)), use_cache=False)

        self.solver = Solver()

        ''' Load the information of GO kb '''
        rule_df = pd.read_csv(rule_path)

        self.annotation = pd.read_csv(annotation_path, header=None, index_col=0)
        print(self.annotation)
        #self.annotation[1] = self.annotation[1].apply(eval)

        self.concept_dom = set()

        ''' Define the variables and rule '''
        rules = []

        dom_set = pd.read_csv(dom_path, header=None)[0]
        for c in dom_set:
            globals().update( {c : Bool(c)} )
        


        for idx, row in rule_df.iterrows():
            #rule = eval(row[0])
            rule = row

            self.concept_dom.add(rule.iloc[1])
            self.concept_dom.add(rule.iloc[3])

            globals().update( { rule.iloc[1] : Bool(rule.iloc[1]) } )
            globals().update( { rule.iloc[3] : Bool(rule.iloc[3]) } )
            #exec(
            #    f"globals().update({Bool('{row[1]}')"
            #    f"globals()['{row[3]}'] = Bool('{row[3]}')"
            #)  # or use dict to create var and modify rules

            #print(rule.iloc[1], type(rule.iloc[1]), globals()[rule.iloc[1]], rule.iloc[3])
           
            if rule.iloc[0] == True:
                r1 = eval(rule.iloc[1])
            else:
                r1 = Not(eval(rule.iloc[1]))
            if rule.iloc[2] == True:
                r2 = eval(rule.iloc[3])
            else:
                r2 = Not(eval(rule.iloc[3]))
            rules.append(Or( r1, r2 ))

        #print('rules=', rules)
        # Define the weights and violated weights
        self.weights = {rule: 1 for rule in rules}  # Assuming the first column is the rule
        #print(rules)
        #print(self.weights)
        #assert(0)
        self.total_violation_weight = Sum(
            [If(Not(rule), self.weights[rule], 0) for rule in self.weights]
        )

        #self.max_depth = max_depth

    def logic_forward(self, pseudo_label, x):
        # Define the logical rules
        # TODO()
        '''
        expand through rule graph with x as start point, for d iterations.
        record all concepts on the expandition path, and map to gene id with annotation.
        return gene id as logic result.

        **use pseudo label?**
        (current: intersection of pseudo label and rule results)
        '''
        #return 0
        #print(pseudo_label,x)
        solver = self.solver
        total_violation_weight = self.total_violation_weight

        violated = 0  # count of violated rules
        # expr = set()

        #print('pseudo_label', pseudo_label)
        #print('x', x)
        gene_pred       = [f'SO_{st:04}' for st in pseudo_label]
        concept_expand  = set(f'GO_{st:07}' for st in x[0])
        concept_pred = set()
        concept_abd  = set()

        #for idx, row in self.annotation.iterrows():
        #    for g in gene_pred:
        #        if g in row[1]:
        #            concept_pred.append(row[0])
        for g in gene_pred:
            if g not in self.annotation.index:
                continue

            for c in self.annotation.loc[g]:
                concept_pred.add(c)

        #print(gene_pred)
        #print(concept_expand)

            # if row[0] in concept_expand:
            #    for id in row[1]:
            #        expr.add(id)

        ''' expand rule on each x and count violated num '''
        # for d in self.max_depth:

        # concept_new = []
        #for idx, row in self.rule_set.iterrows():
        #    for c in concept_expand:
        #        if row[0][1] == c:
        #            # concept_new.append(row[0][3])
        #            concept_abd.append(row[0][3])
        #        if row[0][3] == c:
        #            # concept_new.append(row[0][1])
        #            concept_abd.append(row[0][1])

        self.solver.reset()
        #for c in concept_expand:
        #    if c not in globals().keys():#NOTE:temp
        #        continue
        #    #globals().update({c:True})
        #    print(eval(c))
        #    solver.add( eval(c) == True )

        #for c in concept_pred:
        #    if c not in globals().keys():#NOTE:temp
        #        continue
        #    #globals().update({c:True})
        #    print(eval(c))
        #    solver.add( eval(c) == True )

        for c in self.concept_dom:
            if c in concept_expand or c in concept_pred:
                solver.add( eval(c) == True )
            else:
                solver.add( eval(c) == False )

        #for c in concept_abd:
        #for c in self.concept_dom:
        #    if c not in concept_expand and c not in concept_pred:
        #        #violated += 1
        #        solver.add( c == False )

        # print("violated", violated)
        #return violated
        #print('test')
        if solver.check() == sat:
            model = solver.model()
            #print(x, pseudo_label)
            #print(model)
            #print('total_violation_weight', type(total_violation_weight))
            #print(total_violation_weight)
            total_weight = model.evaluate(total_violation_weight)
            #print('total_weight',type(total_weight))
            #total_weight = model.evaluate(Sum([If(Not(rule), self.weights[rule], 0) for rule in self.weights]))
            #print(total_weight)
            return total_weight.as_long()
        else:
            # No solution found
            return 1e10

        # concept_expand = concept_new

        # res = []
        # for c in pseudo_label:
        #    if c in expr:
        #        res.append(c)

        # expected to be 0 when consistent

        # Steps as follow:
        # 1.Initial the variable

        # 2.Reset the solver

        # 3.Add the attribute restrictions

        # 4.Add the aim restrictions

        # 5.Check the state of solver
