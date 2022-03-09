#!/usr/bin/env pybricks-micropython
# coding=utf-8

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# P0X_BeskrivendeTekst
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
filenameMeas = "Meas_P0X_BeskrivendeTekst_Y.txt"

# --> Filnavn for lagring av BEREGNEDE VARIABLE som gjøres online
#     Typisk navn:  "CalcOnline_P0X_BeskrivendeTekst_Y.txt"
#     Dersom du ikke vil lagre BEREGNEDE VARIABLE, la det stå 
#     filenameCalcOnline = ".txt"
filenameCalcOnline = "CalcOnline_P0X_BeskrivendeTekst_Y.txt"
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
        myColorSensor = ColorSensor(Port.SX)
        myTouchSensor = TouchSensor(Port.SX)
        myUltrasonicSensor = UltrasonicSensor(Port.SX)
        myGyroSensor = GyroSensor(Port.SX)

        motorA = Motor(Port.A)
        motorA.reset_angle(0)
        motorB = Motor(Port.B)
        motorB.reset_angle(0)
        motorC = Motor(Port.C)
        motorC.reset_angle(0)
        motorD = Motor(Port.D)
        motorD.reset_angle(0)

        # Sjekker at joystick er tilkoplet EV3 
        if robot["joystick"]["in_file"] is not None:
            _thread.start_new_thread(getJoystickValues, [robot])
        else:
            print(" --> Joystick er ikke koplet til")
        sleep(0)

        print("2) EQUIPMENT. INITIALIZE MOTORS AND SENSORS.")
        # ------------------------------------------------------------


        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #               3) MEASUREMENTS. INITIALIZE LISTS
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
        #  --> 6) STORE MEASUREMENTS TO FILE

        Tid = []                # registring av tidspunkt for målinger
        Lys = []                # måling av reflektert lys fra ColorSensor
        LysDirekte = []         # måling av lys direkte inn fra ColorSensor
        Bryter = []             # registrering av trykkbryter fra TouchSensor
        Avstand = []            # måling av avstand fra UltrasonicSensor
        GyroAngle = []          # måling av gyrovinkel fra GyroSensor
        GyroRate = []           # måling av gyrovinkelfart fra GyroSensor

        VinkelPosMotorA = []    # vinkelposisjon motor A
        HastighetMotorA = []    # hastighet motor A
        VinkelPosMotorB = []    # vinkelposisjon motor B 
        HastighetMotorB = []    # hastighet motor B
        VinkelPosMotorC = []    # vinkelposisjon motor C
        HastighetMotorC = []    # hastighet motor C
        VinkelPosMotorD = []    # vinkelposisjon motor D
        HastighetMotorD = []    # hastighet motor D

        joyForward = []         # måling av foroverbevegelse styrestikke
        joySide = []            # måling av sidebevegelse styrestikke
        joyTwist = []           # måling av vribevegelse styrestikke
        joyPotMeter = []        # måling av potensionmeter styrestikke
        joyPOVForward = []      # måling av foroverbevegelse toppledd
        joyPOVSide = []         # måling av sidebevegelse toppledd

        joy1 = []               # måling av knapp 1 (skyteknappen)
        joy2 = []               # måling av knapp 2 (ved tommel)
        joy3 = []               # måling av knapp 3 
        joy4 = []               # måling av knapp 4 
        joy5 = []               # måling av knapp 5 
        joy6 = []               # måling av knapp 6 
        joy7 = []               # måling av knapp 7 
        joy8 = []               # måling av knapp 8 
        joy9 = []               # måling av knapp 9 
        joy10 = []              # måling av knapp 10 
        joy11 = []              # måling av knapp 11 
        joy12 = []              # måling av knapp 12 

        print("3) MEASUREMENTS. LISTS INITIALIZED.")
        # ------------------------------------------------------------



        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #         4) optional: OWN VARIABLES. INITIALIZE LISTS
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
        #  --> C) offline: OWN VARIABLES. INITIALIZE LISTS
        # i plottefilen. 

        Ts = []             # tidsskritt
        PowerA = []         # berenging av motorpådrag A
        PowerB = []         # berenging av motorpådrag B
        PowerC = []         # berenging av motorpådrag C
        PowerD = []         # berenging av motorpådrag D

        print("4) OWN VARIABLES. LISTS INITIALIZED.")
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
            #  -->  3) MEASUREMENTS. INITIALIZE LISTS

            if k==0:        
                # Definer starttidspunkt for eksperimentet
                starttidspunkt = perf_counter()
                Tid.append(0) 
            else: 
                # For hver ny runde i while-løkka, registrerer 
                # måletidspunkt
                Tid.append(perf_counter() - starttidspunkt)

            Lys.append(myColorSensor.reflection())
            LysDirekte.append(myColorSensor.ambient())
            Bryter.append(myTouchSensor.pressed())
            Avstand.append(myUltrasonicSensor.distance())
            GyroAngle.append(myGyroSensor.angle())
            GyroRate.append(myGyroSensor.speed())

            VinkelPosMotorA.append(motorA.angle())
            HastighetMotorA.append(motorA.speed())
            VinkelPosMotorB.append(motorB.angle())
            HastighetMotorB.append(motorB.speed())
            VinkelPosMotorC.append(motorC.angle())
            HastighetMotorC.append(motorC.speed())
            VinkelPosMotorD.append(motorD.angle())
            HastighetMotorD.append(motorD.speed())

            joyForward.append(config.joyForwardInstance)
            joySide.append(config.joySideInstance)
            joyTwist.append(config.joyTwistInstance)
            joyPotMeter.append(config.joyPotMeterInstance)
            joyPOVForward.append(config.joyPOVForwardInstance)
            joyPOVSide.append(config.joyPOVSideInstance)

            joy1.append(config.joy1Instance)
            joy2.append(config.joy2Instance)
            joy3.append(config.joy3Instance)
            joy4.append(config.joy4Instance)
            joy5.append(config.joy5Instance)
            joy6.append(config.joy6Instance)
            joy7.append(config.joy7Instance)
            joy8.append(config.joy8Instance)
            joy9.append(config.joy9Instance)
            joy10.append(config.joy10Instance)
            joy11.append(config.joy11Instance)
            joy12.append(config.joy12Instance)
            # --------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #            6) STORE MEASUREMENTS TO FILE
            #
            # I denne seksjonen lagres MÅLINGENE til .txt-filen. 
            #
            # For å holde orden i koden bør du benytte samme 
            # struktur/rekkefølge i seksjonen
            #   --> 3) MEASUREMENTS. INITIALIZE LISTS
            #   --> 5) GET TIME AND MEASUREMENT 
            #   --> 6) STORE MEASUREMENTS TO FILE 
            # 
            # I plottefilen må du passe på at seksjonene
            #  --> B) offline: MEASUREMENTS. INTITALIZE LISTS ACCORDING to 6)
            #  --> E) offline: UNPACK MEASUREMENTS FROM FILE ACCORDING TO 6)
            # har lik struktur som her i seksjon 6)
            
            # Legger først inn 4 linjer som header i filen med målinger.            
            # Husk at siste element i strengen må være '\n'
            if k == 0:
                MeasurementToFileHeader = "Tall viser til kolonnenummer:\n"
                MeasurementToFileHeader += "0=Tid, 1=Lys, 2=, 3= \n"
                MeasurementToFileHeader += "4=, 5=, 6=, 7= \n"
                MeasurementToFileHeader += "8=, 9= \n"
                robot["measurements"].write(MeasurementToFileHeader)

            MeasurementToFile = ""
            MeasurementToFile += str(Tid[-1]) + ","
            MeasurementToFile += str(Lys[-1]) + ","
            MeasurementToFile += str(LysDirekte[-1]) + ","
            MeasurementToFile += str(Bryter[-1]) + ","
            MeasurementToFile += str(Avstand[-1]) + ","
            MeasurementToFile += str(GyroAngle[-1]) + ","
            MeasurementToFile += str(GyroRate[-1]) + ","

            MeasurementToFile += str(VinkelPosMotorA[-1]) + ","
            MeasurementToFile += str(HastighetMotorA[-1]) + ","
            MeasurementToFile += str(VinkelPosMotorB[-1]) + ","
            MeasurementToFile += str(HastighetMotorB[-1]) + ","
            MeasurementToFile += str(VinkelPosMotorC[-1]) + ","
            MeasurementToFile += str(HastighetMotorC[-1]) + ","
            MeasurementToFile += str(VinkelPosMotorD[-1]) + ","
            MeasurementToFile += str(HastighetMotorD[-1]) + ","

            MeasurementToFile += str(joyForward[-1]) + ","
            MeasurementToFile += str(joySide[-1]) + ","
            MeasurementToFile += str(joyTwist[-1]) + ","
            MeasurementToFile += str(joyPotMeter[-1]) + ","
            MeasurementToFile += str(joyPOVForward[-1]) + ","
            MeasurementToFile += str(joyPOVSide[-1]) + ","
            
            MeasurementToFile += str(joy1[-1]) + ","
            MeasurementToFile += str(joy2[-1]) + ","
            MeasurementToFile += str(joy3[-1]) + ","
            MeasurementToFile += str(joy4[-1]) + ","
            MeasurementToFile += str(joy5[-1]) + ","
            MeasurementToFile += str(joy6[-1]) + ","
            MeasurementToFile += str(joy7[-1]) + ","
            MeasurementToFile += str(joy8[-1]) + ","
            MeasurementToFile += str(joy9[-1]) + ","
            MeasurementToFile += str(joy10[-1]) + ","
            MeasurementToFile += str(joy11[-1]) + ","
            MeasurementToFile += str(joy12[-1]) + "\n"

            # Skriv MeasurementToFile til .txt-filen navngitt øverst
            robot["measurements"].write(MeasurementToFile)
            #--------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #    7) optional: PERFORM CALCULATIONS AND SET MOTOR POWER
            # 
            # På samme måte som i seksjon
            #  -->  4) optional: OWN VARIABLES. INITIALIZE LISTS
            # så er bruken av seksjon 7) avhengig av hvordan 
            # prosjektet gjennomføres. Dersom seksjon 4) ikke benyttes 
            # så kan heller ikke seksjon 7) benyttes. Du må i så 
            # fall kommentere bort kallet til MathCalculations()
            # nedenfor. Du må også kommentere bort motorpådragene. 
            
            MathCalculations(.......)

            # Hvis motor(er) brukes i prosjektet så sendes til slutt
            # beregnet pådrag til motor(ene).
            motorA.dc(PowerA[-1])
            motorB.dc(PowerB[-1])
            motorC.dc(PowerC[-1])
            motorD.dc(PowerD[-1])
            # --------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #        8) optional: STORE CALCULATIONS FROM 6) TO FILE
            #
            # På samme måte som i seksjonene
            #  --> 4) optional: OWN VARIABLES. INITIALIZE LISTS
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
                    CalculationsToFileHeader += "0=Ts, 1=PowerA, \n"
                    CalculationsToFileHeader += "2=PowerB, 3=PowerC, 4=PowerD \n"
                    robot["calculations"].write(CalculationsToFileHeader)
                CalculationsToFile = ""
                CalculationsToFile += str(Ts[-1]) + ","
                CalculationsToFile += str(PowerA[-1]) + ","
                CalculationsToFile += str(PowerB[-1]) + ","
                CalculationsToFile += str(PowerC[-1]) + ","
                CalculationsToFile += str(PowerD[-1]) + "\n"

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
            #  --> D) online: DATA TO PLOT. INITIALIZE LISTS ACCORDING TO 9)
            #  --> F) online: RECEIVE DATA TO PLOT ACCORDING TO 9) 
            # har lik struktur som her i seksjon 9)

            if wired:
                DataToOnlinePlot = {}

                # målinger
                DataToOnlinePlot["Tid"] = (Tid[-1])
                DataToOnlinePlot["Lys"] = (Lys[-1])
                DataToOnlinePlot["VinkelPosMotorA"] = (VinkelPosMotorA[-1])
                DataToOnlinePlot["joyForward"] = (joyForward[-1])

                # egne variable
                DataToOnlinePlot["Ts"] = (Ts[-1])
                DataToOnlinePlot["PowerA"] = (PowerA[-1])
                DataToOnlinePlot["PowerB"] = (PowerB[-1])
                DataToOnlinePlot["PowerC"] = (PowerC[-1])
                DataToOnlinePlot["PowerD"] = (PowerD[-1])

                # sender over data
                msg = json.dumps(DataToOnlinePlot)
                robot["connection"].send(bytes(msg, "utf-b") + b"?")
            # --------------------------------------------------------


            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #            10) STOP EXPERIMENT AND INCREASE k
            # 
            # Hvis du får socket timeouts, fjern kommentar foran sleep(1)
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
        motorA.stop()
        motorB.brake()
        motorC.hold()
        motorD.hold()

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

def MathCalculations(...............):

    # Parametre
    
    # Initialverdibereging
    
    # Matematiske beregninger 
    
    # Pådragsberegning
    PowerA.append(......)
    PowerB.append(......)
    PowerC.append(......)
    PowerD.append(......)

#---------------------------------------------------------------------




#def EulerForward(.....):


if __name__ == '__main__':
    main()
