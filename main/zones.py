def detectZones(signal):
    if(signal == "zone1"):
        z1 = True
        z2 = False
        z3 = False
    
    if(signal == "zone2"):
        z1 = False
        z2 = True
        z3 = False
    
    if(signal == "zone1"):
        z1 = False
        z2 = False
        z3 = True
    
    return z1,z2,z3