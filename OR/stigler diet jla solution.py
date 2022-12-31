"""
Causa Stiglerova dieta - konstrukce přes externí CSV

"""

# načíst prostředí
import numpy as np
from pandas import read_csv
from ortools.linear_solver import pywraplp

def StiglerDiet():

  # načíst podkladová data jako pandas dataframe
  df = read_csv('./OR/stigler-diet.csv', delimiter=';', decimal=',')

  pocet_potravin = np.shape(df)[0]
  
  # podat zprávu o úspěšném načtení
  print('načteno %d řádků CSV' % pocet_potravin)
    
  # deklarovat solver; když chyba tak konec zvonec
  solver = pywraplp.Solver('Problém jídelníčku pana Stiglera',
                           pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
  if not solver:
    return

  print('problém deklarován; jedeme:')
  
  # deklarovat proměnné - definované potraviny jako kladné floating číslo s názvem komodity
  potraviny = [solver.NumVar(0.0, solver.infinity(), item) for item in df["Commodity"]]
  print('Počet proměnných =', solver.NumVariables())
  
  # deklarovat omezení - 9 minimálních dávek - zatím jako prázdnou množinu
  omezeni = []

  # kalorie mezi 3K a nekonečnem
  omezeni.append(solver.Constraint(3, solver.infinity(), 'denní příjem kalorií'))
  for i in range(0, pocet_potravin-1):
    omezeni[0].SetCoefficient(potraviny[i], df["Calories (kcal)"][i])

 # protein mezi 70 gramy a nekonečnem
  omezeni.append(solver.Constraint(70, solver.infinity(), 'denní příjem bílkovin'))
  for i in range(0, pocet_potravin-1):
      omezeni[1].SetCoefficient(potraviny[i], float(df["Protein (g)"][i]))

# vápník mezi 0.8 gramy a nekonečnem
  omezeni.append(solver.Constraint(0.8, solver.infinity(), 'denní příjem vápníku'))
  for i in range(0, pocet_potravin-1):
    omezeni[2].SetCoefficient(potraviny[i], df["Calcium (g)"][i])

  # železo mezi 12 miligramy a nekonečnem
  omezeni.append(solver.Constraint(12, solver.infinity(), 'denní příjem železa'))
  for i in range(0, pocet_potravin-1):
      omezeni[3].SetCoefficient(potraviny[i], float(df["Iron (mg)"][i]))

  # Vitamín A mezi 5 KIU a nekonečnem
  omezeni.append(solver.Constraint(5, solver.infinity(), 'denní příjem vitamínu A'))
  for i in range(0, pocet_potravin-1):
      omezeni[4].SetCoefficient(potraviny[i], df["Vitamin A (KIU)"][i])

  # Vitamín B1 mezi 1.8 mg a nekonečnem
  omezeni.append(solver.Constraint(1.8, solver.infinity(), 'denní příjem vitamínu B1'))
  for i in range(0, pocet_potravin-1):
      omezeni[5].SetCoefficient(potraviny[i], df["Thiamine (mg)"][i])

  # Vitamín B2 mezi 2.7 mg a nekonečnem
  omezeni.append(solver.Constraint(2.7, solver.infinity(), 'denní příjem vitamínu B2'))
  for i in range(0, pocet_potravin-1):
      omezeni[6].SetCoefficient(potraviny[i], float(df["Riboflavin (mg)"][i]))

  # Niacin mezi 18 mg a nekonečnem
  omezeni.append(solver.Constraint(18, solver.infinity(), 'denní příjem Niacinu'))
  for i in range(0, pocet_potravin-1):
      omezeni[7].SetCoefficient(potraviny[i], float(df["Niacin (mg)"][i]))

  # Vitamín C mezi 75 mg a nekonečnem
  omezeni.append(solver.Constraint(75, solver.infinity(), 'denní příjem vitamínu C'))
  for i in range(0, pocet_potravin-1):
      omezeni[8].SetCoefficient(potraviny[i], float(df["Ascorbic Acid (mg)"][i]))

  # deklarovat funkci k minimalizaci - součet jako objektivní fce
  objective = solver.Objective()
  for potravina in potraviny:
      objective.SetCoefficient(potravina, 1)

  objective.SetMinimization()
   

  # uložit lp soubor pro kontrolu správnosti zadání...
  res = solver.ExportModelAsLpFormat(False)
  soubor = open("./OR/stigler-diet-jla.lp","w")
  soubor.writelines(res)
  soubor.close()


  # vyřešit!
  status = solver.Solve()

  if status == pywraplp.Solver.OPTIMAL:
    print('\nŘešení floating point problému jídelníčku pana Stiglera:')
    for i, potravina in enumerate(potraviny):
      if potravina.solution_value() > 0.0:
          print('- denní dávka {} v ${:.6f}'.format(df["Commodity"][i], potravina.solution_value()))
    
    print('- celková cena denní krmné dávky = ${:.6f}'.format(solver.Objective().Value()))
    print('Tedy ročně = ${:.2f}'.format(365 * solver.Objective().Value()))
 
  else:
    print('Ještě jednou a pořádně!.')

  print('\nPoučení z krizového vývoje:')
  print('Řešení nalezeno za %f milisekund' % solver.wall_time())
  print('Řešení nalezeno za %d iteratací' % solver.iterations())
  
  # o nalezeném řešení podat zprávu...

StiglerDiet()
