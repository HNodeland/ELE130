#!/usr/bin/env pybricks-micropython
# coding=utf-8

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# P01_NumeriskIntegrasjon
#
# Hensikten med programmet er å ................
#
# Følgende sensorer brukes:
# - Lyssensor
# - ...
# - ...
#
# Følgende motorer brukes:
# - motor A
# - ...
#
# ---------------------------------------------------------------------
import math
try:
    from pybricks.hubs import EV3Brick
    from pybricks.parameters import Port
    from pybricks.ev3devices import *
    from styrestikke.EV3AndJoystick import *
    from time import perf_counter, sleep
    import styrestikke.config
except Exception as e:
    pass  # for å kunne eksportere funksjoner
import struct
import socket
import json
import _thread
import sys

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#            1) EXPERIMENT SETUP AND FILENAME
#
# Skal prosjektet gjennomføres med eller uten USB-ledning?
wired = True

# --> Filnavn for lagring av MÅLINGER som gjøres online
filenameMeas = "Meas_P01_NumeriskIntegrasjon_01.txt"

# --> Filnavn for lagring av BEREGNEDE VARIABLE som gjøres online
#     Typisk navn:  "CalcOnline_P0X_BeskrivendeTekst_Y.txt"
#     Dersom du ikke vil lagre BEREGNEDE VARIABLE, la det stå 
#     filenameCalcOnline = ".txt"
filenameCalcOnline = "CalcOnline_P01_NumeriskIntegrasjon_01.txt"
# --------------------------------------------------------------------


def main():
    try:
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #     2) EQUIPMENT. INITIALIZE MOTORS AND SENSORS
        # 
        # Initialiser robot, sensorer, motorer og styrestikke.
        #
        # Spesifiser hvilke sensorer og motorer som brukes.
        # Du må også spesifisere hvilken port de er tilkoplet.
        #
        # For ryddig og oversiktlig kode er det lurt å slette
        # koden for de sensorene og motorene som ikke brukes.

        robot = Initialize(wired,filenameMeas,filenameCalcOnline)

        # oppdater portnummer
        myColorSensor = ColorSensor(Port.S1)
       

        # Sjekker at joystick er tilkoplet EV3 
        if robot["joystick"]["in_file"] is not None:
            _thread.start_new_thread(getJoystickValues, [robot])
        else:
            print(" --> Joystick er ikke koplet til")
        sleep(0)

        print("2) EQUIPMENT. INITIALIZE MOTORS AND SENSORS.")
        # ------------------------------------------------------------


        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #               3) MEASUREMENTimeStep. INITIALIZE LISTimeStep
        # 
        # Denne seksjonen inneholder alle tilgjengelige målinger
        # fra EV3 og styrestikke, i tillegg til tid. Du skal velge 
        # ut hvilke målinger du vil benytte i prosjektet ved å slette 
        # koden til de målingene du ikke skal bruke. Legg merke til 
        # at listene i utgangspunktet er tomme.
        # 
        # Listene med målinger fylles opp i seksjon 
        #  --> 5) GET TIME AND MEASUREMENT
        # og lagres til .txt-filen i seksjon 
        #  --> 6) STORE MEASUREMENTimeStep TO FILE

        Tid = []                # registring av tidspunkt for målinger
        Lys = []                # måling av reflektert lys fra ColorSensor
        
    

        print("3) MEASUREMENTimeStep. LISTimeStep INITIALIZED.")
        # ------------------------------------------------------------



        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #         4) optional: OWN VARIABLES. INITIALIZE LISTimeStep
        #
        # Denne seksjonen definerer lister med EGNE VARIABLE som 
        # skal beregnes. Tenk nøye gjennom hvilke lister som skal 
        # ha en initialverdi.
        # 
        # Bruken av denne seksjonen avhenger av hvordan prosjektet 
        # gjennomføres. Dersom det er et såkalt "online"-prosjekt 
        # som ikke kan gjennomføre offline, så MÅ denne seksjonen
        # i hovedfilen benyttes. Dette fordi du er nødt til å 
        # beregne bl.a. motorpådraget (som er en EGEN VARIABEL). 
        # 
        # Dersom prosjektet er et "offline"-prosjekt hvor du kun 
        # ønsker å lagre målinger, så trenger du ikke bruke denne
        # seksjonen. Dette fordi du alternativt kan spesifisere 
        # EGEN VARIABLE offline i seksjonen 
        #  --> C) offline: OWN VARIABLES. INITIALIZE LISTimeStep
        # i plottefilen. 
        TimeStep = []                     #Tidsskritt
        FunctionValue = []                   #Lysmåling minus den første lysmålingen
        IntValueOld = []

        sinGraf = []
        sinIntGraf = []
        sumTimeStep = []

        print("4) OWN VARIABLES. LISTimeStep INITIALIZED.")
        # ------------------------------------------------------------

        # indeks som øker for hver runde
        k = 0

        # Går inn i løkke
        while True:

            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #                  5) GET TIME AND MEASUREMENT
            #
            # I denne seksjonen registres måletidspunkt og målinger 
            # fra sensorer, motorer og styrestikke, og disse legges 
            # inn i listene definert i seksjon
            #  -->  3) MEASUREMENTimeStep. INITIALIZE LISTimeStep

            if k==0:        
                # Definer starttidspunkt for eksperimentet
                starttidspunkt = perf_counter()
                Tid.append(0) 
            else: 
                # For hver ny runde i while-løkka, registrerer 
                # måletidspunkt
                Tid.append(perf_counter() - starttidspunkt)

            Lys.append(myColorSensor.reflection())
                    
            # --------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #            6) STORE MEASUREMENTimeStep TO FILE
            #
            # I denne seksjonen lagres MÅLINGENE til .txt-filen. 
            #
            # For å holde orden i koden bør du benytte samme 
            # struktur/rekkefølge i seksjonen
            #   --> 3) MEASUREMENTimeStep. INITIALIZE LISTimeStep
            #   --> 5) GET TIME AND MEASUREMENT 
            #   --> 6) STORE MEASUREMENTimeStep TO FILE 
            # 
            # I plottefilen må du passe på at seksjonene
            #  --> B) offline: MEASUREMENTimeStep. INTITALIZE LISTimeStep ACCORDING to 6)
            #  --> E) offline: UNPACK MEASUREMENTimeStep FROM FILE ACCORDING TO 6)
            # har lik struktur som her i seksjon 6)
            
            # Legger først inn 4 linjer som header i filen med målinger.            
            # Husk at siste element i strengen må være '\n'
            if k == 0:
                MeasurementToFileHeader = "Tall viser til kolonnenummer:\n"
                MeasurementToFileHeader += "0=Tid, 1=Lys\n"
                robot["measuremenTimeStep"].write(MeasurementToFileHeader)

            MeasurementToFile = ""
            MeasurementToFile += str(Tid[-1]) + ","
            MeasurementToFile += str(Lys[-1]) + "\n"
           

            # Skriv MeasurementToFile til .txt-filen navngitt øverst
            robot["measuremenTimeStep"].write(MeasurementToFile)
            #--------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #    7) optional: PERFORM CALCULATIONS AND SET MOTOR POWER
            # 
            # På samme måte som i seksjon
            #  -->  4) optional: OWN VARIABLES. INITIALIZE LISTimeStep
            # så er bruken av seksjon 7) avhengig av hvordan 
            # prosjektet gjennomføres. Dersom seksjon 4) ikke benyttes 
            # så kan heller ikke seksjon 7) benyttes. Du må i så 
            # fall kommentere bort kallet til MathCalculations()
            # nedenfor. Du må også kommentere bort motorpådragene. 
            
            MathCalculations(Tid, Lys, TimeStep, FunctionValue, sinGraf, sinIntGraf, sumTimeStep)

            EulerForward(IntValueOld, FunctionValue, TimeStep)

           

            # Hvis motor(er) brukes i prosjektet så sendes til slutt
            # beregnet pådrag til motor(ene).
            
            # --------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #        8) optional: STORE CALCULATIONS FROM 6) TO FILE
            #
            # På samme måte som i seksjonene
            #  --> 4) optional: OWN VARIABLES. INITIALIZE LISTimeStep
            #  --> 7) optional: PERFORM CALCULATIONS AND SET MOTOR POWER
            # så er bruken av seksjon 8) avhengig av hvordan prosjektet 
            # gjennomføres. Dersom seksjonene 4) og 7) ikke benyttes
            # så kan heller ikke seksjon 8) benyttes. La i så fall
            # filnavnet for lagring av beregnede variable være tomt.
            #
            # Hvis du velger å bruke seksjonene 4), 7) og 8),
            # så må du ikke nødvendigvis lagre ALLE egne variable.

            # Vi legger først inn 3 linjer som header i filen med beregnede 
            # variable. Du kan legge inn flere linjer om du vil.
            if len(filenameCalcOnline)>4:
                if k == 0:
                    CalculationsToFileHeader = "Tallformatet viser til kolonnenummer:\n"
                    CalculationsToFileHeader += "0= \n"


                    robot["calculations"].write(CalculationsToFileHeader)
                CalculationsToFile = ""
             

                # Skriv CalcultedToFile til .txt-filen navngitt i seksjon 1)
                robot["calculations"].write(CalculationsToFile)
            # --------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #     9) wired only: SEND DATA TO F) FOR PLOTTING
            # 
            # Denne seksjonen kjører kun når det er ledning mellom 
            # EV3 og datamaskin ("wired"). Seksjonen sender over til 
            # plottefile utvalgte DATA bestående av både: 
            #   - MÅLINGER spesifisert i seksjon 3) og
            #   - EGNE VARIABLE spesifisert i seksjon 4).
            #  
            # For å holde orden i koden bør du beholde rekkefølgen
            # på de utvalgte listene med MÅLINGER og EGEN VARIABLE
            # slik de er definert i seksjonene 3) og 4). 
            # 
            # I plottefilen må du passe på at seksjonene
            #  --> D) online: DATA TO PLOT. INITIALIZE LISTimeStep ACCORDING TO 9)
            #  --> F) online: RECEIVE DATA TO PLOT ACCORDING TO 9) 
            # har lik struktur som her i seksjon 9)

            if wired:
                DataToOnlinePlot = {}

                # målinger
                DataToOnlinePlot["Tid"] = (Tid[-1])
                DataToOnlinePlot["Lys"] = (Lys[-1])
              
                

                # egne variable
                DataToOnlinePlot["TimeStep"] = (TimeStep[-1])
                DataToOnlinePlot["FunctionValue"] = (FunctionValue[-1])
                DataToOnlinePlot["IntValueOld"] = (IntValueOld[-1])

                # sender over data
                msg = json.dumps(DataToOnlinePlot)
                robot["connection"].send(bytes(msg, "utf-b") + b"?")
            # --------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #            10) STOP EXPERIMENT AND INCREASE k
            # 
            # Hvis du får socket timeouTimeStep, fjern kommentar foran sleep(1)
            # sleep(1)

            # Hvis skyteknappen trykkes inn så skal programmet avsluttes
            if config.joyMainSwitch:
                print("joyMainSwitch er satt til 1")
                break

            # Teller opp k
            k += 1
            #--------------------------------------------------------

    except Exception as e:
        sys.print_exception(e)
    finally:
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #                  11) CLOSE JOYSTICK AND EV3
        #
        # Spesifiser hvordan du vil at motoren(e) skal stoppe.
        # Det er 3 forskjellige måter å stoppe motorene på:
        # - stop() ruller videre og bremser ikke.
        # - brake() ruller videre, men bruker strømmen generert 
        #   av rotasjonen til å bremse.
        # - hold() bråstopper umiddelbart og holder posisjonen
        

        # Lukker forbindelsen til både styrestikke og EV3.
        CloseJoystickAndEV3(robot, wired)
        #--------------------------------------------------------





#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#               12) MATH CALCULATIONS
# Her gjøres alle beregninger basert på målinger og egendefinerte
# lister med variable. 
#
# Denne funksjonen kalles enten fra seksjonen
#  --> 7) optional: PERFORM CALCULATIONS AND SET MOTOR POWER
# ovenfor i online, eller fra
#  --> H) offline: PERFORM CALCULATIONS
# i offline fra plottefilen.
#
# Pass på at funksjonsbeskrivelsen og kallet til 
# funksjonen er identiske i 
#   - seksjonene 7) og 12) for online bruk
# eller i seksjonene
#   - seksjonene H) og 12) for offline bruk

def MathCalculations(Tid, Lys, TimeStep, FunctionValue, sinGraf, sinIntGraf, sumTimeStep):
    
    
    # Parametre
    sin_t = float(math.sin(sumTimeStep[-1]))
    cos_t = float(math.cos(sumTimeStep[-1]))
    # Initialverdibereging
    Nullflow = Lys[0]
    if len(Tid) == 1:
        
        TimeStep.append(0)
        sumTimeStep.append(sumTimeStep[-1]+TimeStep[-1])
        FunctionValue.append(0) 
        sinGraf.append(0)
        sinIntGraf.append(0)
    
    else:
        TimeStep.append(Tid[-1] - Tid[-2])
        sumTimeStep.append(sumTimeStep[-1] + TimeStep[-1])
        FunctionValue.append(Lys[-1] - Nullflow)
        sinGraf.append(sin_t)
        sinIntGraf.append(-cos_t+1)

        #sinIntGraf.append(12.4*-cos_t*71.5)

    
    # Matematiske beregninger 

        
    
    # Pådragsberegning

#---------------------------------------------------------------------

def EulerForward(IntValueOld, FunctionValue, TimeStep):
    if len(IntValueOld) == 1:
        IntValueOld.append(0)

    else:
        IntValueOld.append(IntValueOld[-1] + TimeStep[-1]*FunctionValue[-1])
        
        IntValueNew = IntValueOld[-1]



if __name__ == '__main__':
    main()
