from qiskit import*
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import SXdgGate

import math
import matplotlib.pyplot as plt
import numpy as np
import qiskit_aer
import time

csxdg_gate = SXdgGate().control() #To generate the V and V*- gates
getbinary = lambda x, n: format(x, 'b').zfill(n) #to get the binary representation with n-bit precision

def AddOperator(t,qc,add_v,s):
    for n in range(t):
        if n<t-1:
            qc.append(csxdg_gate, [s[n+t],   add_v[n+1]])
            qc.append(csxdg_gate, [s[n],     add_v[n+1]])
            qc.append(csxdg_gate, [add_v[n], add_v[n+1]])
            qc.cx(s[n],   s[n+t])
            qc.cx(s[n+t], add_v[n])
            qc.cx(s[n],   s[n+t])
            qc.csx(add_v[n], add_v[n+1])
            qc.barrier()
        else: #The carry bit is discarded
            qc.cx(s[n],   s[n+t])
            qc.cx(s[n+t], add_v[n])
            qc.cx(s[n],   s[n+t])
            qc.barrier()
    return qc

def SubOperator(t,qc,sub_v,s):
    qc.append(csxdg_gate, [s[t], sub_v[0]])
    qc.cx(s[0] , s[t]) #Here we discard the 0 position of the add_v variable (it is equal to subtract 1)
    qc.csx(s[0], sub_v[0])
    qc.csx(s[t], sub_v[0])
    qc.barrier()
    for n in range(1,t,1):
        if n<t-1:
            qc.append(csxdg_gate, [s[n+t], sub_v[n]])
            qc.cx(s[n],  s[n+t])
            qc.csx(s[n], sub_v[n])
            qc.cx(sub_v[n-1],  s[n+t])
            qc.csx(sub_v[n-1], sub_v[n])
            qc.csx(s[n+t],   sub_v[n])
            qc.barrier()
        else:
            qc.cx(s[n],  s[n+t])
            qc.cx(sub_v[n-1],  s[n+t])
            qc.barrier()
    return qc

#Two complement function - For integer numbers
def TwoComplementI(number, bit_precision):
    t = getbinary(int(number), bit_precision+1)
    temp = int(t, 2)
    inverse_s = temp ^ (2 ** (len(t) + 1) - 1)
    rslt = bin(inverse_s)[3 : ]
    b = '01'
    sum = bin(int(rslt, 2) + int(b, 2))
    sum = int(sum,2)
    return (sum)

#Two complement function - For binary numbers
def TwocomplementB(number):
    temp = int(number, 2)
    inverse_s = temp ^ (2 ** (len(number) + 1) - 1)
    rslt = bin(inverse_s)[3 : ] 
    b = '01'
    sum = bin(int(rslt, 2) + int(b, 2))
    return (sum[2:]) 

def QCircuit(bit_precision):
    #-------Register initialization-------
    s = QuantumRegister(2*bit_precision,'s')
    #Addition variable
    add_v = QuantumRegister(bit_precision + 1,'a') #The +1 is for the rounding operation
    #Classical register 
    cr = ClassicalRegister(bit_precision*2,'c')
    #Subtraction variable
    sub_v = QuantumRegister(bit_precision-1,'d')
    #Circuit definition 
    qc = QuantumCircuit(s,add_v, sub_v, cr)    
    return (qc, add_v, sub_v, s)

#Simulation process
def FSimulation(circuit):
    simulator = qiskit_aer.Aer.get_backend('qasm_simulator')
    job = transpile(circuit, backend=simulator)
    result = simulator.run(job).result()
    counts = result.get_counts()
    return(counts)

def initialComplement(a,b, bit_precision):
    p = ''
    if a<0:
        #Signal[2*i] = TwoComplementI(Signal[2*i]*-1,bit_precision-1)
        p = getbinary(int(TwoComplementI(a*-1,bit_precision-1)), bit_precision)[::-1]
    else:
        p =  getbinary(int(a), bit_precision)[::-1]        
    if b<0:
        #Signal[2*i+1] = TwoComplementI(Signal[2*i+2]*-1,bit_precision-1)
        p = p + getbinary(int(TwoComplementI(b*-1,bit_precision-1)), bit_precision)[::-1]
    else:
        p = p + getbinary(int(b), bit_precision)[::-1]
    return p

def QISTransform(Signal, DLevel, bit_precision):
    #Initial Zero padding (it is because we need a 2^n signal elements)
    while (Signal.size)%2!=0 or (Signal.size)<2:
        Signal = np.append(Signal,0)
    # Exception
    max_depth = len(Signal)//2
    if DLevel> max_depth:
      raise Exception("Sorry, depth nya kakehan")
    #Decomposition level
    list_AD = []
    for level in range(0, DLevel):
        if level>0:
            Signal = np.array(ai)
            if Signal.size%2==1:
                Signal = np.append(Signal,0)
        di  = [] #to store the D(i) coefficient
        ai  = [] #to store the A(i) coefficient
        for i in range(0,int(Signal.size/2),1):
            #Take the next three elements of the signal
            signal = [Signal[2*i], Signal[2*i+1]]
            #Two's complement to the initial signal elements (return a string with the binary representation)
            p = initialComplement(Signal[2*i], Signal[2*i+1], bit_precision)
            #Circuit definition
            (circuit,add_v,sub_v,s) = QCircuit(bit_precision)
            #-------Signal elements storing-------
            #Apply the X gate when the bit is 1, and I gate when is 0
            if [j for j in range(len(p)) if p[j]=='1'] !=[]:
                circuit.x( [j for j in range(len(p)) if p[j]=='1'])
            circuit.barrier()
            #-------Operators-------
            #Addition operation -- Between the S(2i) and S(2i+1) signal elements
            circuit = AddOperator(bit_precision, circuit, add_v, s)
            #For the rounding - Copy the MSB into the next qubit
            circuit.cx(add_v[-2],add_v[-1])
            circuit.barrier()
            #Subtraction operation -- Between the S(2i+1) and the S(2i) element
            circuit = SubOperator(bit_precision, circuit, sub_v, s)
            #-------Measurement-------
            r_1 = [add_v[o] for o in range(1,bit_precision+1,1)]
            r_2 = [s[o] for o in range(bit_precision, 2*bit_precision,1)]
            r = np.append(r_1,r_2)
            m = range(bit_precision*2) #Number of classical bits
            circuit.measure(r, m)
            #-------Simulation-------
            d = str(FSimulation(circuit))
            #Extract the binary representation
            a_1 = d[2+bit_precision:2*bit_precision+2]
            d_1 = d[2:2+bit_precision]
            #Two's complement of the number
            if d_1[0]=='1':
                d_1 = int(TwocomplementB(d_1),2)*-1
            else:
                d_1 = int(d_1, 2)

            if a_1[0]=='1':
                a_1 = int(TwocomplementB(a_1),2)*-1
            else:
                a_1 = int(a_1, 2)
            #Store the coefficient D(i) in the variable
            ai.append(a_1)
            di.append(d_1)
        list_AD.append(di)
        if level==(DLevel-1):
            list_AD.append(ai)
    list_AD = list_AD[::-1]
    # display(circuit.draw("mpl"))
    return list_AD

def InvQISTransform(input, bit_precision):
    DLevel = len(input) - 1
    Ai = np.array(input[0])
    Di = np.array(input[1])
    for level in range(DLevel):
        ai  = [] #to store the A(i) coefficient
        for i in range(Ai.size):
            #Take the next three elements of the signal
            signal = [Di[i], 2*Ai[i]]
            if Di[i]%2==1:
                signal = [Di[i], 2*Ai[i]+1]
            #Two's complement to the initial signal elements (return a string with the binary representation)
            p = initialComplement(signal[0], signal[1], bit_precision)
            #Circuit definition
            (circuit,add_v,sub_v,s) = QCircuit(bit_precision)
            #-------Signal elements storing-------
            #Apply the X gate when the bit is 1, and I gate when is 0
            if [j for j in range(len(p)) if p[j]=='1'] !=[]:
                circuit.x( [j for j in range(len(p)) if p[j]=='1'])
            circuit.barrier()
            #-------Operators-------
            #Addition operation -- Between the S(2i) and S(2i+1) signal elements
            circuit = AddOperator(bit_precision, circuit, add_v, s)
            #For the rounding - Copy the MSB into the next qubit
            circuit.cx(add_v[-2],add_v[-1])
            circuit.barrier()
            #Subtraction operation -- Between the S(2i+1) and the S(2i) element
            circuit = SubOperator(bit_precision, circuit, sub_v, s)
            #-------Measurement-------
            r_1 = [add_v[o] for o in range(1,bit_precision+1,1)]
            r_2 = [s[o] for o in range(bit_precision, 2*bit_precision,1)]
            r = np.append(r_1,r_2)
            m = range(bit_precision*2) #Number of classical bits
            circuit.measure(r, m)
            #-------Simulation-------
            d = str(FSimulation(circuit))
            #Extract the binary representation
            a_1 = d[2+bit_precision:2*bit_precision+2]
            d_1 = d[2:2+bit_precision]
            #Two's complement of the number
            if d_1[0]=='1':
                d_1 = int(TwocomplementB(d_1),2)*-1
            else:
                d_1 = int(d_1, 2)
            if a_1[0]=='1':
                a_1 = int(TwocomplementB(a_1),2)*-1
            else:
                a_1 = int(a_1, 2)

            ai.append(d_1//2)
            ai.append(a_1)

        Ai = np.array(ai)
        if Ai[-1]==0:
            Ai = Ai[:-1]
        if level<DLevel-1:
            Di = input[level+2]
    return Ai

def QISTransformLevel(Signal, Key, bit_precision):
  for i in range(len(Key)):
      list_result = QISTransform(Signal, Key[i], bit_precision)
      Signal = np.concatenate(list_result).ravel()
  return list_result

def InvQISTransformLevel(inv_result, Key, bit_precision):
  Key = Key[::-1]
  for i in range(len(Key)):
      list_result = []
      for j in range(Key[i]):
          list_result.append(inv_result[-(len(inv_result)//2):])
          inv_result = inv_result[:-(len(inv_result)//2)]
      list_result.append(inv_result)
      list_result = list_result[::-1]
      inv_result = InvQISTransform(list_result, bit_precision)
  return inv_result

def permutation_matrix(n):
    P = np.eye(n) 
    np.random.shuffle(P)
    return P

def enkripsi(PlainText, Key, bit_precision):    
    start_time = time.time()
    SignalOri = np.array([ord(char) for char in PlainText])
    Signal = SignalOri % 16
    k = (SignalOri-Signal)//16
    list_result = QISTransformLevel(Signal, Key, bit_precision)
    arr_result = np.concatenate(list_result).ravel()
    A = permutation_matrix(len(Signal))
    Key3 = np.dot(A, k)
    Key3 = Key3.astype(int)
    if len(Key3) < len(arr_result):
        Key3 = np.append(Key3, np.ones(len(arr_result) - len(Key3), dtype=int))
    Key2 = np.where(arr_result < 0, 1, 0)
    X = (abs(arr_result) + 32)*Key3
    ChiperText = ''.join(chr(x) for x in X)
    te = round(time.time() - start_time, 2)
    print(len(SignalOri))
    return ChiperText, A, Key3, Key2, te

def deskripsi(ChiperText, A, Key3, Key2, Key, bit_precision):
    start_time = time.time()
    signalChip = (np.array([ord(char) for char in ChiperText])//Key3)-32
    signalChip = np.where(Key2 == 1, -signalChip, signalChip)
    invChipper = InvQISTransformLevel(signalChip, Key, bit_precision)
    Key3 = Key3[Key3 != 1]
    A_inv = np.linalg.inv(A)
    Key3 = np.dot(A_inv, Key3)
    Key3 = Key3.astype(int)
    inverschip = invChipper+(Key3*16)
    invChipperText = ''.join([chr(x) for x in inverschip])
    td = round(time.time() - start_time, 2)
    return invChipperText, td

def corelation_value(PlainText, ChiperText):
    plain_num = np.array([ord(char) for char in PlainText])
    chip_num = np.array([ord(char) for char in ChiperText])
    min_length = min(len(plain_num), len(chip_num))
    plain_num = plain_num[:min_length]
    chip_num = chip_num[:min_length]
    correlation_matrix = np.corrcoef(plain_num, chip_num)
    correlation_value = abs(round(correlation_matrix[0, 1],5))
    return correlation_value

def count_characters(char, text):
    return text.count(char)

def encryption_quality(PlainText, ChiperText):
    temp = 0
    n = 65536 - 32
    for i in range(32, 65536):
        temp += abs(count_characters(chr(i), PlainText) - count_characters(chr(i), ChiperText))
    result = temp / n
    n1 = len(PlainText)
    n2 = len(ChiperText)
    if 2 * n1 < n2:
        max_quality_enk = round(2 * n2 / n,5)
    else:
        max_quality_enk = round(2 * n2 / n,5)
    persent_quality_enk = round((result / max_quality_enk) * 100,2)
    return max_quality_enk, persent_quality_enk