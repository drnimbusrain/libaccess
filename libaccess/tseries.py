#=====================================================================================================
# tseries.py - plots general time series for variables over a simulation
#
# Rick D. Saylor, July 2018
#
import os
from matplotlib import use
use("WXAgg")
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
from datetime import datetime
from .pltutils import pltoutput, timekeys, get0Dvar, setstdfmts

# set figure formatting parameters
tfsize   = 18     # plot title font size
tyloc    = 1.02   # title y location
lfszsm   = 10     # legend font size small
lfszlg   = 14     # legend font size large
yfsize   = 18     # y-axis title font size
ylabpad  = 10     # y-axis title padding
xfsize   = 18     # x-axis title font size
xlabpad  = 10     # x-axis title padding
tlmaj    = 6      # major tick length
tlmin    = 4      # minor tick length
tlbsize  = 17     # tick label font size
tlbpad   = 3      # tick label padding
lnwdth   = 1.5    # linewidth
msize    = 8      # marker size


#######################################################################################################
# plottsm - create a time series plot for multiple 0D variables
#
def plottsm(simname, dirname, varnames, varlabels, varunits, plttitle, plttype, scolors, outtype, outfn):
    """Create a time series plot for multiple 0D (time only) variables from an
       ACCESS simulation

    Args:
       simname   (str)      : ACCESS simulation name
       dirname   (str)      : simulation output directory
       varnames  list(str)  : names of variables plotted
       varlabels list(str)  : labels for variables
       varunits  (str)      : units for variable
       plttitle  (str)      : title for the plot
       plttype   (str)      : type of plot, either "marker" or "line"
       scolor    list(str)  : color names to use for markers or line
       outtype   (str)      : either 'pdf', 'png', or 'x11'
       outfn     (str)      : string for output file 

    Returns:
       Nothing
    """
    # read elapsed hour/datetime key file
    dts, hrs = timekeys(simname)

    # get variable values to plot
    varx = {}
    vlbs = {}
    clrs = {}
    for varname, varlabel, scolor in zip(varnames, varlabels, scolors):
        dat = get0Dvar(simname, dirname, varname) 
        varx[varname] = dat
        clrs[varname] = scolor
        vlbs[varname] = varlabel

    nts = len(dts)

    # create the plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    # line or marker plot?
    for varname in varnames:
        if  (plttype == "marker"):
            plt.plot(dts, varx[varname], color=clrs[varname], linestyle="None", marker="o", ms=msize, label=vlbs[varname])
        else:
            plt.plot(dts, varx[varname], color=clrs[varname], linestyle="-", linewidth=lnwdth, label=vlbs[varname])

    # take care of time formatting on x-axis
    days = mdates.DayLocator()
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    if (nts > 48):
        hours = mdates.HourLocator(byhour=range(24), interval=4)
    else:
        hours = mdates.HourLocator(byhour=range(24), interval=1)
    ax.xaxis.set_minor_locator(hours)

    # set standard formatting
    setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

    # set y-axis label
    plt.ylabel(varunits, fontsize=yfsize, labelpad=ylabpad)

    # add plot title
    plt.title(plttitle+" - "+simname, fontsize=tfsize, y=tyloc)

    # add legend
    if (len(varnames) > 1):
        plt.legend(loc=4, fontsize=lfszlg, bbox_to_anchor=(0.99, 0.70))

    # create output
    pltoutput(simname, outfn, outtype)

    return
