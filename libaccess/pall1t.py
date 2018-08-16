#==================================================================================================
# pall1t.py - plot canopy profiles for one time
#
# Rick D. Saylor, July 2018 (rewrite)
#
import os
from matplotlib import use
use("WXAgg")
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from matplotlib import rcParams
from .pltutils import pltoutput, timekeys, get1Dvar, setstdfmts

# colors
colors = ["gray", "peru", "brown", "red", "royalblue", "green", "violet", "magenta", "cyan", "olive"]

# formatting
tfsize = 22    # plot title font size
tyloc  = 0.95  # title y location
lfsize = 14    # legend font size
yfsize = 16    # y-axis title font size
xfsize = 13    # x-axis title font size
tlmaj  = 6     # major tick length
tlmin  = 4     # minor tick length
tlbsize= 10    # tick label size
msize  = 6     # marker size
lnwdth = 2     # linewidth
xtpad = 15     # x title padding
ytpad = 0      # y title padding
tlbpad = 0     # tick label padding

def pltall1t(simname, outtype, tslice):
   """Create a seven panel figure showing all canopy profiles for
      one time slice of an ACCESS simulation

   Args:
      simname  (str)   : ACCESS simulation name
      outtype  (str)   : either 'pdf', 'png', or 'x11'
      tslice   (int)   : time slice from the simulation (t0 = 1)

   Returns:
      Nothing
   """
   rcParams["mathtext.default"] = "regular"

   dirout = os.getcwd()+"/"

   # read elapsed hour/datetime key file
   dts, hrs = timekeys(simname)
   datetimes = []
   for dt in dts:
       datetimes.append(datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")) 
   
   # Tair
   z, atair = get1Dvar(simname, "met", "tk")
   tair     = atair[:, tslice-1] - 273.15           # convert from K to C

   # Ubar
   z, aubar = get1Dvar(simname, "met", "ubar")
   ubar     = aubar[:, tslice-1]*0.01               # cm/s to m/s

   # fsun
   z, afsun = get1Dvar(simname, "canopy", "fsun")
   fsun     = afsun[:, tslice-1]

   # fshd
   z, afshd = get1Dvar(simname, "canopy", "fshd")
   fshd     = afshd[:, tslice-1]

   # ppfdsun
   z, appfdsun = get1Dvar(simname, "canopy", "ppfdsun")
   ppfdsun     = appfdsun[:, tslice-1]

   # ppfdshd
   z, appfdshd = get1Dvar(simname, "canopy", "ppfdshd")
   ppfdshd     = appfdshd[:, tslice-1]

   # nirsun
   z, anirsun = get1Dvar(simname, "canopy", "nirsun")
   nirsun     = anirsun[:, tslice-1]

   # nirshd
   z, anirshd = get1Dvar(simname, "canopy", "nirshd")
   nirshd     = anirshd[:, tslice-1]

   # lwup
   z, alwup = get1Dvar(simname, "canopy", "lwup")
   lwup     = alwup[:, tslice-1]

   # lwdn
   z, alwdn = get1Dvar(simname, "canopy", "lwdn")
   lwdn     = alwdn[:, tslice-1]

   # rtsun
   z, artsun = get1Dvar(simname, "canopy", "rtsun")
   rtsun     = artsun[:, tslice-1]

   # rtshd
   z, artshd = get1Dvar(simname, "canopy", "rtshd")
   rtshd     = artshd[:, tslice-1]

   # rasun
   z, arasun = get1Dvar(simname, "canopy", "rabssun")
   rasun     = arasun[:, tslice-1]

   # rashd
   z, arashd = get1Dvar(simname, "canopy", "rabsshd")
   rashd     = arashd[:, tslice-1]

   # rssun
   z, arssun = get1Dvar(simname, "canopy", "rssun")
   rssun     = arssun[:, tslice-1]

   # rsshd
   z, arsshd = get1Dvar(simname, "canopy", "rsshd")
   rsshd     = arsshd[:, tslice-1]

   # tlsun
   z, atlsun = get1Dvar(simname, "canopy", "tlsun")
   tlsun     = atlsun[:, tslice-1] - 273.15     # convert from K to C

   # tlshd
   z, atlshd = get1Dvar(simname, "canopy", "tlshd")
   tlshd     = atlshd[:, tslice-1] - 273.15     # convert from K to C

   # gssun
   z, agssun = get1Dvar(simname, "canopy", "gssun")
   gssun     = agssun[:, tslice-1]

   # gsshd
   z, agsshd = get1Dvar(simname, "canopy", "gsshd")
   gsshd     = agsshd[:, tslice-1]

   # ansun
   z, aansun = get1Dvar(simname, "canopy", "anetsun")
   ansun     = aansun[:, tslice-1]

   # anshd
   z, aanshd = get1Dvar(simname, "canopy", "anetshd")
   anshd     = aanshd[:, tslice-1]

   # lai, clai
   flai = open(dirout+simname+"/canopy/laiprof.dat")
   lines = flai.readlines()
   flai.close()
   lines = lines[1:]   # skip the header line
   nz = len(z)
   lai  = np.zeros(nz)
   clai = np.zeros(nz)
   k = 0
   for line in lines:
      data = line.split()
      lai[k] = float(data[1])
      clai[k] = float(data[2])
      k+=1

   # create the plots
   fig = plt.figure(figsize=(16,12))

   # LAI
   ax = fig.add_subplot(2,5,1)
   ax.plot(lai, z, color=colors[0], linestyle="None", marker="o", markersize=msize, label="LAI")

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("LAI, m$^2$ m$^{-2}$", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.65,0.85))

   # sun/shade fractions
   ax = fig.add_subplot(2,5,2)
   ax.plot(fsun, z, color=colors[1], linestyle="None", marker="o", markersize=msize, label="f$_{sun}$")
   ax.plot(fshd, z, color=colors[2], linestyle="None", marker="o", markersize=msize, label="f$_{shd}$")

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("fraction", fontsize=xfsize, labelpad=xtpad-5)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.85,0.75))

   # LW up & dn
   ax = fig.add_subplot(2,5,3)
   ax.plot(lwup, z, color=colors[3], linestyle="None", marker="s", markersize=msize, label="LW$_{up}$")
   ax.plot(lwdn, z, color=colors[4], linestyle="None", marker="s", markersize=msize, label="LW$_{dn}$")

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("W m$^{-2}$", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.65,0.75))

   # Rabs sun & shade
   ax = fig.add_subplot(2,5,4)
   ax.plot(rasun, z, color=colors[1], linestyle="None", marker="s", markersize=msize, label="R$_{a,sun}$")
   ax.plot(rashd, z, color=colors[2], linestyle="None", marker="s", markersize=msize, label="R$_{a,shd}$")
   radif = rasun+rashd
   sumra=0.0
   nra=0
   for i in range(nz):
      if (clai[i] > 0.0):
         sumra+=0.5*radif[i]
         nra+=1
   if (nra > 0):
      ramean = sumra/float(nra)
   else:
      ramean = 0.0
   drx=0.1*ramean
   drx = max(50.0, drx)
   plt.xlim(xmax=ramean+drx, xmin=ramean-drx)

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("W m$^{-2}$", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.95,0.75))

   # Tair, Tleaf_sun, Tleaf_shd
   ax = fig.add_subplot(2,5,5)
   ax.plot(tlsun, z, color=colors[1], linestyle="None", marker="o", markersize=msize, label="T$_{l,sun}$")
   ax.plot(tlshd, z, color=colors[2], linestyle="None", marker="o", markersize=msize, label="T$_{l,shd}$")
   ax.plot(tair, z, color=colors[3], linestyle="None", marker="o", markersize=msize, label="T$_{air}$")
   tamin = min(tair)
   tamax = max(tair)
   tdif = tlsun-tlshd
   dtx = max(abs(tdif))
   dtx = max(5.0, dtx)
   plt.xlim(xmax=tamax+dtx, xmin=tamin-dtx)

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("$^o$C", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.55,0.70))

   # Mean wind speed
   ax = fig.add_subplot(2,5,6)
   ax.plot(ubar, z, color=colors[0], linestyle="None", marker="o", markersize=msize, label="u")

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("m s$^{-1}$", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.60,0.80))

   # Stomatal conductance, sun & shade
   ax = fig.add_subplot(2,5,7)
   ax.plot(gssun, z, color=colors[1], linestyle="None", marker="o", markersize=msize, label="g$_{s,sun}$")
   ax.plot(gsshd, z, color=colors[2], linestyle="None", marker="o", markersize=msize, label="g$_{s,shd}$")

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("mol m$^{-2}$ s$^{-1}$", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.95,0.75))

   # Stomatal resistance, sun & shade
   ax = fig.add_subplot(2,5,8)
   ax.plot(rssun, z, color=colors[1], linestyle="None", marker="o", markersize=msize, label="r$_{s,sun}$")
   ax.plot(rsshd, z, color=colors[2], linestyle="None", marker="o", markersize=msize, label="r$_{s,shd}$")
   xmin, xmax = ax.get_xlim()
   plt.xticks(np.arange(xmin, xmax+1, 1000.))

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("s m$^{-1}$", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.95,0.75))

   # Net photosynthetic assimilation rate, sun & shade
   ax = fig.add_subplot(2,5,9)
   ax.plot(ansun, z, color=colors[1], linestyle="None", marker="o", markersize=msize, label="A$_{n,sun}$")
   ax.plot(anshd, z, color=colors[2], linestyle="None", marker="o", markersize=msize, label="A$_{n,shd}$")

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("$\mu$mol m$^{-2}$ s$^{-1}$", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize, bbox_to_anchor=(0.95,0.75))

   # PPFD and NIR, sun & shade
   ax = fig.add_subplot(2,5,10)
   ax.plot(ppfdsun, z, color=colors[1], linestyle="None", marker="s", markersize=msize, label="PPFD$_{sun}$")
   ax.plot(ppfdshd, z, color=colors[2], linestyle="None", marker="s", markersize=msize, label="PPFD$_{shd}$")
   ax.plot(nirsun, z, color=colors[3], linestyle="None", marker="s", markersize=msize, label="NIR$_{sun}$")
   ax.plot(nirshd, z, color=colors[4], linestyle="None", marker="s", markersize=msize, label="NIR$_{shd}$")

   setstdfmts(ax, tlmaj, tlmin, tlbsize, tlbpad)

   plt.xlabel("W m$^{-2}$", fontsize=xfsize, labelpad=xtpad)
   plt.legend(loc=4, fontsize=lfsize-1, bbox_to_anchor=(1.05,0.00))

   plt.suptitle(simname+" - "+datetimes[tslice], fontsize=tfsize, y=tyloc) 

   # create output 
   pltoutput(simname, "pall1t", outtype)

   return
