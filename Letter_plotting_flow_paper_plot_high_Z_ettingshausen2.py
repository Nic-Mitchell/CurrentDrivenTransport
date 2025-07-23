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



filename_base = "180725_ettings2"

save = True

r_hall0 = 1
N_K_s = [0.1,0.05,0.0001]
M_s = [0.0001,0.025,0.05]

data_list = [[0 for j in range(len(N_K_s))] for i in range(len(M_s))]

Z0 = 20
D_ov_L_plateau = 0

title=r"$Z=20$"

for i in range(len(M_s)):
    for j in range(len(N_K_s)):
        M = M_s[i]
        N_K = N_K_s[j]
        filename=filename_base+"_N_K_"+str(N_K)+"_hall_"+str(r_hall0)+"_M_"+str(M)+"_Z_"+str(Z0)
        with open(filename+".pkl",'rb') as file:
            data = dill.load(file)
            data.L = 1/N_K / np.sqrt(1+Z0)
            data_list[i][j] = data


colors_z = np.flip(colorlist.gen_color(cmap="winter",n=len(N_K_s)+2))[1:-1]
colors_y = np.flip(colorlist.gen_color(cmap="autumn",n=len(N_K_s)+2))[1:-1]


local_color_z = "purple"
local_color_y = "brown"


fig,axes=plt.subplots(len(M_s),1,figsize=(5,8),sharex=True)


for i in range(len(M_s)):
    data = data_list[i][2]
    axes[i].plot( data.z_s / data.L , np.sqrt(2)* data.q_nonlocal[:,2] / data.M , color="red",label=r"$N_K= 10^{-4}$")

    data = data_list[i][1]
    axes[i].plot( data.z_s / data.L , np.sqrt(2)* data.q_nonlocal[:,2] / data.M , color="green",label=r"$N_K= 0.05$")

    data = data_list[i][0]
    axes[i].plot( data.z_s / data.L , np.sqrt(2)* data.q_nonlocal[:,2] / data.M , color="blue",label=r"$N_K=0.1$")



    axes[i].set_ylabel(r"$q^u_{\times}/( N_u^0 q_0)$")
    axes[i].set_ylim([-0.8,0])

    axes[i].plot( data.z_s / data.L , np.sqrt(2)* data.q_local[:,2] / data.M , color="black",linestyle=":",label="Local analytic")
    
    axes[i].text(-2.9,-0.7,r"$N_u^0=$"+str(data.M))
    
axes[0].legend(loc="lower right")

axes[-1].set_xlim([-3,3])
axes[-1].set_xlabel(r"$z/L$")



axes[0].set_title(r"Nonlocal Ettingshausen heat flux, $Z=$"+str(Z0)+r", $\chi=1$")
plt.tight_layout()
plt.savefig(filename_base+"_nonlocal_ettings.png")
plt.show()