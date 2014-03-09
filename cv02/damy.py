
import os
import math

CESTA_K_MINISAT = "minisat"





# Pomocna funkcia na zapis implikacie do suboru
def write(subor, a, b):
    subor.write( "{0:d} {1:d} 0\n".format(a, b) )

def q(i,j):
    return N*i + j +1
    
# Funkcia zapisujuca problem do vstupneho suboru SAT solvera v spravnom formate
def zapis_problem(subor,p):
    print(p)
    riadok = ""
    for x in range(int(p)):
        for y in range(int(p)):
            riadok += str(q(x,y)) + " "
        riadok += "0\n"
        subor.write(riadok)
        riadok = ""
        

    for x in range(int(p)):
        for y in range(int(p)):
            for z in range(int(p)):
                if (y != z):
                    write(subor,-q(x,y),-q(x,z))

    for x in range(int(p)):
        for y in range(int(p)):
            for z in range(int(p)):
                if (y != z):
                    write(subor,-q(y,x),-q(z,x))

    for x in range(int(p)):
        for y in range(int(p)):
            for z in range(int(p) - y):
                if (q(x+z,y+z) <= N*N):
                    if(q(x,y) != q(x+z,y+z)):
                        write(subor,-q(x,y),-q(x+z,y+z))
                    
    i = 0
    for x in range(int(p)):
        for y in reversed(range(1,int(p))):
            i = 0
            for z in range(int(p)):
                if (x + i < N) and ( y- z >= 0):
                    if q(x,y) != q(x +z,y-z):
                        write(subor,-q(x,y),-q(x+y,y-z))
                    
    

# Funkcia vypisujuca riesenie najdene SAT solverom z jeho vystupneho suboru
def vypis_riesenie(ries):
    
    vs = ries.split()
    cisla = [int(cislo) for cislo in vs]
    riadok = 0

    for cislo in cisla:
        if cislo > 0:
            riadok =  math.trunc((cislo - 1) / N)      
            stlpec = (cislo-1)  % N          
            print ("{0} {1}".format(riadok, stlpec) )

def main():
    global N
    N = int(input())
    
    try:
        with open("vstup.txt", "w") as o:
            # zapiseme nas problem
            zapis_problem(o,N)
    except IOError as e:
        print("Chyba pri vytvarani vstupneho suboru ({0}): {1}".format(
                e.errno, e.strerror))
        return 1
    
    # spustime SAT solver
    os.system("{} vstup.txt vystup.txt".format(CESTA_K_MINISAT));

    # nacitame jeho vystup
    try:
        with open("vystup.txt", "r") as i:
            # prvy riadok je SAT alebo UNSAT
            sat = i.readline()
            if sat == "SAT\n":
                print("Riesenie:")
                # druhy riadok je riesenie
                ries = i.readline()
                vypis_riesenie(ries)
            else:
                print("Ziadne riesenie")
    except IOError as e:
        print("Chyba pri nacitavani vystupneho suboru ({0}): {1}".format(
                e.errno, e.strerror))
        return 1
    
    return 0

if __name__ == "__main__":
    main()
