def ruleTranslate(s: str, p:str, o:str):
    '''
    Translate an RDF triple <s,p,o> to Horn Clause (~)x | (~)y,
    according to the natural semantic of the predicate.
    '''

    flags = []

    match p:

        case '22-rdf-syntax-ns#first': 
            #TODO
            '''
            counts 1475 in extracted subgraph
            '''
            pass

        case '22-rdf-syntax-ns#rest': 
            '''
            counts 1475 in extracted subgraph
            '''
            pass

        case 'IAO_0100001': 
            '''
            IAO_0100001 'term_replaced_by'
            logic expr: x<->y  =  (~x|y)&(x|~y)
            Definition: Use on obsolete terms, relating the term to another term that can be used as a substitute
            subgraph count: 156 '''
            #flags = [(False, True), (True, False)]
            pass

        case 'oboInOwl#consider': 
            #TODO
            '''
            counts 95 in extracted subgraph
            '''
            pass

        case 'oboInOwl#hasAlternativeId': 
            '''
            logic expr: x<->y  =  (~x|y)&(x|~y)
            subgraph count: 1015 '''
            #flags = [(False, True), (True, False)]
            #NOTE: temp inactivated
            pass

        case 'oboInOwl#inSubset': 
            #TODO
            '''
            counts 1834 in extracted subgraph
            '''
            pass

        case 'owl#disjointWith': 
            '''
            logic expr: ~x|~y
            subgraph count: 26'''
            #flags = [(False, False)]
            pass

        case 'owl#equivalentClass': 
            '''
            logic expr: x<->y  =  (~x|y)&(x|~y)
            subgraph count: 983 '''
            #flags = [(False, True), (True, False)]
            #NOTE: temp inactivated

        case 'owl#intersectionOf': 
            #TODO
            '''
            subgraph count: 939
            '''
            pass

        case 'owl#inverseOf': 
            '''
            Do NOT process.
            subgraph count: 1 '''
            pass

        case 'owl#onProperty':
            #TODO
            '''
            subgraph count: 1884 '''

            #flags = [(False, True)]

            match o:

                case 'BFO_0000050':
                    '''
                    part of
                    counts 8999 in owl '''
                    flags = [True]

                case 'BFO_0000051':
                    '''
                    has part
                    counts 864 in owl '''
                    pass

                case 'BFO_0000066':
                    '''
                    occurs in
                    counts 387 in owl '''
                    pass

                case 'RO_0002092':
                    '''
                    happens during
                    counts 30 in owl '''
                    pass

                case 'RO_0002211':
                    '''
                    regulates
                    counts 6623 in owl '''
                    flags = [True]

                case 'RO_0002212':
                    '''
                    negatively regulates
                    counts 5779 in owl '''
                    #NOTE: will change to false after adding pos/neg expr
                    flags = [True]

                case 'RO_0002213':
                    '''
                    positively regulates
                    counts 5801 in owl '''
                    flags = [True]

                case _:
                    pass

        case 'owl#propertyChainAxiom':
            #TODO
            '''
            counts 2 in extracted subgraph '''
            pass

        case 'owl#someValuesFrom':
            #TODO
            '''
            counts 1884 in extracted subgraph '''
            flags = [True]

        case 'rdf-schema#subClassOf':
            '''
            logic expr: ~x|y
            subgraph count: 8345 '''
            flags = [True]
    
        case 'rdf-schema#subPropertyOf':
            '''
            NOTE: temporarilt do NOTHING
            logic expr: ~x|y
            subgraph count: 22 '''
            pass
            #flags = [(False, True)]

    #if s < o:
    return [(s, o, f) for f in flags]
    #else:
    #    return [(o, s, f) for f in flags]
