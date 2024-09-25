from ablkit.reasoning import KBBase
import pandas as pd

class GO(KBBase):
    def __init__(self, single_gene : str, rule_path : str, annotation_path : str, logger):

        ''' Define pseudo label convertion list & z3 solver '''
        super().__init__(pseudo_label_list=[0,1], use_cache=False, logger=logger)

        #NOTE: temp
        #rule_path = 'rules/single_genes/SO_0014_sg_rule_test_modify.csv'

        ''' Load GO rules and annotations
            Define set of concepts related to current single gene '''
        print(rule_path)
        self.rule_df = pd.read_csv(rule_path, header=None)
        annotation = pd.read_csv(annotation_path, header=None, index_col=0)
        sg_row = annotation.loc[single_gene]
        self.goa_con_set = eval(sg_row[1])


    def logic_forward(self, pseudo_label, x):
        # 
        '''
        Define the logical rules.

        List related concepts of pseudo labels, by GO annotations.
        Check if input concepts and pseudo label concepts (converted from annotation)
        conform with rules (in disjunction form, mined from GO).

        NOTE: Truth values are interpreted under CWA (i.e. False if not in pseudo_label).
        '''


        ''' definie pseudo label and input concept set '''
        concept_input = set(f'GO_{st:07}' for st in x[0])
        pred_expr = pseudo_label[0]

        ''' check rules in rule dataframe '''
        vio_cnt = 0
        for i, row in self.rule_df.iterrows():
            if row[0] in concept_input and row[1] in self.goa_con_set:
                ''' if current gene regulated by input cond, but not expressed '''
                if pred_expr == 0:
                    vio_cnt += 5

            if row[0] not in concept_input and row[1] in self.goa_con_set:
                ''' if current gene not regulated by input cond, but expressed '''
                if pred_expr == 1:
                    vio_cnt += 0
                    #NOTE: handle this case?

            if row[0] in self.goa_con_set and row[1] in concept_input:
                ''' if current gene regulates input cond, but not expressed '''
                if pred_expr == 0:
                    vio_cnt += 5

            if row[0] in self.goa_con_set and row[1] not in concept_input:
                ''' if conditions regulated by current gene not shown in input '''
                if pred_expr == 1:
                    vio_cnt += 1

        #print(pred_expr, vio_cnt)
        return vio_cnt
