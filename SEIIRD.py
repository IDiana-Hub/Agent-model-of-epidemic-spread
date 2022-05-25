import random
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *
from math import floor
random.seed()
N=200 #популяція
Ni=1 #початкова кількість хворих 
Nf=0 
Nc=0
time=0
y=0
d=0
h1=0
h2=0
u=0
o=0;
e=0;
S=N-Ni; I=Ni;I2=0;E=0;R=0;D=0; t=0; Imax=0; Itotal=I; I2max=0;
St=[];It=[];I2t=[];Et=[];Rt=[];Dt=[];T=[]
Population=[]
class human:
    def __init__(self, ID,r, Status):
        self.ID=ID; self.Status=Status; self.Contact=list(); self.T=r

    def family(self, Nf):
        for i in range(1, Nf+1):
            a = self.ID-i; a = round(a)
            self.Contact.append(serch(a))
    def newC(self, Nc, Nf):
        for i in range(Nc):
            a=random.randint(0, N-1)
            self.Contact.insert(Nf+i, serch(a))
    def toInf(self, t, y,d,h1,h2,u,o,e, Nf,Nc):
        global S,E,I,I2,R,D, Imax, Itotal, I2max
        z=int(random.randint(-3, 3))
        delta=t-self.T
        b=random.random()
        match (self.Status):
            case "S":
                a=0;a2=0
                for i in range(Nf+Nc):
                    if (self.Contact[i]==None):
                        print(i)
                        print(self.ID, self.Contact[i-1])
                    if (self.Contact[i].Status=="I"): a+=1;
                    if (self.Contact[i].Status=="I2"): a2+=1;
                if (b<=a*y+a2*o):
                    self.Status="E"; self.T=t; S-=1; E+=1;
            case "E":
                if (delta>=d+z):
                    if (b<=e): self.Status="I"
                    else:
                        self.Status="I2"
                        I2+=1
                        if(I2>I2max): I2max=I2
                    self.T=t
                    E-=1; I+=1; Itotal+=1
                    if(I>Imax): Imax=I
                    if(E<0 or I<0):
                        print("магия")
                        print(self.ID, self.Status)
            case "I":
                if(delta>=h1+z):
                    I-=1
                    self.Status="R"
                    R+=1;
            case "I2":
                if(delta>=h2+z):
                    I-=1; I2-=1
                    if (b<=u):
                        self.Status="D"
                        D+=1;
                    else:
                        self.Status="R"
                        R+=1;
                    if(E<0 or I<0):
                        print("магия")
                        print(self.ID, self.Status)
def serch(n):
    global Population
    for i in range(N):
        if (Population[i].ID==n):
            return Population[i];
    print(n, "нет такого")
def round(i):
    global N
    if (i<0): return N+i
    else: return i
def update():
    global S,E,I,I2,R,D,t
    T.append(t)
    St.append(S)
    Et.append(E)
    It.append(I)
    I2t.append(I2)
    Rt.append(R)
    Dt.append(D)

def p(t):
    if(t<10 or t>50): return 1
    else:
        a=0.5+((t-30)*0.041)*((t-30)*0.041)*((t-30)*0.041)*((t-30)*0.041)
        return a

def pley():
    global Population, S,E,I,I2,R,D, Imax, Itotal, root, t
    Nf=int(Nftxt.get()) #постійні контакти
    Nc=int(Nctxt.get()) #випадкові контакти
    time=int(timetxt.get())#час моделювання
    y=float(ytxt.get()) #заразність
    o=float(otxt.get()) #заразність безсимтомних та у інкубаційний період
    d=float(dtxt.get()) #інкубаційний період
    h1=float(h1txt.get()) #днів до одужання безсимптомних
    h2=float(h2txt.get()) #днів до одужання
    u=float(utxt.get()) #ко-оф смертності
    e=float(etxt.get()) #частка безсимптомних хворих
    for i in range(N):
        Population[i].family(Nf)
    for t in range(time):
        #print(t)
        Nf=int(Nftxt.get())
        Nc=int(Nctxt.get())
        if (Q.get()==1):
            Nf=floor(Nf*p(t))
            Nc=floor(Nc*p(t))
        for i in range(N):
            Population[i].newC(Nc, Nf)
            Population[i].toInf(t, y,d,h1,h2,u,o,e, Nf,Nc)
        update()
    lS.configure(text="Вразливі = "+ str(S))
    lE.configure(text="Латантні = "+ str(E))
    lI.configure(text="Інфіковані = "+ str(I))
    lI2.configure(text="Тяжкохворі = "+ str(I))
    lR.configure(text="Одужавши = "+ str(R))
    lD.configure(text="Померлі = "+ str(D))
    lt.configure(text="t = "+ str(t))
    lImax.configure(text="загальна кількість захворілих = "
                    +str(Itotal)+"\n максимальна кількість хворих одночасно = "
                    +str(Imax)+"\n максимальна кількість тяжкохворих одночасно = "
                    +str(I2max))
    plt.draw()
def graf():
    plt.plot(T, St, color ="#7FFF00", label="S")
    plt.plot(T, Et, color ="#FFFF00", label="E")
    plt.plot(T, It, "--", color ="#FF0000", label="I")
    plt.plot(T, I2t, color ="#FF0000", label="I2")
    plt.plot(T, Rt, color ="#006400", label="R")
    plt.plot(T, Dt, color ="#000000", label="D")
    plt.legend()
    plt.show()
    
for i in range(N-Ni):
    Population.append(human(i,0,"S"))
for i in range(Ni):
    Population.append(human(N-Ni+i,0,"I"))      

root = Tk()
root.title("SIERD")
l3 = Label(root, width=28, text="популяція")
l4 = Label(root, width=28, text="початкова кількість хворих")
l1 = Label(root, width=28, text="постійні контакти")
l2 = Label(root, width=28, text="випадкові контакти")
l5 = Label(root, width=28, text="час моделювання")
l6 = Label(root, width=28, text="заразність")
l10 = Label(root, width=28, text="заразність безсимтомних/іп")
l7 = Label(root, width=28, text="інкубаційний період")
l8 = Label(root, width=28, text="днів до одужання")
l11 = Label(root, width=28, text="днів до одужання безсимптомних")
l9 = Label(root, width=28, text="ко-оф смертності")
l12 = Label(root, width=28, text="частка безсимптомних хворих")
Nftxt = Entry(root,width=5); Nftxt.insert(0, "10")
Nctxt = Entry(root,width=5); Nctxt.insert(0,"20")
Ntxt = Entry(root,width=5); Ntxt.insert(0,"200")
Nitxt = Entry(root,width=5); Nitxt.insert(0,"1")
timetxt = Entry(root,width=5);timetxt.insert(0,"100")
ytxt = Entry(root,width=5); ytxt.insert(0,"0.0194")
otxt = Entry(root,width=5); otxt.insert(0,"0.008")
dtxt = Entry(root,width=5); dtxt.insert(0,"5")
h1txt = Entry(root,width=5); h1txt.insert(0,"7")
h2txt = Entry(root,width=5); h2txt.insert(0,"30")
utxt = Entry(root,width=5); utxt.insert(0,"0.03")
etxt = Entry(root,width=5); etxt.insert(0,"0.8")
lN = Label(root, text="N = "+ str(N))
lS = Label(root, text="S = "+ str(S))
lE = Label(root, text="E = "+ str(E))
lI = Label(root, text="I = "+ str(I))
lI2= Label(root, text="I2= "+ str(I2))
lR = Label(root, text="R = "+ str(R))
lD = Label(root, text="D = "+ str(D))
lt = Label(root, text="t = "+ str(t))
lImax = Label(root, text="")
l3.grid(column=0, row=0)
l4.grid(column=0, row=1)
l1.grid(column=0, row=2)
l2.grid(column=0, row=3)
l5.grid(column=0, row=4)
l6.grid(column=0, row=5)
l10.grid(column=0, row=6)
l7.grid(column=0, row=7)
l8.grid(column=0, row=8)
l11.grid(column=0, row=9)
l9.grid(column=0, row=10)
l12.grid(column=0, row=11)
Ntxt.grid(column=1, row=0)
Nitxt.grid(column=1, row=1)
Nftxt.grid(column=1, row=2)
Nctxt.grid(column=1, row=3)
timetxt.grid(column=1, row=4)
ytxt.grid(column=1, row=5)
otxt.grid(column=1, row=6)
dtxt.grid(column=1, row=7)
h1txt.grid(column=1, row=9)
h2txt.grid(column=1, row=8)
utxt.grid(column=1, row=10)
etxt.grid(column=1, row=11)
lN.grid(column=2, row=0)
lS.grid(column=2, row=1)
lE.grid(column=2, row=2)
lI.grid(column=2, row=3)
lImax.grid(column=3, row=7)
lI2.grid(column=2, row=4)
lR.grid(column=2, row=5)
lD.grid(column=2, row=6)
lt.grid(column=2, row=7)
BStart = Button(root, text="Почати", command=pley)
BStart.grid(column=2, row=12)
BStart = Button(root, text="Графік", command=graf)
BStart.grid(column=2, row=11)
Q=IntVar()
Chec = Checkbutton(root, text="карантинні обмежання", variable=Q)
Chec.grid(column=0, row=12)
root.mainloop()
