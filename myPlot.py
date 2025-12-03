# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Sajjad Foroughi
"""
A Novel Method That Corrects Steady-State Relative Permeability Calculations for Inhomogeneous Saturation Profiles Along the Flow Direction.

Author: Dr. Sajjad Foroughi (Imperial College London)
Contact: s.foroughi@imperial.ac.uk
Repository: https://github.com/ImperialCollegeLondon/relPermCorrection
License: MIT

If you use this code, please cite:
1. Zhang, G., Foroughi, S., Bijeljic, B., & Blunt, M. J. (2023). 
A method to correct steady-state relative permeability measurements for inhomogeneous saturation profiles in one-dimensional flow. 
Transport in Porous Media. https://doi.org/10.1007/s11242-023-01993-6
2. Guanglei Zhang, Sajjad Foroughi, Ali Q. Raeini, Martin J. Blunt, and Branko Bijeljic. 
"The Impact of Bimodal Pore Size Distribution and Wettability on Relative Permeability and Capillary Pressure in a Microporous Limestone with Uncertainty Quantification." 
Advances in Water Resources 171 (2023): 104352.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import os

import matplotlib
import os

plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = ['Times New Roman']
matplotlib.rcParams.update({'font.size': 14})


inSwExpMax = np.array([0.19921092,	0.3199588631,	0.408699803,	0.5996927998,	0.6469354051,	0.6979354051,	0.7266751209,	0.8586492147])
inSwExpMin = np.array([0.17078908,	0.2900411369,	0.371300197,	0.5563072002,	0.5990645949,	0.6500645949,	0.6713248791,	0.7853507853])
							
inkrWExpMax =np.array([0,	0.0442299509,	0.0729332242,	0.048413257,	0.0517566285,	0.0765499182,	0.0970765957,	0.5212831424])
inkrWExpMin = np.array([0,	0.0147700491,	0.0074667758,	0.002586743,	0.0288433715,	0.0274500818,	0.0545234043,	0.4067168576])

inkrOExpMax = np.array([0.9244697218,	0.4135499182,	0.2615531915,	0.0644099836,	0.0484833061,	0.0295833061,	0.0174733061,	0])
inkrOExpMin = np.array([0.7575302782,	0.3644500818,	0.1764468085,	0.0545900164,	0.0321166939,	0.0132166939,	0.0011066939,	0])




krW = np.array([0,	0.0295,	0.0402,	0.0255,	0.0403,	0.052,	0.0758,	0.464])
krO = np.array([0.841,	0.389,	0.219,	0.0595,	0.0403,	0.0214,	0.00929,	0])


a = (pd.read_excel('Sw.xlsx'))
#a = (pd.read_excel('test.xlsx'))
Sws = a.to_numpy()

plt.figure(1)

SWEXPMean = np.array([0.185,	0.305,	0.39,	0.578,	0.623,	0.674,	0.699,	0.822])#np.mean(Sws,axis=0)
print(SWEXPMean)
AllKrOil = np.transpose(np.loadtxt("AllKrOil.txt"))
AllKrWater = np.transpose(np.loadtxt("AllKrWater.txt"))
kroMean = np.mean(AllKrOil,axis=0)
kroMax= np.amax(AllKrOil,axis=0)
kroMin= np.amin(AllKrOil,axis=0)
krwMean = np.mean(AllKrWater,axis=0)
krwMax= np.amax(AllKrWater,axis=0)
krwMin= np.amin(AllKrWater,axis=0)
plt.fill_between(SWEXPMean,kroMax[:-1],kroMin[:-1],color = 'r',alpha=0.2,label='_nolegend_')

print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
print("SWEXPMean",SWEXPMean[:-1])
print("kroMax :",kroMax[:-1])
print("kroMin :",kroMin[:-1])
print("kroMean :",kroMean[:-1])
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
print("SWEXPMean",SWEXPMean[:-1])
print("krwMax :",krwMax[:-1])
print("krwMin :",krwMin[:-1])
print("krwMean :",krwMean[:-1])
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
plt.plot(SWEXPMean,kroMax[:-1],color = 'r',alpha=0.2,label='_nolegend_')
plt.plot(SWEXPMean,kroMin[:-1],color = 'r',alpha=0.2,label='_nolegend_')
plt.plot(SWEXPMean,kroMean[:-1],':r+',label = "Mean of realisations (Oil)")

plt.fill_between(SWEXPMean,krwMax[:-1],krwMin[:-1],color = 'b',alpha=0.2,label='_nolegend_')
plt.plot(SWEXPMean,krwMax[:-1],color = 'b',alpha=0.35,label='_nolegend_')
plt.plot(SWEXPMean,krwMin[:-1],color = 'b',alpha=0.35,label='_nolegend_')
plt.plot(SWEXPMean,krwMean[:-1],':bx',label = "Mean of realisations (Water)")

plt.plot(SWEXPMean,krO,'ro', label = "Uniform (Oil)",linestyle='dashed')
plt.plot(SWEXPMean,krW,'bs', label = "Uniform (Water)",linestyle='dashed')

yO_error = [krO - inkrOExpMin, inkrOExpMax - krO]
yW_error = [krW - inkrWExpMin, inkrWExpMax - krW]
x_error = [SWEXPMean - inSwExpMin, inSwExpMax - SWEXPMean]
plt.errorbar(SWEXPMean,krO, yerr=yO_error, xerr=x_error, fmt='ro', capsize=3)
plt.errorbar(SWEXPMean,krW, yerr=yW_error, xerr=x_error, fmt='bs', capsize=3)


#plt.fill(np.append(inSwExpMin, inSwExpMax[::-1]),np.append(inkrOExpMin, inkrOExpMax[::-1]),color = 'r',alpha=0.15,label='_nolegend_',hatch="+++")
#plt.fill(np.append(inSwExpMax, inSwExpMin[::-1]),np.append(inkrWExpMin, inkrWExpMax[::-1]),color = 'b',alpha=0.15,label='_nolegend_',hatch="xxx")

plt.legend()
m,n=np.shape(AllKrOil)
m,n=np.shape(AllKrWater)

plt.xlabel('$S_w$')
plt.ylabel('$k_r$')


ax = plt.gca()  # gca stands for 'get current axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
plt.xlim(0, 1)
plt.ylim(0, 1)
#ax.set_xlabel('$S_w$', ontname="Arial", size=16,fontweight="bold")
#ax.set_ylabel('$k_r$', fontname="Arial", size=16,fontweight="bold")
ax.set_xlabel('$S_w$',  size=16,fontweight="bold")#, family='Arial')
ax.set_ylabel('$k_r$',  size=16,fontweight="bold")#, family='Arial')
#rc('font',**{'family':'serif','serif':['Times']})
#rc('text', usetex=True)

name = "Fig1"

if os.path.exists(name+".png"):
	os.remove(name+".png")        
plt.savefig(name+".png",dpi=100,bbox_inches='tight')
if os.path.exists(name+".eps"):
	os.remove(name+".eps")        
plt.savefig(name+".eps",format='eps',bbox_inches='tight')
#plt.show()
#exit()
'''
plt.figure(20)
yO_error = [krO - inkrOExpMin, inkrOExpMax - krO]
yW_error = [krW - inkrWExpMin, inkrWExpMax - krW]
x_error = [SWEXPMean - inSwExpMin, inSwExpMax - SWEXPMean]
plt.errorbar(SWEXPMean,krO, yerr=yO_error, xerr=x_error, fmt='rx')
#plt.errorbar(SWEXPMean,krW, yerr=yW_error, xerr=x_error, fmt='b+')
'''
#exit()
Lower_yValue = 1e-3

plt.figure(2)
plt.fill_between(SWEXPMean[:-1],kroMax[:-2],kroMin[:-2],color = 'r',alpha=0.2,label='_nolegend_')

plt.plot(SWEXPMean[:-1],kroMax[:-2],color = 'r',alpha=0.2,label='_nolegend_')
plt.plot(SWEXPMean[:-1],kroMin[:-2],color = 'r',alpha=0.2,label='_nolegend_')
plt.plot(SWEXPMean[:-1],kroMean[:-2],':r+',label = "Mean of realisations (Oil)")

plt.fill_between(SWEXPMean[1:],krwMax[1:-1],krwMin[1:-1],color = 'b',alpha=0.2,label='_nolegend_')
plt.plot(SWEXPMean[1:],krwMax[1:-1],color = 'b',alpha=0.2,label='_nolegend_')
plt.plot(SWEXPMean[1:],krwMin[1:-1],color = 'b',alpha=0.2,label='_nolegend_')
plt.plot(SWEXPMean[1:],krwMean[1:-1],':bx',label = "Mean of realisations (Water)")


plt.plot(SWEXPMean[:-1],krO[:-1],'ro', label = "Uniform (Oil)",linestyle='dashed')
plt.plot(SWEXPMean[1:],krW[1:],'bs', label = "Uniform (Water)",linestyle='dashed')

yO_error = [krO[:-1] - inkrOExpMin[:-1], inkrOExpMax[:-1] - krO[:-1]]
yW_error = [krW[1:] - inkrWExpMin[1:], inkrWExpMax[1:] - krW[1:]]
xO_error = [SWEXPMean[:-1] - inSwExpMin[:-1], inSwExpMax[:-1] - SWEXPMean[:-1]]
xW_error = [SWEXPMean[1:] - inSwExpMin[1:], inSwExpMax[1:] - SWEXPMean[1:]]
plt.errorbar(SWEXPMean[:-1],krO[:-1], yerr=yO_error, xerr=xO_error, fmt='ro')
plt.errorbar(SWEXPMean[1:],krW[1:], yerr=yW_error, xerr=xW_error, fmt='bs')
'''
myX1 = inSwExpMin[:-1]
myX2 = inSwExpMax[:-1]
myY1 = inkrOExpMin[:-1]
myY2 = inkrOExpMax[:-1]
plt.fill(np.append(myX1, myX2[::-1]),np.append(myY1, myY2[::-1]),color = 'r',alpha=0.15,label='_nolegend_',hatch="+++")

myX1 = inSwExpMin[1:]
myX2 = inSwExpMax[1:]
myY1 = inkrWExpMin[1:]
myY2 = inkrWExpMax[1:]
plt.fill(np.append(myX2, myX1[::-1]),np.append(myY1, myY2[::-1]),color = 'b',alpha=0.15,label='_nolegend_',hatch="xxx")
'''
plt.legend()
m,n=np.shape(AllKrOil)
m,n=np.shape(AllKrWater)

plt.xlabel('$S_w$')
plt.ylabel('$k_r$')
ax.set_xlabel('$S_w$', fontname="Times New Roman", size=16,fontweight="bold")
ax.set_ylabel('$k_r$', fontname="Times New Roman", size=16,fontweight="bold")
plt.yscale('log')


plt.xlim(0, 1)
plt.ylim(Lower_yValue, 1)

ax = plt.gca()  # gca stands for 'get current axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',Lower_yValue))
#ax.yaxis.set_ticks_position('left')
#ax.spines['left'].set_position(('data',0))
#plt.axis([0, 1, 1e-3, 1])


plt.show()
name = "Fig2"
if os.path.exists(name+".png"):
	os.remove(name+".png")        
#plt.savefig(name+".png",dpi=100,bbox_inches='tight')
if os.path.exists(name+".eps"):
	os.remove(name+".eps")        
plt.savefig(name+".eps",format='eps',bbox_inches='tight')
plt.figure(3)
#exit()
#AllKrOil = (np.loadtxt("AllKrOil.txt"))
#AllKrWater = (np.loadtxt("AllKrWater.txt"))

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)
cmapO = get_cmap(m,'Paired')
cmapW = get_cmap(m,'Paired')
alphaValue = 1.0
myLineWidth = 1.5


plt.plot(SWEXPMean,AllKrOil[0,:-1],color = (1,0,0),alpha=alphaValue,linewidth=myLineWidth,linestyle='dashed',  label='Oil')
plt.plot(SWEXPMean,AllKrWater[0,:-1],color = (0,0,1),alpha=alphaValue,linewidth=myLineWidth,linestyle='dashed',  label='Water')    
for ii in range(1,m):
    rgb = (1,0,0)#cmapO(50)#(random.random(), random.random(), random.random())
    plt.plot(SWEXPMean,AllKrOil[ii,:-1],color = rgb,alpha=alphaValue,linewidth=myLineWidth,linestyle='dashed', label='_nolegend_')
    rgb = (0,0,1)#cmapW(50)
    plt.plot(SWEXPMean,AllKrWater[ii,:-1],color = rgb,alpha=alphaValue,linewidth=myLineWidth,linestyle='dashed', label='_nolegend_')    
ax = plt.gca()  # gca stands for 'get current axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
plt.xlim(0, 1)
plt.ylim(0, 1)
ax.set_xlabel('$S_w$', fontname="Times New Roman", size=16,fontweight="bold")
ax.set_ylabel('$k_r$', fontname="Times New Roman", size=16,fontweight="bold")
plt.plot(SWEXPMean[:-1],krO[:-1],'-r', label = "Uniform (Oil)")
plt.plot(SWEXPMean[1:],krW[1:],'-b', label = "Uniform (Water)")

yO_error = [krO[:-1] - inkrOExpMin[:-1], inkrOExpMax[:-1] - krO[:-1]]
yW_error = [krW[1:] - inkrWExpMin[1:], inkrWExpMax[1:] - krW[1:]]
xO_error = [SWEXPMean[:-1] - inSwExpMin[:-1], inSwExpMax[:-1] - SWEXPMean[:-1]]
xW_error = [SWEXPMean[1:] - inSwExpMin[1:], inSwExpMax[1:] - SWEXPMean[1:]]
plt.errorbar(SWEXPMean[:-1],krO[:-1], yerr=yO_error, xerr=xO_error, fmt=':ro')
plt.errorbar(SWEXPMean[1:],krW[1:], yerr=yW_error, xerr=xW_error, fmt=':bs')
plt.legend()
name = "Fig3"

if os.path.exists(name+".png"):
	os.remove(name+".png")        
plt.savefig(name+".png",dpi=100,bbox_inches='tight')
if os.path.exists(name+".eps"):
	os.remove(name+".eps")        
plt.savefig(name+".eps",format='eps',bbox_inches='tight')
plt.figure(4)

plt.plot(SWEXPMean[:-1],AllKrOil[0,:-2],color = (1,0,0),alpha=alphaValue,linewidth=myLineWidth,linestyle='dashed', label='Oil')
plt.plot(SWEXPMean[1:],AllKrWater[0,1:-1],color = (0,0,1),alpha=alphaValue,linewidth=myLineWidth,linestyle='dashed',  label='Water')    
for ii in range(1,m):
    rgb = (1,0,0)#cmapO(50)#(random.random(), random.random(), random.random())
    plt.plot(SWEXPMean[:-1],AllKrOil[ii,:-2],color = rgb,alpha=alphaValue,linewidth=myLineWidth,linestyle='dashed', label='_nolegend_')
    rgb = (0,0,1)#cmapW(50)#
    plt.plot(SWEXPMean[1:],AllKrWater[ii,1:-1],color = rgb,alpha=alphaValue,linewidth=myLineWidth,linestyle='dashed', label='_nolegend_')    
ax = plt.gca()  # gca stands for 'get current axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',Lower_yValue))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
plt.xlim(0, 1)
plt.ylim(Lower_yValue, 1)
ax.set_xlabel('$S_w$', fontname="Times New Roman", size=16,fontweight="bold")
ax.set_ylabel('$k_r$', fontname="Times New Roman", size=16,fontweight="bold")
plt.plot(SWEXPMean[:-1],krO[:-1],'-r', label = "Uniform (Oil)")
plt.plot(SWEXPMean[1:],krW[1:],'-b', label = "Uniform (Water)")

yO_error = [krO[:-1] - inkrOExpMin[:-1], inkrOExpMax[:-1] - krO[:-1]]
yW_error = [krW[1:] - inkrWExpMin[1:], inkrWExpMax[1:] - krW[1:]]
xO_error = [SWEXPMean[:-1] - inSwExpMin[:-1], inSwExpMax[:-1] - SWEXPMean[:-1]]
xW_error = [SWEXPMean[1:] - inSwExpMin[1:], inSwExpMax[1:] - SWEXPMean[1:]]
plt.errorbar(SWEXPMean[:-1],krO[:-1], yerr=yO_error, xerr=xO_error, fmt=':ro')
plt.errorbar(SWEXPMean[1:],krW[1:], yerr=yW_error, xerr=xW_error, fmt=':bs')
plt.yscale('log')
plt.legend()

plt.gca().spines['top'].set_visible(False)  
plt.gca().spines['right'].set_visible(False)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 16
#'''
name = "Fig4"

if os.path.exists(name+".png"):
	os.remove(name+".png")        
plt.savefig(name+".png",dpi=100,bbox_inches='tight')
if os.path.exists(name+".eps"):
	os.remove(name+".eps")        
plt.savefig(name+".eps",format='eps',bbox_inches='tight')

#'''
plt.show()
