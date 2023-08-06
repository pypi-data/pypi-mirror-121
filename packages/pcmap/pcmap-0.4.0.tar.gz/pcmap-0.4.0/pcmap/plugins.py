def enrich_map(ccmap_in, pdbObj):
    """ Add x,y,z coordinates to atoms of provided atomic contact map"""    
    d = {}
    av = pdbObj.atomVectorize
    trace = [ (_.seqRes, _.chainID) for _ in pdbObj.trace ]

    for x, y, z, seqRes, chainID, resName, name in zip(*av[:]):
        d[ f"{name}{resName}{seqRes}{chainID}" ] = (name, resName, seqRes, chainID, x, y, z)

    ccmap_out = {"type" : "atomic_rich", "data": []}
    for a1, a2, dist in ccmap_in["data"]:
        #print (a1, a2)
        #print(d[''.join(a1)],  d[''.join(a2)], dist)
        ccmap_out["data"]. append( (d[''.join(a1)],  d[''.join(a2)], dist) )
    
    return ccmap_out