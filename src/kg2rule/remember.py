def resolve(r1, r2, con_spec):
    '''
    return r=a|b,
    if r1=a|p and r2=b|~p and p not in concept sepcification
    '''

    for i1,i2 in [(0,0), (0,2), (2,0), (2,2)]:
        if (r1[i1+1] == r2[i2+1]) and (r1[i1] != r2[i2]) and\
            (r1[i1+1] not in con_spec) :

            ia = 2-i1
            ib = 2-i2

            if r1[ia+1] < r2[ib+1]:
                return (r1[ia], r1[ia+1], r2[ib], r2[ib+1])
            else:
                return (r2[ib], r2[ib+1], r1[ia], r1[ia+1])

    return None
