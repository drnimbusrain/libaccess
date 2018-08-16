#==========================================================================================================
# genvar.py - plots vertical profiles of a defined variable
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
# plotprofs1 - create a one-panel figure for a defined variable
#
def plotprofs1(simname, dirname, varname, varunits, vartitle, outtype, outfn, intdt, htop):
    """Create a one-panel vertical profile figure for a defined variable    

    Args:
       simname  (str)   : ACCESS simulation name
       dirname  (str)   : simulation output directory
       varname  (str)   : name of variable plotted
       varunits (str)   : units string for x-axis label
       vartitle (str)   : plot title
       outtype  (str)   : either 'pdf', 'png', or 'x11'
       outfn    (str)   : string for output file name
       intdt    (int)   : time step interval for plotting profiles
       htop     (float) : height of the top of the plotted domain (m)

    Returns:
       Nothing
    """
    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    # get data for var
    z, var = get1Dvar(simname, dirname, varname)

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

    # limit to plotted domain height
    plt.ylim(-0.1, htop)

    # set labels and title
    plt.xlabel(varunits, fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title(vartitle+" - "+simname, fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    # add legend
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.99, 0.10))

    # create output
    pltoutput(simname, outfn, outtype)

    return


###########################################################################################################
# plotprofs2 - create a two-panel figure for defined variables
#
def plotprofs2(simname, dirnames, varnames, varunits, vartitles, outtype, outfn, intdt, htop):
    """Create a two-panel vertical profile figure for defined variables   

    Args:
       simname    (str)    : ACCESS simulation name
       dirnames  list(str) : simulation output directorys
       varnames  list(str) : name of variables plotted
       varunits  list(str) : units strings for x-axis labels
       vartitles list(str) : plot titles
       outtype    (str)    : either 'pdf', 'png', or 'x11'
       outfn      (str)    : string for output file name
       intdt      (int)    : time step interval for plotting profiles
       htop      (float)   : height of the top of the plotted domains (m)

    Returns:
       Nothing
    """
    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    nts = len(hrs)        # number of time slices 

    # set size of figure area
    fig = plt.figure(figsize=(12, 10))

    # get data for first var
    z0, var0 = get1Dvar(simname, dirnames[0], varnames[0])

    # plot first var
    ax0 = plt.subplot(1, 2, 1)

    # plot one line for each time with intdt interval  
    ic = 0                    # color array index
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(var0[:, m], z0, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to plotted domain height
    plt.ylim(-0.1, htop)

    # set labels and title
    plt.xlabel(varunits[0], fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title(vartitles[0], fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax0, tlmaj, tlmin, tlbsize, tlbpad)

    # get data for second var
    z1, var1 = get1Dvar(simname, dirnames[1], varnames[1])

    # plot second var
    ax1 = plt.subplot(1, 2, 2)

    # plot one line for each time with intdt interval  
    ic = 0                    # color array index
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(var1[:, m], z1, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to plotted domain height
    plt.ylim(-0.1, htop)

    # set labels and title
    plt.xlabel(varunits[1], fontsize=xfsize, labelpad=xlabpad)
    plt.title(vartitles[1], fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax1, tlmaj, tlmin, tlbsize, tlbpad)

    # add legend
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.99, 0.10))

    # add simname to the top
    plt.suptitle(simname, fontsize=tfsize, x=0.5, y=0.97)

    # create output
    pltoutput(simname, outfn, outtype)

    return

###########################################################################################################
# plotprofs3 - create a three-panel figure for defined variables
#
def plotprofs3(simname, dirnames, varnames, varunits, vartitles, outtype, outfn, intdt, htop):
    """Create a three-panel vertical profile figure for defined variables   

    Args:
       simname    (str)    : ACCESS simulation name
       dirnames  list(str) : simulation output directorys
       varnames  list(str) : name of variables plotted
       varunits  list(str) : units strings for x-axis labels
       vartitles list(str) : plot titles
       outtype    (str)    : either 'pdf', 'png', or 'x11'
       outfn      (str)    : string for output file name
       intdt      (int)    : time step interval for plotting profiles
       htop      (float)   : height of the top of the plotted domains (m)

    Returns:
       Nothing
    """
    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    nts = len(hrs)        # number of time slices 

    # set size of figure area
    fig = plt.figure(figsize=(16, 10))

    # get data for first var
    z0, var0 = get1Dvar(simname, dirnames[0], varnames[0])

    # plot first var
    ax0 = plt.subplot(1, 3, 1)

    # plot one line for each time with intdt interval  
    ic = 0                    # color array index
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(var0[:, m], z0, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to plotted domain height
    plt.ylim(-0.1, htop)

    # set labels and title
    plt.xlabel(varunits[0], fontsize=xfsize, labelpad=xlabpad)
    plt.ylabel("z (m)", fontsize=yfsize, labelpad=ylabpad)
    plt.title(vartitles[0], fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax0, tlmaj, tlmin, tlbsize, tlbpad)

    # get data for second var
    z1, var1 = get1Dvar(simname, dirnames[1], varnames[1])

    # plot second var
    ax1 = plt.subplot(1, 3, 2)

    # plot one line for each time with intdt interval  
    ic = 0                    # color array index
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(var1[:, m], z1, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to plotted domain height
    plt.ylim(-0.1, htop)

    # set labels and title
    plt.xlabel(varunits[1], fontsize=xfsize, labelpad=xlabpad)
    plt.title(vartitles[1], fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax1, tlmaj, tlmin, tlbsize, tlbpad)

    # get data for third var
    z2, var2 = get1Dvar(simname, dirnames[2], varnames[2])

    # plot third var
    ax2 = plt.subplot(1, 3, 3)

    # plot one line for each time with intdt interval  
    ic = 0                    # color array index
    for m in range(nts):
        if ( (m % intdt) == 0):
            labstr = hrs[m]
            plt.plot(var2[:, m], z2, color=colors[ic], linestyle="-", linewidth=lnwdth, label=labstr)
            ic+=1
            if (ic > len(colors)-1):    # cycle back through the colors
                ic = 0

    # limit to plotted domain height
    plt.ylim(-0.1, htop)

    # set labels and title
    plt.xlabel(varunits[2], fontsize=xfsize, labelpad=xlabpad)
    plt.title(vartitles[2], fontsize=tfsize, y=tyloc)

    # set standard formatting
    setstdfmts(ax2, tlmaj, tlmin, tlbsize, tlbpad)

    # add legend
    plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.99, 0.10))

    # add simname to the top
    plt.suptitle(simname, fontsize=tfsize, x=0.5, y=0.97)

    # create output
    pltoutput(simname, outfn, outtype)

    return
