#==========================================================================================================
# budget.py - plots vertical profiles of the budget rates for a defined species variable
#              for one defined time of a simulation
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
# plotprofs - create a one-panel figure for the budget rates of defined species variable
#
def plotprofs(simname, spcname, varunits, outtype, outfn, itime, zmax, xmax, hc):
    """Create a one-panel vertical profile figure of the budget rates for a defined species variable    
       at one defined time

    Args:
       simname  (str)   : ACCESS simulation name
       spcname  (str)   : name of species plotted
       varunits (str)   : units string for x-axis label
       outtype  (str)   : either 'pdf', 'png', or 'x11'
       outfn    (str)   : string for output file name
       itime    (int)   : simulation output time step number 
       zmax     (float) : height of the top of the plotted domain (m)
       xmax     (float) : maximum value on x-axis
       hc       (flost) : canopy height (m)

    Returns:
       Nothing
    """
    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    # get budget data for the species
    dirname = "budget"

    # constrained
    z, bad = get1Dvar(simname, dirname, spcname+"_bad")

    # chemistry
    z, bch = get1Dvar(simname, dirname, spcname+"_bch")

    # deposition
    z, bdp = get1Dvar(simname, dirname, spcname+"_bdp")

    # emission
    z, bem = get1Dvar(simname, dirname, spcname+"_bem")

    # vertical transport
    z, bvt = get1Dvar(simname, dirname, spcname+"_bvt")

    nts = len(hrs)        # number of time slices 

    # create the plot
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))

    # plot the vertical profiles of budget rates at the specified time
    plt.plot(bad[:, itime], z, color=colors[0], linestyle="-", linewidth=lnwdth, label="cns")
    plt.plot(bch[:, itime], z, color=colors[3], linestyle="-", linewidth=lnwdth, label="chm")
    plt.plot(bdp[:, itime], z, color=colors[4], linestyle="-", linewidth=lnwdth, label="dep")
    plt.plot(bem[:, itime], z, color=colors[5], linestyle="-", linewidth=lnwdth, label="ems")
    plt.plot(bvt[:, itime], z, color=colors[1], linestyle="-", linewidth=lnwdth, label="vtx")

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
    plt.xlabel(spcname+"-"+varunits, fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title(simname+" - "+hrs[itime], fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    # add legend
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.99, 0.10))

    # create output
    pltoutput(simname, outfn, outtype)

    return

