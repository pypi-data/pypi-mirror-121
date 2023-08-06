from pathlib import Path
import sys
import os
from matplotlib import pyplot as plt
import numpy as np

biopal_path = Path("C:\ARESYS_PROJ\BioPAL")

sys.path.append(str(biopal_path))
os.chdir(biopal_path)

from biopal.io.data_io import BiomassL1cRaster, biomassL2raster
from biopal.utility.utility_functions import bioplot

input_path = r"C:\bio\demo_input_file_run_AGB.xml"

from biopal.dataset_query.dataset_query import dataset_query

dataset_query_obj = dataset_query()
input_path_from_query = dataset_query_obj.run(input_path)

from biopal.io.xml_io import parse_input_file

input_params_obj = parse_input_file(input_path_from_query)
stack_based_processing_obj = input_params_obj.stack_based_processing
found_stack_ids = stack_based_processing_obj.stack_composition.keys()
print(
    "SLC SAR images (slant range geometry) stacks and acquisitions found from the query"
)
for stack_id, acquisition_ids in stack_based_processing_obj.stack_composition.items():
    print("\n    Stack:")
    print("    ", stack_id)
    print("        Acquisitions:")
    for acq_id in acquisition_ids:
        print("        ", acq_id)
dataSet_path = input_params_obj.dataset_query.L1C_repository
print(
    "\n The above stacks with the acquisitions can be found at following path:\n {}".format(
        dataSet_path
    )
)
# Print the path of the DTM projected in radar coordinates
reference_height_path = Path.home().joinpath(
    dataSet_path, stack_based_processing_obj.reference_height_file_names[stack_id]
)
print(
    "\n Full path of the reference height file valid for the above stack {}: \n {}".format(
        stack_id, reference_height_path
    )
)


# Plotting one of the SLC
slc_pf_path = Path.home().joinpath(dataSet_path, acq_id)
channel_to_read = 2  # Counter is zero based, 2 is VH

SLC_obj = BiomassL1cRaster(slc_pf_path, channel_to_read)
SLC_figure = bioplot(SLC_obj).plot_db()
SLC_figure.show()
SLC_figure.savefig("SLC_figure.png")  # save the figure as a PNG image

if 0:
    fig, ax = plt.subplots()
    ax.set_xlabel("xxxx")
    ax.set_title("TESTING")
    SLC_figure2 = bioplot(SLC_obj).plot_db(ax)
    SLC_figure2.show()
    SLC_figure2.savefig("prova2.png")  # save the figure as a PNG image


channel_to_read = 0  # Counter is zero based, there is only one channel
reference_height_obj = BiomassL1cRaster(reference_height_path, channel_to_read)
ref_h_figure = bioplot(reference_height_obj).plot_db()
ref_h_figure.show()
ref_h_figure.savefig("ref_h_figure.png")  # save the figure as a PNG image


from biopal.agb.main_AGB import StackBasedProcessingAGB

configuration_file_path = str(
    Path.home().joinpath(biopal_path, "biopal", "conf", "Configuration_File.xml")
)

# Initialize Stack Based Processing AGB APP
stack_based_processing_obj = StackBasedProcessingAGB(configuration_file_path)

# Run Stack Based Processing AGB APP
print("AGB stack-based processing APP started...")
(
    input_file_from_stack_based,
    configuration_file_updated,
) = stack_based_processing_obj.run(input_path_from_query)

# Some of the computed output paths:
import os

input_params_obj = parse_input_file(input_file_from_stack_based)
output_folder = input_params_obj.output_specification.output_folder

npy_name = str(
    list(
        Path(Path.home().joinpath(output_folder, "Products", "breakpoints")).rglob(
            "*.npy"
        )
    )[0]
)
ground_canc_sr_path = Path.home().joinpath(
    output_folder,
    npy_name,
)
print(
    "\n Path of ground cancelled data in slant range geometry: \n {}".format(
        ground_canc_sr_path
    )
)

geocoded_dir = str(
    list(
        Path(Path.home().joinpath(output_folder, "Products", "temp", "geocoded")).rglob(
            "GC_*"
        )
    )[0]
)
sigma_tif_name = str(list(Path(geocoded_dir).rglob("sigma0_vh.tif"))[0])
ground_canc_gr_path = Path.home().joinpath(
    geocoded_dir,
    sigma_tif_name,
)
print(
    "\n  Path of ground cancelled VH data, geocoded: \n {}".format(ground_canc_gr_path)
)

theta_tif_name = str(list(Path(geocoded_dir).rglob("theta.tif"))[0])
theta_inc_path = Path.home().joinpath(
    geocoded_dir,
    theta_tif_name,
)
print("\n  Path of incidence angle map, geocoded: \n {}".format(theta_inc_path))


ground_canc_obj = biomassL2raster(str(ground_canc_gr_path), band_to_read=1)
ground_canc_figure = bioplot(ground_canc_obj).plot_db()
ground_canc_figure.show()
ground_canc_figure.savefig("ground_canc_figure.png")  # save the figure as a PNG image


theta_inc_obj = biomassL2raster(str(theta_inc_path), band_to_read=1)
theta_inc_figure = bioplot(theta_inc_obj).plot()
theta_inc_figure.show()
theta_inc_figure.savefig("ground_canc_figure.png")  # save the figure as a PNG image

from biopal.agb.main_AGB import CoreProcessingAGB

# Initialize Core Processing AGB APP
agb_processing_obj = CoreProcessingAGB(configuration_file_updated)

# Run Main APP #2: AGB Core Processing
print(
    "AGB core-processing APP started (this will take some time, wait for ending message)..."
)
agb_processing_obj.run(input_file_from_stack_based)


input_params_obj = parse_input_file(input_file_from_stack_based)
output_folder = input_params_obj.output_specification.output_folder
tile_equi7_folder = list(
    Path.home().joinpath(Path(output_folder), "Products", "global_AGB").rglob("*")
)[0]
tile_equi7_subfolder = list(Path(tile_equi7_folder).rglob("*"))[0]
final_estimation_path = list(Path(tile_equi7_subfolder).rglob("*.tif"))[0]
print(
    "\n Path of the final AGB estimation product, in EQUI7 map geometry: \n {}".format(
        final_estimation_path
    )
)

reference_agb_folder = input_params_obj.stack_based_processing.reference_agb_folder
calibration_path = Path.home().joinpath(reference_agb_folder, "cal_05_no_errors.tif")
print("\n Path of the input calibration data used: \n {}".format(calibration_path))


lidar_agb_path = r"C:\ARESYS_PROJ\workingDir\biopal_data_V2_update\lope_lidar\equi7_50m\lidar_agb\EQUI7_AF050M\E045N048T3\lidar_AGB_AF050M_E045N048T3.tif"

lidar_agb_figure = lidar_agb_obj.plot()
lidar_agb_figure.show()

theta_inc_obj = biomassL2raster(lidar_agb_path, band_to_read)
lidar_agb_figure = bioplot(lidar_agb_obj).plot()
lidar_agb_figure.show()
lidar_agb_figure.savefig("lidar_agb_figure.png")  # save the figure as a PNG image


calibration_path = str(
    Path.home().joinpath(reference_agb_folder, "cal_05_no_errors.tif")
)
band_to_read = 1
calibration_agb_obj = biomassL2raster(calibration_path, band_to_read)
calibration_agb_figure = calibration_agb_obj.plot("il mio titolo")
calibration_agb_figure.show()

calibration_agb_obj = biomassL2raster(calibration_path, band_to_read)
calibration_agb_figure = bioplot(calibration_agb_obj).plot()
calibration_agb_figure.show()
calibration_agb_figure.savefig(
    "calibration_agb_figure.png"
)  # save the figure as a PNG image
