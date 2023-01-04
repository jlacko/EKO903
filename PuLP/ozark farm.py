"""
příklad z https://is.muni.cz/www/jkrejci/Linear_Programming_orig.pdf
řešen technikou PuLP / v OR složce analogické řešení přes Google OR
"""

# načíst prostředí
from pulp import *

# tabulka surovin
suroviny = ["corn", "soybean"]

# omezující podmínky
cena = {
  "corn" : .30,
  "soybean" : .90
}

# pravá strana převedená na levou; zbyde nula
protein = {
  "corn" : (.09 - .3),
  "soybean" : (.60 -.3)
}

vlaknina = {
  "corn" : (.02 - .05),
  "soybean" : (.06 -.05)
}

# deklarace problému
prob = LpProblem("causa Ozark Farms", LpMinimize)

# deklarace proměnných
suroviny_prom = LpVariable.dicts("suroviny", suroviny, 0)

# funkce k minimalizaci
prob += (
    lpSum([cena[i] * suroviny_prom[i] for i in suroviny]),
    "cena denní krmné dávky",
)

# omezující podmínky
prob += lpSum([suroviny_prom[i] for i in suroviny]) >= 800, "denni_krmna_davka"

prob += lpSum([protein[i]  * suroviny_prom[i] for i in suroviny]) >= 0, "podil_proteinu"
              
prob += lpSum([vlaknina[i] * suroviny_prom[i] for i in suroviny]) <= 0, "podil_vlakniny"

# odlít definici stranou pro debug
prob.writeLP("./PuLP/ozark-farm.lp")

# vyřešit!
prob.solve()

# zavolat domů stav problému
print("Status:", LpStatus[prob.status])

# vypsat cílové hodnoty složek krmné směsi
for v in prob.variables():
    print(v.name, "=", v.varValue)

# vypsat dosaženou hodnotu minimalizované fce
print("Náklady krmné dávky = ", value(prob.objective))

