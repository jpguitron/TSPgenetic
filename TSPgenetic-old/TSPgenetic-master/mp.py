import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt




class Mp:
    
    def __init__(self):

        fname = './gadm36_MEX_shp/gadm36_MEX_0.shp'
        adm1_shapes = list(shpreader.Reader(fname).geometries())
        self.ax = plt.axes(projection=ccrs.PlateCarree())

        plt.title('Mexico')
        self.ax.coastlines(resolution='10m')

        self.ax.add_geometries(adm1_shapes, ccrs.PlateCarree(), edgecolor='black', facecolor='gray', alpha=0.5)
        self.ax.set_extent([-120, -80, 10, 35], ccrs.PlateCarree())


        
        

    def generateLines(self,lines):
        
        for i in range(len(lines)-1):
            x=[lines[i].lon, lines[i+1].lon]
            y=[lines[i].lat, lines[i+1].lat]
            self.ax.plot(x, y, transform=ccrs.PlateCarree(), color='red', lw=2)
        
        x=[lines[0].lon, lines[len(lines)-1].lon]
        y=[lines[0].lat, lines[len(lines)-1].lat]
        self.ax.plot(x, y, transform=ccrs.PlateCarree(), color='red', lw=2)

    def clearMap(self):
        pass

    def display(self):
        plt.show()