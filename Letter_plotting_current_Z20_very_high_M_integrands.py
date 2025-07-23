
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


filename_base = "180725_ettings_integrands2"

save = True
title=r"Quasilocal heat flux integrands   $ \frac{1}{N_u} \frac{v_{th,e}}{q_0} \frac{dq_i}{dw} $"

r_hall0 =  1
N_K = 0.0001

Z0=20

D_ov_L_plateau = 0

M_s = [ 0.0001, 0.025 , 0.05]

M = 0.05
filename=filename_base+"_N_K_"+str(N_K)+"_hall_"+str(r_hall0)+"_M_"+str(M)+"_Z_"+str(Z0)
with open(filename+".pkl",'rb') as file:
    data = dill.load(file)

colors_z = np.flip(colorlist.gen_color(cmap="winter",n=len(M_s)+2))[1:-1]
colors_y = np.flip(colorlist.gen_color(cmap="autumn",n=len(M_s)+2))[1:-1]


local_color_z = "purple"
local_color_y = "brown"

 
n0 = 1

fig,axes=plt.subplots(1,1,figsize = (8,5))
fig.suptitle(title,y=0.95 )




def ab_from_lm(l,m):
    if np.abs(m) > l:
        print("ab_from_lm error")
        return None
    elif m >= 0:
        return l , l - m
    elif m<0:
        return l + m , l
    

liney_s = []
linez_s = []

xlim = [0,5.5]

axes.set_xlim(xlim)

axes.plot( xlim ,np.zeros_like(xlim),color="black"  )
axes.text( 0.1 , 1.2 , r"$Z=20$, $\chi=1$, $N_K = 10^{-4}$")
for j in range(len(M_s)):
    
    i = np.argmin(np.abs(data.uy - M_s[j]))
    #print(data.uy[i]/M_s[j])
        
    line1, = axes.plot( data.w_s / data.v_th_s[i]  ,np.sqrt(2)* data.q_y_nonlocal_integrand[i,:] / data.uy[i], color=colors_y[j] ,label=M_s[j] )        
    line2, = axes.plot( data.w_s / data.v_th_s[i]  ,np.sqrt(2)* data.q_z_nonlocal_integrand[i,:] / data.uy[i], color=colors_z[j] ,label=M_s[j] )        

    liney_s.append(line1)
    linez_s.append(line2)



i=0
line1,= axes.plot( data.w_s / data.v_th_s[i]  ,np.sqrt(2)* data.q_y_local_integrand[i,:] / data.uy[i], color=local_color_y ,linestyle=":" ,label="Local analytic" )        
line2,= axes.plot( data.w_s / data.v_th_s[i]  ,np.sqrt(2)* data.q_z_local_integrand[i,:] / data.uy[i], color=local_color_z ,linestyle=":" ,label="Local analytic" )        


liney_s.append(line1)
linez_s.append(line2)

legend_y = axes.legend(handles=liney_s , loc = "center right",title=r"$N_u$ ($q^u_\perp$ integrand)")
legend_z = axes.legend(handles=linez_s , loc = "upper right",title=r"$N_u$ ($q^u_\times$ integrand)")

axes.add_artist(legend_y)
axes.add_artist(legend_z)


plt.subplots_adjust(wspace=0.15, hspace=0.1)



axes.set_xlabel(r"$w/v_{th,e}$")


plt.savefig(filename_base+"_df.png",bbox_inches="tight")

plt.show()
        
        
        
        
        
        
        
        
        
        