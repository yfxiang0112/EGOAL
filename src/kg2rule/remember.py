def resolve(r1, r2, con_spec):
    '''
    return r=a->b,
    if r1=a->p and r2=p->b
    or r2=a->p and r1=p->b, and p not in concept sepcification
    '''

    if r1[1] == r2[0]:
        if r1[0] != r2[1] and r1[1] not in con_spec:
            return (r1[0], r2[1], not(r1[2]^r2[2]))

    elif r2[1] == r1[0]:
        if r2[0] != r1[0] and r2[1] not in con_spec:
            return (r2[0], r1[1], not(r1[2]^r2[2]))

    #for i1,i2 in [(0,0), (0,2), (2,0), (2,2)]:
    #    if (r1[i1+1] == r2[i2+1]) and (r1[i1] != r2[i2]) and\
    #        (r1[i1+1] not in con_spec) :

    #        ia = 2-i1
    #        ib = 2-i2

    #        if r1[ia+1] < r2[ib+1]:
    #            return (r1[ia], r1[ia+1], r2[ib], r2[ib+1])
    #        else:
    #            return (r2[ib], r2[ib+1], r1[ia], r1[ia+1])

    return None
