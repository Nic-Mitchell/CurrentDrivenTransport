# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 14:17:40 2025

@author: Nic
"""

import numpy as np
# from scipy import sparse,integrate,interpolate,linalg,optimize
from math import factorial
from scipy import sparse
from scipy.special import erf,eval_genlaguerre
import matplotlib.pyplot as plt
from scipy import integrate as inte
import time
from copy import deepcopy
from mycolorpy import colorlist
import dill # for saving objects
import inspect



filename_base = "180725_ettings_vs_u"

save = True

r_hall0 = 1
N_K_s = [0.1,0.01,0.001,0.0001]
M = 0.05

data_list = [0 for j in range(len(N_K_s))]

Z0 = 20
D_ov_L_plateau = 0


for j in range(len(N_K_s)):
    N_K = N_K_s[j]
    filename=filename_base+"_N_K_"+str(N_K)+"_hall_"+str(r_hall0)+"_M_"+str(M)+"_Z_"+str(Z0)
    with open(filename+".pkl",'rb') as file:
        data = dill.load(file)
        data.L =1/N_K / np.sqrt(1+Z0)
        data_list[j] = data



fig,axes=plt.subplots(2,1,figsize=(5,5.5),height_ratios=(1,0.2))


data_list[0].color="blue"
data_list[1].color="seagreen"
data_list[2].color="darkorange"
data_list[3].color="red"

data_list[0].N_K_label=r"$10^{-1}$"
data_list[1].N_K_label=r"$10^{-2}$"
data_list[2].N_K_label=r"$10^{-3}$"
data_list[3].N_K_label=r"$10^{-4}$"



for data in data_list:
    axes[0].plot( data.u[:,1] , data.q_nonlocal[:,2] / data.q_local[:,2] , color=data.color,label=data.N_K_label)


axes[0].plot(  data.u[:,1] , np.ones(data.N_i) , color="black",linestyle=":")

axes[0].legend(loc="lower left",title=r"$N_K$" ,framealpha=0.5,ncol=4,fontsize=10)



axes[0].set_xlim([0,M])
axes[0].set_ylim([0,2])
axes[0].set_xlabel(r"$N_u=\vert \Delta u\vert /v_{th,e}$")
axes[0].set_ylabel(r"$q_\times^u / q_\times^{u,local}$")


### add markers

M1 = M*0.5


s=100
marker1 = "P"
marker2 = "X"
zorder=2

data = data_list[2]
i0 = np.argmin(np.abs(data.uy - M))
i1 = np.argmin(np.abs(data.uy - M1))
i2 = int(2*i0 - i1)


for data in data_list:
    axes[0].scatter(data.uy[i1] , (data.q_nonlocal[:,2] / data.q_local[:,2])[i1],marker=marker1,color=data.color,s=s,edgecolors='black',zorder=zorder)
    axes[0].scatter(data.uy[i2] , (data.q_nonlocal[:,2] / data.q_local[:,2])[i2],marker=marker2,color=data.color,s=s,edgecolors='black',zorder=zorder)

axes[-1].scatter(data.z_s[i1]/data.L , data.uy[i1] / data.M ,marker=marker1 , color="black",s=s ,zorder=zorder)
axes[-1].scatter(data.z_s[i2]/data.L , data.uy[i2] / data.M ,marker=marker2 , color="black",s=s ,zorder=zorder)



axes[-1].set_ylim([0,1.1])
axes[-1].plot(data.z_s / data.L , data.u[:,1] / data.M, color="black")
axes[-1].set_ylabel(r"$\Delta u_y/u_0$")
axes[-1].text(-2.9,0.85,"Flow profile")
axes[-1].text(-2.9,0.55,r"$N_u^0 = $"+str(M))
axes[-1].set_xlim([-3,3])
axes[-1].set_xlabel(r"$z/L$")



plt.tight_layout()
plt.savefig(filename_base+"_nonlocal_ettings_q_vs_u.png")
plt.show()