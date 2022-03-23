def EulerForward(IntValue, FunctionValue, TimeStep):
    if len(IntValue) == 1:
        IntValue.append(0)

    else:
        IntValue.append(IntValue[-1] + TimeStep[-1]*FunctionValue[-1])
    

def iir_filtration(Index, Value, Value_iir, Alfa_verdi):
    if len(Index) == 1:
        Value_iir.append(Value[0])
    else:
        Value_iir.append((Alfa_verdi*Value[-1])+((1-Alfa_verdi)*Value_iir[-1]))


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


