#==================================================================================================
# pltutils.py - plotting utilities
#
# Rick D. Saylor, July 2018
#
import os
from matplotlib import use
use("WXAgg")
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
from datetime import datetime

def setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad):
    """Set standard formatting for plots

    Uses the seaborn module, adds a grid to the plot, and formats ticks

    Args:
       ax (obj)      : axes object from figure creation
       tlmaj (int)   : major tick length
       tlmin (int)   : minor tick length
       tlbsize (int) : size of tick labels
       tlbpad (int)  : padding for tick labels

    Returns:
       Nothing

    """
    # seaborn settings
    sns.set_context("talk")
    sns.set_style("ticks")

    # pretty grid
    plt.grid(b=True, which="major", color="gray", linewidth=1.0, alpha=0.50)
    plt.grid(b=True, which="minor", color="gray", linewidth=0.5, alpha=0.25)

    # pretty ticks
    plt.minorticks_on()
    ax.tick_params(which="both", direction="out")
    ax.tick_params(which="major", length=tlmaj)
    ax.tick_params(which="minor", length=tlmin)
    ax.tick_params(which="both", labelsize=tlbsize, pad=tlbpad)

    return

def pltoutput(simname, varname, outtype):
    """Output the figure to the screen or to a file, as specified

    Args:
       simname (str)  : ACCESS simulation name
       varname (str)  : name of variable plotted
       outtype (str)  : either 'pdf', 'png', or 'x11'

    Returns:
       Nothing
    """
    # output file name for hardcopy
    ofname = os.getcwd()+"/img/"+simname+"_"+varname

    if   (outtype == "pdf"):
        plt.savefig(ofname+".pdf")

    elif (outtype == "png"):
        plt.savefig(ofname+".png")

    else:
        plt.show()

    return

def timekeys(simname):
    """Reads timekey file from ACCESS simulation and returns datetimes
       and hour strings

    Args:
       simname (str)            : ACCESS simulation name

    Returns:
       dts (list of datetimes)  : datetimes corresponding to simulation output times
       hrs (list of str)        : strings corresponding to the hour (24-hr clock)
    """
    # read elapsed hour/datetime key file
    fndt = os.getcwd()+"/"+simname+"/ACCESS_timekey.dat"
    fhdt = open(fndt)
    lines = fhdt.readlines()
    fhdt.close()
    lines = lines[1:]          # ignore the header line

    dts = []
    hrs = []
    for line in lines:
        data = line.split()
        date = data[1]
        time = data[2]
        dt   = date+" "+time
        dts.append(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S"))
        hrs.append(time[0:5])

    return dts, hrs

def getspunits(simname):
    """Reads species units key file which defines species output as ppbv

    Args:
       simname (str)            : ACCESS simulation name

    Returns:
       ppbvs (list of str)      : species strings output as ppbv
    """
    # read species units key file
    fnsp = os.getcwd()+"/"+simname+"/ACCESS_ppbv.dat"
    fhsp = open(fnsp)
    lines = fhsp.readlines()
    fhsp.close()
    lines = lines[1:]          # ignore the header line
   
    pppbs = []
    for line in lines:
        data = line.split()
        ppbvs.append(data[1])

    return ppbvs

def get1Dvar(simname, dirname, varname):
    """Reads a height-time output file from an ACCESS simulation and
       returns the data

    Args:
       simname (str)        : ACCESS simulation name
       dirname (str)        : name of the simulation output directory
       varname (str)        : variable name

    Returns:
       z (numpy 1D array)   : domain vertical levels (m)
       var (numpy 2D array) : data corresponding to varname
    """ 
    fnvar = os.getcwd()+"/"+simname+"/"+dirname+"/"+varname+".dat"
    fhvar = open(fnvar)
    lines = fhvar.readlines()
    fhvar.close()

    nts   = len(lines[0].split()) - 1    # number of time slices   
    lines = lines[1:]                    # ignore the header line
    nz    = len(lines)                   # number of vertical heights

    z   = np.zeros(nz)                   # vertical heights (m)
    var = np.zeros( (nz, nts) )          # the data

    k = 0
    for line in lines:
        data = line.split()
        z[k] = float(data[0])            # vertical height for this line
        m = 0
        data = data[1:]                  # now, only the data
        for value in data:
            var[k, m] = float(value)     # get data for each time
            m+=1
        k+=1 

    return z, var

def get0Dvar(simname, dirname, varname):
    """Reads a time only output file from an ACCESS simulation and
       returns the data

    Args:
       simname (str)         : ACCESS simulation name
       dirname (str)         : name of the simulation output directory
       varname (str)         : variable name

    Returns:
       var (numpy 1D array)  : data corresponding to varname
    """
    fnvar = os.getcwd()+"/"+simname+"/"+dirname+"/"+varname+".dat"
    fhvar = open(fnvar)
    lines = fhvar.readlines()
    fhvar.close()

    lines = lines[1:]                    # ignore the header line
    nts   = len(lines)                   # number of time slices
    var = np.zeros(nts)                  # the data

    i = 0
    for line in lines:
        data = line.split()
        var[i] = float(data[1])          # get data for each time
        i+=1 

    return var

