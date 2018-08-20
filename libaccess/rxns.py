#==========================================================================================================
# rxns.py - plots vertical profiles of reaction rate coefficients or overall rates for a specified 
#            reaction over defined time intervals of a simulation
#
# Rick D. Saylor, August 2018
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
# plotprofs - create a one-panel figure for a defined species variable
#
def plotprofs(simname, dirname, rxnnum, outtype, intdt, zmax, xmax, hc):
    """Create a one-panel vertical profile figure for a defined species variable    

    Args:
       simname  (str)   : ACCESS simulation name
       dirname  (str)   : simulation output directory, either "rates" or "ks"
       rxnnum   (int)   : reaction number to be plotted 
       outtype  (str)   : either 'pdf', 'png', or 'x11'
       intdt    (int)   : time step interval for plotting profiles
       zmax     (float) : height of the top of the plotted domain (m)
       xmax     (float) : maximum value on x-axis
       hc       (flost) : canopy height (m)

    Returns:
       Nothing
    """
    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    # get data for the specified reaction
    srxnnum = "rxn"+str(rxnnum).zfill(5)
    z, var = get1Dvar(simname, dirname, srxnnum)

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

    # limit to specified height
    nz = len(z)
    if (zmax == -1.):
        zmax = z[nz-1]
    plt.ylim(-0.1, zmax)
    if (xmax != -1.):
        plt.xlim(-0.1, xmax)

    # draw line showing canopy height, if applicable
    if (zmax > hc):
        ahc = [hc, hc]
        xbnds = list(ax.get_xlim())
        plt.plot(xbnds, ahc, color='0.25', linestyle='--', linewidth=lnwdth)

    # set labels and title
    if (dirname == "rates"):
        varunits = "(molec cm$^{-3}$ s$^{-1}$)"
        vartitle = "Rxn Rate: "+str(rxnnum) 
        outfn = "rates"
    else:
        varunits = "(molec-cm-s units)"
        vartitle = "Rate Coef: "+str(rxnnum) 
        outfn = "ks"

    plt.xlabel(spcname+"-"+varunits, fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title(vartitle+" - "+simname, fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    # add legend
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.99, 0.10))

    # create output
    pltoutput(simname, outfn, outtype)

    return
