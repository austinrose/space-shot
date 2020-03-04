mass_payload = 10000
mass_propellant = 300000
mass_structural = 300000

def payload_ratio():
    return (mass_payload / (mass_propellant + mass_structural + mass_payload))

def structural_ratio():
    return(mass_structural / (mass_structural + mass_propellant))

 def mf_over_mi():
    return(structural_ratio() + payload_ratio() * (1 - structural_ratio()))

