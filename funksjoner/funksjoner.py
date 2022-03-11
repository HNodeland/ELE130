
#---INTEGRASJON---
def EulerForward(IntValueOld, FunctionValue, TimeStep):
    if len(IntValueOld) == 1:
        IntValueOld.append(0)

    else:
        IntValueOld.append(IntValueOld[-1] + TimeStep[-1]*FunctionValue[-1])
    
#---IIR FILTER---
def iir_filtration(Value, Value_iir, Alfa_verdi):
    if len(Value) == 1:
        Value_iir.append(Value[0])
    else:
        Value_iir.append((Alfa_verdi*Value[-1])+((1-Alfa_verdi)*Value_iir[-1]))

#---FIR FILTER---
def fir_filtration(Index, Value, Value_fir, m_value):
    if len(Index) == 1:
        Value_fir.append(Value[0])
    else:
        sumValue = 0
        if len(Index) < m_value:
            m_value = len(Index)
    sumValue = sum(Value[- m_value:])
    Value_fir.append((1/m_value) * sumValue)

#---DERIVASJON---
def derivasjon(Index, TimeStep, Value, delta_Value, Derivative):
    
    if len(Index) == 1:
        TimeStep.append(0)
        delta_Value.append(0)
        Derivative.append(0)
        

        
    elif len(Index) == 2:
        Derivative.append(0)
        TimeStep.append(Index[-1] - Index[-2])
        delta_Value.append(Value[-1] - Value[-2])

    else:
        TimeStep.append(Index[-1] - Index[-2])
        delta_Value.append(Value[-1] - Value[-2])
        Derivative.append(delta_Value[-1] / TimeStep[-1])
       

