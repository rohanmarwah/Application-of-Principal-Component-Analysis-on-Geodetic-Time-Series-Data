#This model aims to output EOF modes and Principal component(PC) time series
#given GPS time-series data for crustal deformation analysis.
#The package used for EOF Analysis is Andrew Dawson's 'eofs' python package.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from eofs.standard import Eof
import os
import cartopy.crs as ccrs
import matplotlib.colors as colors


path1=r'C:\Users\DELL\Desktop\SOP'

up=pd.read_excel(os.path.join(path1,'location_conference_refined.xlsx'),usecols=['Up'])
up=up.to_numpy()
lons=pd.read_excel(os.path.join(path1,'location_conference.xlsx'),usecols=['long'])
lons=lons.to_numpy()
lats=pd.read_excel(os.path.join(path1,'location_conference.xlsx'),usecols=['lat'])
lats=lats.to_numpy()
lons1=pd.read_excel(os.path.join(path1,'location_conference_refined.xlsx'),usecols=['long'])
lons1=lons1.to_numpy()
lats1=pd.read_excel(os.path.join(path1,'location_conference_refined.xlsx'),usecols=['lat'])
lats1=lats1.to_numpy()

#Taking 1 month data for EOF analysis
yfinal1month= pd.read_excel(r'C:\Users\DELL\Desktop\SOP\sample3_conference.xlsx')
yfinal1month=yfinal1month.to_numpy()

#EOF analysis:
solver=Eof(yfinal1month)
pc1=solver.pcs(npcs=1)
eof1=solver.eofs(neofs=1)



#Plotting the temporal pattern:
pcplot=plt.plot(pc1)
plt.legend(pcplot,['First PC'])
plt.ylabel('Up (mm)')
plt.xlabel('Days since 1-11-2016')
plt.title('Temporal Pattern(U)', fontsize=16)
plt.show()


#plotting spacial pattern:
fig, ax1 = plt.subplots(dpi=400)
proj = ccrs.PlateCarree(central_longitude=0, globe=None)
ax1 = plt.axes(projection=proj)  
ax1.set_global()
ax1.coastlines(zorder=1)
ax1.plot(lons, lats, 'g^', ms=2,zorder=2)
ax1.set_extent([165, 180,-48, -33])
plt.title('Up', fontsize=16)

divnorm = colors.DivergingNorm(vmin=-0.8, vcenter=0, vmax=0.8)

ax1.tricontour(lons.squeeze(), lats.squeeze(), eof1.squeeze(), levels=10, linewidths=0, colors='k')
cntr1=ax1.tricontourf(lons.squeeze(), lats.squeeze(), eof1.squeeze(), levels=10, cmap="RdBu", norm=divnorm)
fig.colorbar(cntr1, ax=ax1)

ax1.plot(173.077, -42.757, 'r*', ms=10)
ax1.set_extent([165, 180,-48, -33])
ax1.quiver(lons1,lats1,0,up,color="b",width=0.003,scale=100,zorder=3)
ax1.text(177.6,-46.6,'10 mm',fontsize=5)
plt.show()


#percentage variation in each PC:
variance=solver.varianceFraction(neigs=3)
print(variance*100)




