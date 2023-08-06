import numpy as np
import matplotlib.pyplot as plt
from gdalconst import GA_ReadOnly
from osgeo import gdal, osr


path_tiffE7 = r"C:\bio\out_new_8_aprile\AGB\BIOMASS_L2_20210408T103223\AGB\Products\global_AGB\AF050M\E042N048T6\agb_1_est_db_backtransf_.tif"
driver = gdal.Open(path_tiffE7, GA_ReadOnly)
projection = driver.getProjection()
if 'AUTHORITY["EPSG","9001"]' in projection:
    print("EQUI7")
driver = None

path_tiff = r"C:\bio\out_new_8_aprile\AGB\BIOMASS_L2_20210408T103223\AGB\Products\temp\geocoded\GC_02_H_230.00_RGSW_00_RGSBSW_00_AZSW_00\sigma0_hh.tif"
driver = gdal.Open(path_tiff, GA_ReadOnly)
proll = driver.GetProjection()
driver = None
if 'AUTHORITY["EPSG","9001"]' in proll:
    print("EQUI7")
if 0:
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.cos(x)

    fig, ax = plt.subplots()
    ax.set_xlabel("xxxx")
    ax.set_title("TESTING")
    ax.set_xlim([1, 7])

    ax.plot(x, y, "r+")
    fig.savefig("prova2.png")  # save the figure as a PNG image
