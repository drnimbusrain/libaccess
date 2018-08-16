#=======================================================================================================
# canopy.py - plots vertical profiles of canopy physics variables over
#             a simulation for sun/shade/weighted variables
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

########################################################################################################
# plotall3 - create a figure for sunlit, shaded and weighted canopy variable
#            (PPFD, NIR, Rabs, Tleaf, gs, or Anet)
#
def plotall3(simname, varname, outtype, intdt, hmax, hc):
    """Create a 3 panel figure for a canopy variable for the sunlit, shaded
       and weighted fractions

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
    if  (varname == "ppfd"):
        varunits = "$\mu$mol m$^{-2}$ s$^{-1}$"
        vartitle = "PPFD"

    elif(varname == "nir"):
        varunits = "W m$^{-2}$"
        vartitle = "NIR"

    elif(varname == "rabs"):
        varunits = "W m$^{-2}$"
        vartitle = "R$_{abs}$"

    elif(varname == "tl"):
        varunits = "K"
        vartitle = "T$_{leaf}$"

    elif(varname == "gs"):
        varunits = "mol m$^{-2}$ s$^{-1}$"
        vartitle = "g$_{s}$"

    elif(varname == "anet"):
        varunits = "$\mu$mol m$^{-2}$ s$^{-1}$"
        vartitle = "A$_{net}$"

    else: 
        print("Unknown canopy variable!")
        return 1

    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    # get data for sunlit var
    z, varsun = get1Dvar(simname, "canopy", varname+"sun")

    # get data for shaded var
    z, varshd = get1Dvar(simname, "canopy", varname+"shd")

    # get data for weighted var
    z, varwgt = get1Dvar(simname, "canopy", varname+"wgt")

    # create the plot 
    fig = plt.figure(figsize=(16, 10))

    nts = varsun.shape[1]      # number of time slices

    ###################
    # sunlit var plot
    ###################
    ax = plt.subplot(1, 3, 1)
    ic = 0                     # color array index

    # draw a vertical profile for each intdt time
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(varsun[:, m], z, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to canopy height
    plt.ylim(-0.1, hc)

    # set labels and title
    plt.xlabel(varunits, fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title("sunlit", fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    ###################
    # shaded var plot
    ###################
    ax = plt.subplot(1, 3, 2)
    ic = 0                     # color array index

    # draw a vertical profile for each intdt time
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(varshd[:, m], z, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to canopy height
    plt.ylim(-0.1, hc)

    # set labels and title
    plt.xlabel(varunits, fontsize=xfsize, labelpad=xlabpad)
    plt.title("shaded", fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    ###################
    # weighted var plot
    ###################
    ax = plt.subplot(1, 3, 3)
    ic = 0                     # color array index

    # draw a vertical profile for each intdt time
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(varwgt[:, m], z, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to canopy height
    plt.ylim(-0.1, hc)

    # set labels and title
    plt.xlabel(varunits, fontsize=xfsize, labelpad=xlabpad)
    plt.title("weighted", fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    # add the legend (only on the last plot)
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.55, 0.01))

    # add super title
    plt.suptitle(simname+"-"+vartitle, fontsize=tfsize, x=0.5, y=0.97)

    # create output
    pltoutput(simname, varname, outtype)

    return

########################################################################################################
# plotsun - create a figure for sunlit & shaded canopy fractions
#
def plotsun(simname, outtype, intdt, hmax, hc):
    """Create a 2 panel figure for the sunlit and shaded canopy fractions

    Args:
       simname  (str)  : ACCESS simulation name
       outtype  (str)  : either 'pdf', 'png', or 'x11'
       intdt    (int)  : time step interval for plotting profiles
       hmax     (float) : height of the top of the domain (m)
       hc       (float) : height of the top of the canopy (m)

    Returns:
       Nothing
    """
    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    # get data for sunlit fraction
    z, fsun = get1Dvar(simname, "canopy", "fsun")

    # get data for shaded fraction
    z, fshd = get1Dvar(simname, "canopy", "fshd")

    # create the plot
    fig = plt.figure(figsize=(12, 10))

    nts = fsun.shape[1]      # number of time slices

    #######################
    # sunlit fraction plot
    #######################
    ax = plt.subplot(1, 2, 1)
    ic = 0    # color array index

    # draw a vertical profile for each intdt time
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(fsun[:, m], z, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to canopy height
    plt.ylim(-0.1, hc)

    # set labels and title
    plt.xlabel("fraction", fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title("sunlit", fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    #######################
    # shaded fraction plot
    #######################
    ax = plt.subplot(1, 2, 2)
    ic = 0    # color array index

    # draw a vertical profile for each intdt time
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(fshd[:, m], z, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to canopy height
    plt.ylim(-0.1, hc)

    # set labels and title
    plt.xlabel("fraction", fontsize=xfsize, labelpad=xlabpad)
    plt.title("shaded", fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    # add the legend (on the last plot only)
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.55, 0.01))

    # add the super title
    plt.suptitle(simname+"-Sun/Shade", fontsize=tfsize, x=0.5, y=0.99)
    
    # create output
    pltoutput(simname, "sunshd", outtype)

    return

########################################################################################################
# plotlw - create a figure for upwelling and downwelling long-wave radiation
#
def plotlw(simname, outtype, intdt, hmax, hc):
    """Create a 2 panel figure for the upwelling and downwelling longwave radiation

    Args:
       simname  (str)  : ACCESS simulation name
       outtype  (str)  : either 'pdf', 'png', or 'x11'
       intdt    (int)  : time step interval for plotting profiles
       hmax     (float) : height of the top of the domain (m)
       hc       (float) : height of the top of the canopy (m)

    Returns:
       Nothing
    """
    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    # get data for LW up
    z, lwup = get1Dvar(simname, "canopy", "lwup")

    # get data for LW down
    z, lwdn = get1Dvar(simname, "canopy", "lwdn")

    # create the plot
    fig = plt.figure(figsize=(12, 10))

    nts = lwdn.shape[1]    # number of time slices

    ################
    # LW up plot
    ################
    ax = plt.subplot(1, 2, 1)
    ic = 0                 # color array index

    # draw a vertical profile for each intdt time
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(lwup[:, m], z, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to canopy height
    plt.ylim(-0.1, hc)

    # set labels and title
    swm2 = "W m$^{-2}$"
    plt.xlabel(swm2, fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title("LW Up", fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    ################
    # LW down plot
    ################
    ax = plt.subplot(1, 2, 2)
    ic = 0    # color array index

    # draw a vertical profile for each intdt time
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(lwdn[:, m], z, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to canopy height
    plt.ylim(-0.1, hc)

    # set labels and title
    plt.xlabel(swm2, fontsize=xfsize, labelpad=xlabpad)
    plt.title("LW Down", fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    # add the legend (only on the last plot)
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.55, 0.01))

    # add the super title
    plt.suptitle(simname, fontsize=tfsize, x=0.5, y=0.99)
    
    # create output
    pltoutput(simname, "lw", outtype)

    return 0
