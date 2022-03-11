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

def fir_filtration(Index, Value, Value_fir, m_value):
    if len(Index) == 1:
        Value_fir.append(Value[0])
    else:
        sumValue = 0
        if len(Index) < m_value:
            m_value = len(Index)
    sumValue = sum(Value[- m_value:])
    Value_fir.append((1/m_value) * sumValue)



Ts = [1]

def derivasjon(Index, Value, Value_iir, Derivative, Alfa_verdi):
    if len(Index) == 1:
      
        Value_iir.append(Value)
        Derivative.append(0)
        
    else:
        Value_iir.append(iir_filtration(Index, Value, Value_iir, Alfa_verdi))

        DeltaIndex = (Index[-1] - Index[-2])            #Tidsskritt (Bredde)
        DeltaValue = (Value_iir[-1] - Value_iir[-2])    #Funksjonsverdi (Høyde)
        
        Derivative.append(DeltaValue / DeltaIndex)

