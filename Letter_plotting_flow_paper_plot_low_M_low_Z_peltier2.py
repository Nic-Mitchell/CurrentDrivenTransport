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



filename_base = "180725_peltier"

save = True

r_hall0 = 0
N_K_s = [0.1,0.0001]

data_list = [0 for j in range(len(N_K_s))]

Z0 = 1
M=0.0001
D_ov_L_plateau = 0

title=r"$N_u^0 = 1/10,000$, $Z=1$"


for j in range(len(N_K_s)):
    N_K = N_K_s[j]
    filename=filename_base+"_N_K_"+str(N_K)+"_hall_"+str(r_hall0)+"_M_"+str(M)+"_Z_"+str(Z0)
    with open(filename+".pkl",'rb') as file:
        data = dill.load(file)
        data.L =  1/N_K / np.sqrt(1+Z0)

        data_list[j] = data


colors_z = np.flip(colorlist.gen_color(cmap="winter",n=len(N_K_s)+2))[1:-1]
colors_y = np.flip(colorlist.gen_color(cmap="autumn",n=len(N_K_s)+2))[1:-1]


local_color_z = "purple"
local_color_y = "brown"


fig,axes=plt.subplots(2,1,height_ratios=(1,0.3),figsize=(5,4),sharex=True)


data_nl = data_list[0]
data_l = data_list[1]

axes[0].plot( data_l.z_s / data_l.L ,np.sqrt(2)*  data_l.q_nonlocal[:,1] / data_l.M , color="red",label=r"$N_K=$"+str(data_l.N_K))
axes[0].plot( data_nl.z_s / data_nl.L ,np.sqrt(2)*  data_nl.q_nonlocal[:,1] / data_nl.M , color="blue",label=r"$N_K=$"+str(data_nl.N_K))

axes[0].plot( data_l.z_s / data_l.L ,np.sqrt(2)*  data_l.q_local[:,1] / data_l.M , color="black",linestyle=":",label="Local analytic")

axes[0].legend()

axes[0].set_ylim(ymin=0)
axes[0].set_ylabel(r"$q^u_{\parallel}/(N_u^0 q_0)$")

axes[-1].set_xlim([-3,3])
axes[-1].set_xlabel(r"$z/L$")

axes[-1].set_ylim([0,1.1])
axes[-1].plot(data_l.z_s / data_l.L , data.u[:,1] / data.M, color="black")
axes[-1].set_ylabel(r"$\Delta u_y/u_0$")

axes[-1].text(-2.9,0.45,"Flow profile \n"+r"$N_u^0 = 10^{-4}$")


axes[0].set_title(r"Nonlocal Peltier heat flux, Z=1")
plt.tight_layout()
plt.savefig(filename_base+"_peltier.png")
plt.show()