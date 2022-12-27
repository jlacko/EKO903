"""
příklad z https://is.muni.cz/www/jkrejci/Linear_Programming_orig.pdf
řešení technikou Google OR tools / v PuLP analogické řešení přes PuLP
"""

# načíst prostředí
from ortools.linear_solver import pywraplp

# deklarovat funkci na řešení problému
def OzarkFarms():
    
    # deklarovat solver; když chyba tak konec zvonec
    solver = pywraplp.Solver.CreateSolver('SCIP') # pozor, ne GLOP!!!
    if not solver:
        return

    print('problém deklarován; jedeme:')
    # deklarovat proměnné v intervalu nula až plus nekonečno
    corn = solver.IntVar(0, solver.infinity(), 'corn')
    soybean = solver.IntVar(0, solver.infinity(), 'soybean')

    print('počet proměnných v solveru =', solver.NumVariables())

    # denní krmná dávka alespoň...
    solver.Add(corn + soybean >= 800)

    # podíl bílkovin - bez převádění pravé strany na levo
    solver.Add(.09 * corn +  .6 * soybean >= .3 * (corn + soybean))
    
    # podíl vlákniny - bez převádění pravé strany na levo
    solver.Add(.02 * corn + .06 * soybean <= .05 * (corn + soybean))


    print('počet omezení v solveru =', solver.NumConstraints())

    # deklarovat funkci k minimalizaci
    solver.Minimize(.3 * corn + .9 * soybean)

    # Solve the system.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('\nŘešení celočíselného problému Ozark Farm:')
        print('- cena denní krmné dávky =', solver.Objective().Value())
        print('- spotřeba liber kukuřice =', corn.solution_value())
        print('- spotřeba liber mleté sójy =', soybean.solution_value())
    else:
        print('Ještě jednou a pořádně!.')

    print('\nPoučení z krizového vývoje:')
    print('Řešení nalezeno za %f milisekund' % solver.wall_time())
    print('Řešení nalezeno za %d iteratací' % solver.iterations())


OzarkFarms()
