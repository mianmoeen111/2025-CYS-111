graph={'A':{'B':2,'C':10},'B':{'C':3},'C':{}}
A=0
B=999
C=999
visited=[]
visited.append('A')
if A+graph['A']['B']<B:
    B=A+graph['A']['B']
    visited.append('B')
if B+graph['A']['C']<C:
    C=B+graph['A']['C']
    visited.append('C')
print(f'{visited} A={A} B={B} C={C}')