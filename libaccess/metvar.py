#==========================================================================================================
# metvar.py - plots vertical profiles of meteorological variables 
#              over defined time intervals of a simulation
#
# Rick D. Saylor, July 2018
#
import os
from matplotlib import use
use("WXAgg")
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
from .pltutils import pltoutput, timekeys, get1Dvar, setstdfmts

# set colors
colors = ["gray", "peru", "brown", "red", "royalblue", "green", "violet", "magenta", "cyan", "olive"]

# set common figure formatting parameters
tfsize   = 18     # plot title font size
tyloc    = 1.02   # plot title y location
lfsize   = 14     # legend font size
yfsize   = 18     # y-axis title font size
ylabpad  = 10     # y-axis title padding
xfsize   = 18     # x-axis title font size
xlabpad  = 10     # x-axis title padding
tlmaj    =  6     # major tick length
tlmin    =  4     # minor tick length
tlbsize  = 17     # tick label font size
tlbpad   =  3     # tick label padding
lnwdth   = 1.5    # linewidth

###########################################################################################################
# plotprofs - create a figure for a meteorological variable
#             (Tair, Cair, H2O, qh, Pmb, ubar, or Kv)
#
def plotprofs(simname, varname, outtype, intdt, hmax, hc):
    """Create a vertical profile figure for a meterological variable    

    Args:
       simname  (str)   : ACCESS simulation name
       varname  (str)   : name of variable plotted
       outtype  (str)   : either 'pdf', 'png', or 'x11'
       intdt    (int)   : time step interval for plotting profiles
       hmax     (float) : height of the top of the domain (m)
       hc       (float) : height of the top of the canopy (m) 

    Returns:
       Nothing
    """
    # link varname with appropriate units and plot title strings
    if  (varname == "tk"):
        varunits = "K"
        vartitle = "Air Temperature"

    elif(varname == "cair"):
        varunits = "molecules cm$^{-3}$"
        vartitle = "Air Density"

    elif(varname == "h2o"):
        varunits = "molecules cm$^{-3}$"
        vartitle = "Water Vapor Concentration"

    elif(varname == "kv"):
        varunits = "cm$^{2}$ s$^{-1}$"
        vartitle = "Eddy Diffusivity"

    elif(varname == "pmb"):
        varunits = "millbar"
        vartitle = "Air Pressure"

    elif(varname == "qh"):
        varunits = "g kg$^{-1}$"
        vartitle = "Specific Humidity"

    elif(varname == "ubar"):
        varunits = "cm s$^{-1}$"
        vartitle = "Mean Wind Speed"

    else:
        print("Unknown met variable!")
        return 1

    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    # get data for var
    z, var = get1Dvar(simname, "met", varname)

    nts = var.shape[1]        # number of time slices 

    # create the plot
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))

    # plot one line for each time with intdt interval  
    ic = 0                    # color array index
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(var[:, m], z, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to domain height
    plt.ylim(-0.1, hmax)

    # set labels and title
    plt.xlabel(varunits, fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title(vartitle+" - "+simname, fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    # add legend
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.99, 0.10))

    # create output
    pltoutput(simname, varname, outtype)

    return
