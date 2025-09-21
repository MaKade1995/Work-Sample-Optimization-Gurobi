import numpy as np
import gurobipy as gp
from gurobipy import GRB


'Wenn das Ergebnis zu Car Rental 1 ausgegeben werden soll, dann bitte CarRental gleich 1 setzten'

'Wenn das Ergebnis zu Car Rental 2 ausgegeben werden soll, dann bitte CarRental gleich 2 setzten'


CarRental = 2


'_____________________________Daten___________________________________________'

Niederlassungen     = ['Glasgow', 'Manchester', 'Birmingham', 'Plymouth']

ORW                 = ['Glasgow', 'Plymouth'] #Niederlassungen ohne Reperaturwerkstatt

RW                  = ['Manchester', 'Birmingham'] #Niederlassungen mit Reperaturwerkstatt

Tagname             = ['Montag', 'Dienstag', 'Mittwoch', 'Donerstag', 'Freitag', 'Samstag']
'Montag(0) bis Samstag(5)'
Arbeitstage         = [0, 1, 2, 3, 4, 5] 
'Montag(0) bis Freitag(4)'
Werktage            = [0, 1, 2, 3, 4]

Mietdauer           = [1, 2, 3]

MietdauerAmSamstag  = [2, 3] #ohne Rabatt

'Daten (Wiliams 1978)'
Mietverteilung  = [0, 0.55, 0.20, 0.25]

Ausleihkosten   = [0, 20, 25, 30]

PreisGleicheNL  = [0, 50, 70, 120]

PreisAndereNL   = [0, 70, 100, 150]


Niederlassungen, Reparaturkapazitaet = gp.multidict(
    {('Glasgow'): 0,('Manchester'): 12,('Birmingham'): 20, ('Plymouth'): 0 })

'Table 12.20 (Wiliams 1978)'
NiederlassungenTage, Nachfrage = gp.multidict({
    ('Glasgow',     0): 100,
    ('Glasgow',     1): 150,
    ('Glasgow',     2): 135,
    ('Glasgow',     3): 83,
    ('Glasgow',     4): 120,
    ('Glasgow',     5): 230,
    ('Manchester',  0): 250,
    ('Manchester',  1): 143,
    ('Manchester',  2): 80,
    ('Manchester',  3): 225,
    ('Manchester',  4): 210,
    ('Manchester',  5): 98,
    ('Birmingham',  0): 95,
    ('Birmingham',  1): 195,
    ('Birmingham',  2): 242,
    ('Birmingham',  3): 111,
    ('Birmingham',  4): 70,
    ('Birmingham',  5): 124,
    ('Plymouth',    0): 160,
    ('Plymouth',    1): 99,
    ('Plymouth',    2): 55,
    ('Plymouth',    3): 96,
    ('Plymouth',    4): 115,
    ('Plymouth',    5): 80})


'Table 12.21 (Wiliams 1978)'
RueckgabeNL, Rueckgabeverteilung = gp.multidict({
    ('Glasgow',     'Glasgow'):         0.6,
    ('Glasgow',     'Manchester'):      0.2,
    ('Glasgow',     'Birmingham'):      0.1,
    ('Glasgow',     'Plymouth'):        0.1,
    ('Manchester',  'Glasgow'):         0.15,
    ('Manchester',  'Manchester'):      0.55,
    ('Manchester',  'Birmingham'):      0.25,
    ('Manchester',  'Plymouth'):        0.05,
    ('Birmingham',  'Glasgow'):         0.15,
    ('Birmingham',  'Manchester'):      0.2,
    ('Birmingham',  'Birmingham'):      0.54,
    ('Birmingham',  'Plymouth'):        0.11,
    ('Plymouth',    'Glasgow'):         0.08,
    ('Plymouth',    'Manchester'):      0.12,
    ('Plymouth',    'Birmingham'):      0.27,
    ('Plymouth',    'Plymouth'):        0.53})


'Table 12.22 (Wiliams 1978)'
TransferNL, Transferkosten = gp.multidict({
    ('Glasgow',     'Glasgow'):     0,
    ('Glasgow',     'Manchester'):  20,
    ('Glasgow',     'Birmingham'):  30,
    ('Glasgow',     'Plymouth'):    50,
    ('Manchester',  'Glasgow'):     20,
    ('Manchester',  'Manchester'):  0,
    ('Manchester',  'Birmingham'):  15,
    ('Manchester',  'Plymouth'):    35,
    ('Birmingham',  'Glasgow'):     30,
    ('Birmingham',  'Manchester'):  15,
    ('Birmingham',  'Birmingham'):  0,
    ('Birmingham',  'Plymouth'):    25,
    ('Plymouth',    'Glasgow'):     50,
    ('Plymouth',    'Manchester'):  35,
    ('Plymouth',    'Birmingham'):  25,
    ('Plymouth',    'Plymouth'):    0})


'Car Rental 2'

'(Wiliams 1978)'
KostenRepErwB = 18000

KostenRepErwBzusaetzlich = 8000

KostenRepErwM = 20000

KostenRepErwMzusaetzlich = 5000

KostenRepErwP = 19000


"__________________________Tuple_____________________________________________________________________"



Transfer = []

for NL in Niederlassungen:
    for NLi in Niederlassungen:
        if (NL != NLi):
            h = NL, NLi
            Transfer.append(h)


TransferTage = []

for NL, NLi in Transfer:
    for t in Arbeitstage:
        h = NL, NLi, t
        TransferTage.append(h)


TransferMietdauer = []

for NL, NLi in Transfer:
        for M in Mietdauer:
            h = NL, NLi, M
            TransferMietdauer.append(h)
            

TransferTageMietdauer = []

for NL, NLi in Transfer:
    for t in Werktage:
        for M in Mietdauer:
            h = NL, NLi, t, M
            TransferTageMietdauer.append(h)
            
            
TransferMietdauerAmSamstag = []

for NL, NLi in Transfer:
    for M in MietdauerAmSamstag:
        h = NL, NLi, M
        TransferMietdauerAmSamstag.append(h)


NiederlassungenMietdauer = []

for NL in Niederlassungen:
    for M in Mietdauer:
        h = NL, M
        NiederlassungenMietdauer.append(h)


NiederlassungenTageMietdauer = []

for NL in Niederlassungen:
    for t in Werktage:
        for M in Mietdauer:
            h = NL, t, M
            NiederlassungenTageMietdauer.append(h)


NiederlassungenMietdauerAmSamstag = []

for NL in Niederlassungen:
    for M in MietdauerAmSamstag:
        h = NL, M
        NiederlassungenMietdauerAmSamstag.append(h)


"__________________________________Definition der Variablen_____________________________________"



'Car Rental 1'

model = gp.Model('CarRental')

'Anzahl der Autos'
n = model.addVar(0)

'unbeschädigte Autos'
nu = model.addVars(NiederlassungenTage)

'beschädigten Autos'
nb = model.addVars(NiederlassungenTage)

'ausgeliehene Autos'
tr = model.addVars(NiederlassungenTage)

'Endbestand unbeschädigter Autos'
eu = model.addVars(NiederlassungenTage)

'Endbestand an beschädigten Autos'
eb = model.addVars(NiederlassungenTage)

'in ein anderes Depot transportierte unbeschädigte Autos'
tu = model.addVars(TransferTage)

'in ein anderes Depot transportierte beschädigte Autos'
tb = model.addVars(TransferTage)

'reparierte Autos'
rp = model.addVars(NiederlassungenTage)


'Car Rental 2'

'Erweiterung in Birmingham um 5'
ErB = model.addVar(vtype=GRB.BINARY)

'Erweiterung in Birmingham um zusätzliche 5'
ErBz = model.addVar(vtype=GRB.BINARY)

'Erweiterung in Manchester um 5'
ErM = model.addVar(vtype=GRB.BINARY)

'Erweiterung in Manchester um zusätzliche 5'
ErMz = model.addVar(vtype=GRB.BINARY)

'Errichtung einer Reparaturkapazität in Plymouth mit 5 Einheiten'
ErP = model.addVar(vtype=GRB.BINARY)


"______________________________________________NEBENBEDINGUNGEN_________________________________"


'Anzahl der unbeschädigte Autos in Niederlassungen'
model.addConstrs(sum(0.9 * Rueckgabeverteilung[NLi, NL] * Mietverteilung[M] * tr[NLi, (t - M) % 6] for NLi, M in NiederlassungenMietdauer)
     + sum(tu.select('*', NL, (t - 1) % 6)) + rp[NL, (t - 1) % 6]
     + eu[NL, (t - 1) % 6] == nu[NL, t] for NL in Niederlassungen for t in Arbeitstage)


'Anzahl der beschädigten Autos in eine Niederlassung'
model.addConstrs(sum(0.1 * Rueckgabeverteilung[NLi, NL] * Mietverteilung[M] * tr[NLi, (t - M) % 6] for NLi, M in NiederlassungenMietdauer)
     + sum(tb[NLi, NL, (t - 1) % 6] for NLi, NLNL in Transfer if (NLNL == NL))
     + eb[NL, (t - 1) % 6] == nb[NL, t] for NL in Niederlassungen for t in Arbeitstage)       


'Anzahl der unbeschädigten Autos aus einer Niederlassung mit Reparaturwerkstatt' 
model.addConstrs(tr[NL, t] + sum(tu.select(NL, '*', t)) + eu[NL, t] == nu[NL, t] for NL in RW for t in Arbeitstage)


'unbeschädigte Autos aus einer Niederlassung ohne Werkstatt'
model.addConstrs(tr[NL, t] + sum(tu.select(NL, '*', t)) + eu[NL, t] == nu[(NL, t)] for NL in ORW for t in Arbeitstage)


'Anzahl der beschädigten Autos aus einer Niederlassung mit Reparaturwerkstatt'
model.addConstrs(rp[NL, t] + sum(tb[NL, NLi, t] for NLi in ORW) + eb[NL, t] == nb[NL, t] for NL in RW for t in Arbeitstage)


'Anzahl der beschädigten Autos aus einer Niederlassung ohne Reparaturwerkstatt'
model.addConstrs(sum(tb[NL, NLi, t] for NLi in RW) + eb[NL, t] == nb[NL, t] for NL in ORW for t in Arbeitstage)


'Anzahl der Fahrzeuge übersteigt nicht die Nachfrage'
model.addConstrs(tr[NL,t]<=Nachfrage[NL,t] for NL, t in NiederlassungenTage)


'Die Anzahl der reparierten Autos übersteigt nicht die Reparaturkapazität'
if CarRental == 1 :
    model.addConstrs(rp[NL, t] <= Reparaturkapazitaet[NL] for NL, t in NiederlassungenTage)     


'Gesamtanzahl an Autos'
model.addConstr(sum(0.25 * tr[NL, 0] + 0.45 * tr[NL, 1] + nu[NL, 2] + nb[NL, 2] for NL in Niederlassungen) == n)



'Car Rental 2'

if CarRental == 2 :
    'Neue maximale Reparaturkapazität in Bermingham'
    model.addConstrs(rp['Birmingham',t] <= Reparaturkapazitaet['Birmingham'] + 5*ErB + 5*ErBz for t in Arbeitstage )
    
    'Neue maximale Reparaturkapazität in Manchester'
    model.addConstrs(rp['Manchester',t] <= Reparaturkapazitaet['Manchester'] + 5*ErM + 5*ErMz for t in Arbeitstage )
    
    'Neue maximale Reparaturkapazität in Plymouth'
    model.addConstrs(rp['Plymouth',t] <= Reparaturkapazitaet['Plymouth'] + 5*ErP for t in Arbeitstage )
    
    'Maximale Reparaturkapazität in Glasgow'
    model.addConstrs(rp['Glasgow', t] <= Reparaturkapazitaet['Glasgow'] for t in Arbeitstage)


    'Option2 kann nur gewählt werden, wenn Option1 bereits gewählt wurde'
    model.addConstr( ErB >= ErBz )
    
    'Option4 kann nur gewählt werden, wenn Option3 bereits gewählt wurde'
    model.addConstr( ErM >= ErMz )


    'Es können nicht mehr als 3 Optionen gewählt werden'
    model.addConstr(ErB + ErBz + ErM + ErMz + ErP <= 3)



"_________________________________Zielfunktion__________________________________________________"



if CarRental == 1:
 model.setObjective(( 
    
          sum(Rueckgabeverteilung[NL, NL]    *  Mietverteilung[M] * (PreisGleicheNL[M]   -  Ausleihkosten[M] + 10) * tr[NL, t] for NL, t, M in NiederlassungenTageMietdauer)
        + sum(Rueckgabeverteilung[NL, NLi]   *  Mietverteilung[M] * (PreisAndereNL[M]    -  Ausleihkosten[M] + 10) * tr[NL, t] for NL, NLi, t, M in TransferTageMietdauer)
        
        + sum(Rueckgabeverteilung[NL, NL]    *  0.55 *               (30                 -  20               + 10) * tr[NL, 5] for NL in Niederlassungen)
        + sum(Rueckgabeverteilung[NL, NLi]   *  0.55 *               (50                 -  20               + 10) * tr[NL, 5] for NL, NLi in Transfer)
        
        + sum(Rueckgabeverteilung[NL, NL]    *  Mietverteilung[M] * (PreisGleicheNL[M]   -  Ausleihkosten[M] + 10) * tr[NL, 5] for NL, M in NiederlassungenMietdauerAmSamstag)
        + sum(Rueckgabeverteilung[NL, NLi]   *  Mietverteilung[M] * (PreisAndereNL[M]    -  Ausleihkosten[M] + 10) * tr[NL, 5] for NL, NLi, M in TransferMietdauerAmSamstag)
        
        - sum(Transferkosten[NL, NLi] * tu[NL, NLi, t] for NL, NLi, t in TransferTage)
        - sum(Transferkosten[NL, NLi] * tb[NL, NLi, t] for NL, NLi, t in TransferTage) 
        
        - 15 * n), 
    
          GRB.MAXIMIZE)



if CarRental == 2:
    model.setObjective(( 
    
          sum(Rueckgabeverteilung[NL, NL]    *  Mietverteilung[M] * (PreisGleicheNL[M]   -  Ausleihkosten[M] + 10) * tr[NL, t] for NL, t, M in NiederlassungenTageMietdauer)
        + sum(Rueckgabeverteilung[NL, NLi]   *  Mietverteilung[M] * (PreisAndereNL[M]    -  Ausleihkosten[M] + 10) * tr[NL, t] for NL, NLi, t, M in TransferTageMietdauer)
        
        + sum(Rueckgabeverteilung[NL, NL]    *  0.55 *               (30                 -  20               + 10) * tr[NL, 5] for NL in Niederlassungen)
        + sum(Rueckgabeverteilung[NL, NLi]   *  0.55 *               (50                 -  20               + 10) * tr[NL, 5] for NL, NLi in Transfer)
        
        + sum(Rueckgabeverteilung[NL, NL]    *  Mietverteilung[M] * (PreisGleicheNL[M]   -  Ausleihkosten[M] + 10) * tr[NL, 5] for NL, M in NiederlassungenMietdauerAmSamstag)
        + sum(Rueckgabeverteilung[NL, NLi]   *  Mietverteilung[M] * (PreisAndereNL[M]    -  Ausleihkosten[M] + 10) * tr[NL, 5] for NL, NLi, M in TransferMietdauerAmSamstag)
        
        - sum(Transferkosten[NL, NLi] * tu[NL, NLi, t] for NL, NLi, t in TransferTage)
        - sum(Transferkosten[NL, NLi] * tb[NL, NLi, t] for NL, NLi, t in TransferTage) 
        
        -(KostenRepErwB*ErB + KostenRepErwBzusaetzlich*ErBz + KostenRepErwM*ErM + KostenRepErwMzusaetzlich*ErMz + KostenRepErwP*ErP)
        
        - 15 * n), 
    
          GRB.MAXIMIZE)


model.write('CarRental.lp')

model.optimize()


"________________________________________Ausgabe________________________________________________"

print(" ")
print(" ")
print("__________________________________________________________________________")
print(" ")
if CarRental == 1:
    print("Wie viele Fahrzeuge sollte die Autovermietung besitzen und an welchen Niederlassungen sind diese optimal zu platzieren?")

    print(" ")
    print(" ")
    
    print("Die zu erwartende Anzahl an unbeschädigten Autos, welche aus jeder Niederlassung und Tag ausgeliehen werden: ")
    print(" ")


    x=-1
    Ausleihe = np.zeros(shape=(6,4))
    
    
    for NL in Niederlassungen:
        x=x+1
        for t in Arbeitstage:
            count = 0
            for NLi in Niederlassungen:
                for r in Mietdauer:
                    count += 0.9 * Rueckgabeverteilung[NL, NLi] * Mietverteilung[M] * tr[NL, t].x
            Ausleihe[t, x] = round(count)
    
    print(Ausleihe)

    print(" ")
    
    print("Die zu erwartende Anzahl von beschädigten Autos in den Niederlassungen am Morgen von jedem Tag: ")
    
    print(" ")
    x=-1
    Ausleihe = np.zeros(shape=(6,4))
    
    
    for NL in Niederlassungen:
        x=x+1
        for t in Arbeitstage:
            count=nu[NL, t].x
            Ausleihe[t, x] = round(count)
    
    print(Ausleihe)

    print(" ")
    
    print("(entlang der spalten: 1. Glasgow, 2. Manchester, 3. Birmingham und 4. Plymouth )")
    
    print("(entlang der Zeilen: 1. Montag, 2. Dienstag, 3. Mittwoch, 4. Donnerstag, 5. Freitag und 6. Samstag )")

    print("--------------------------------------------------------------------------")
print(f"Die optimale Anzahl an Autos im Besitz lautet: {round(n.x)}.")
print(" ")
print(f"Der höchste Gewinn ist: {'{:,.2f}£'.format(round(model.objVal, 2))}.")


if CarRental == 1:
     print("__________________________________________________________________________")

if CarRental == 2:
    print("--------------------------------------------------------------------------")

    print("Car Rental 2")
    if ErB.x+ErBz.x == 1:
        print("-Erweiterungsmöglichkeiten 1:")
        print("Den höchsten Gewinn bringt eine Erweiterung der Reparaturkapazitäten in Birmingham um 5 Einheiten")
    if ErB.x+ErBz.x == 2:
        print("-Erweiterungsmöglichkeiten 1 und 2:")
        print("Den höchsten Gewinn bringt eine zweifache Erweiterung der Reparaturkapazitäten in Birmingham um insgesamt 10 Einheiten")

if CarRental == 2:
    if ErM.x+ErMz.x == 1:
        print("-Erweiterungsmöglichkeiten 3:")
        print("Den höchsten Gewinn bringt eine Erweiterung der Reparaturkapazitäten in Manchetser um 5 Einheiten")
    if ErM.x+ErMz.x == 2:
        print("-Erweiterungsmöglichkeiten 3 und 4:")
        print("Den höchsten Gewinn bringt eine zweifache Erweiterung der Reparaturkapazitäten in Manchester um insgesamt 10 Einheiten")

if CarRental == 2:
    if ErP.x == 1:
        print("-Erweiterungsmöglichkeiten 5:")
        print("Den höchsten Gewinn bringt eine Errichtung einer Werkstatt in Plymouth mit 5 Kapazitätseinheiten")
        
if CarRental == 2:
    print("__________________________________________________________________________")
    
    