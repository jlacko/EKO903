"""
příklad z https://is.muni.cz/www/jkrejci/Linear_Programming_orig.pdf
řešení technikou Google OR tools / v PuLP analogické řešení přes PuLP
"""

# načíst prostředí
from ortools.linear_solver import pywraplp

# deklarovat funkci na řešení problému
def OzarkFarms():
    
    # deklarovat solver; když chyba tak konec zvonec
    solver = pywraplp.Solver('Ozark Farms floating point problem',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    if not solver:
        return

    print('problém deklarován; jedeme:')
    # deklarovat proměnné v intervalu nula až plus nekonečno
    corn = solver.NumVar(0, solver.infinity(), name = 'kukuřice')
    soybean = solver.NumVar(0, solver.infinity(), name = 'soja')

    print('počet proměnných v solveru =', solver.NumVariables())

    # denní krmná dávka alespoň...
    solver.Add(corn + soybean >= 800, name = 'objem krmné dávky')

    # podíl bílkovin - bez převádění pravé strany na levo
    solver.Add(.09 * corn +  .6 * soybean >= .3 * (corn + soybean), name = 'podíl bílkovin')
    
    # podíl vlákniny - bez převádění pravé strany na levo
    solver.Add(.02 * corn + .06 * soybean <= .05 * (corn + soybean), name = 'podíl vlákniny')

    print('počet omezení v solveru =', solver.NumConstraints())

    # deklarovat funkci k minimalizaci
    solver.Minimize(.3 * corn + .9 * soybean)

    # Solve the system.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('\nŘešení floating point problému Ozark Farm:')
        print('- cena denní krmné dávky =', solver.Objective().Value())
        print('- spotřeba liber kukuřice =', corn.solution_value())
        print('- spotřeba liber mleté sójy =', soybean.solution_value())
        
        # uložit lp soubor 
        res = solver.ExportModelAsLpFormat(obfuscated = False)
        soubor = open("./OR/ozark-farm-floating.lp","w")
        soubor.writelines(res)
        soubor.close()
    else:
        print('Ještě jednou a pořádně!.')

    print('\nPoučení z krizového vývoje:')
    print('Řešení nalezeno za %f milisekund' % solver.wall_time())
    print('Řešení nalezeno za %d iteratací' % solver.iterations())

# funkci deklarovanou výše spustit
OzarkFarms()