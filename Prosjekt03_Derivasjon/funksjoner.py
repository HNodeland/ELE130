def EulerForward(IntValueOld, FunctionValue, TimeStep):
    if len(IntValueOld) == 1:
        IntValueOld.append(0)

    else:
        IntValueOld.append(IntValueOld[-1] + TimeStep[-1]*FunctionValue[-1])
    

def iir_filtration(Index, Value, Value_iir, Alfa_verdi):
    if len(Index) == 1:
        Value_iir.append(Value[0])
    else:
        Value_iir.append((Alfa_verdi*Value[-1])+((1-Alfa_verdi)*Value_iir[-1]))

def iir_filtration2(Index, Value, Value_iir2, Alfa_verdi):
    if len(Index) == 1:
        Value_iir2.append(Value[0])
    else:
        Value_iir2.append((Alfa_verdi*Value[-1])+((1-Alfa_verdi)*Value_iir2[-1]))


def fir_filtration(Index, Value, Value_fir, m_value):
    if len(Index) == 1:
        Value_fir.append(Value[0])
    else:
        sumValue = 0
        if len(Index) < m_value:
            m_value = len(Index)
    sumValue = sum(Value[- m_value:])
    Value_fir.append((1/m_value) * sumValue)



def derivasjon(Index, Value, Derivative):
    if len(Index) == 1:
        Derivative.append(0)
        
    else:
        DeltaIndex = (Index[-1] - Index[-2])            #Tidsskritt (Bredde)
        DeltaValue = (Value[-1] - Value[-2])        #Funksjonsverdi (Høyde)
        
        Derivative.append(DeltaValue / DeltaIndex)

def derivasjon2(Index, Value, Derivative2):
    if len(Index) == 1:
        Derivative2.append(0)
        
    else:
        DeltaIndex = (Index[-1] - Index[-2])            #Tidsskritt (Bredde)
        DeltaValue = (Value[-1] - Value[-2])        #Funksjonsverdi (Høyde)
        
        Derivative2.append(DeltaValue / DeltaIndex)


