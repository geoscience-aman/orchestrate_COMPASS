1. Install COMPASS: https://github.com/opera-adt/COMPASS
   
`conda install -c conda-forge compass`

2. Clone this repository.

`git clone https://github.com/geoscience-aman/orchestrate_COMPASS.git`

3. Activate the `compass` environment.

```
cd orchestrate_COMPASS
conda env create --file custom_compass_environment_no_builds.yml
conda activate compass
```

4. Clip the DEM to the scene size. 

The DEM coverage needs to be larger than the scene coverage. COMPASS takes care of the exact clipping to match the scene size. 

Usage: 
`python3 clip_dem.py dem_path scene_xml --buffer buffer_size`

E.g. (Run this on the NCI to avoid copying over the full DEM)

`python3 clip_dem.py /g/data/v10/eoancillarydata-2/elevation/copernicus_30m/copernicus-30m-dem.tif /g/data/fj7/Copernicus/Sentinel-1/C-SAR/SLC/2024/2024-08/65S105E-70S110E/S1A_IW_SLC__1SSH_20240804T130856_20240804T130923_055063_06B563_99ED.xml /g/data/u46/users/ac0646/cslc_gen_prep/clipped_dem.tif --buffer 0.1`

5. Find the stack of SLC.

`python3 scene_stack_finder.py S1A_IW_SLC__1SSH_20230130T130918_20230130T130945_047013_05A3A4_9800 --max_neighbors 10 --max_perpendicular_baseline 8 --max_temporal_baseline 400 --output_file file_ids.txt`

6. Download the resulting safe files.

`python3 download_products.py file_ids.txt ./ --credentials_file data/asf_credentials.txt`

7. Download precise orbit files.

`python3 download_eofs.py safe_file_path`

E.g. 

`python3 download_eofs.py /home/ubuntu/gen_cslc/data/safe/S1A_IW_SLC__1SSH_20240804T130856_20240804T130923_055063_06B563_99ED.zip`

The script will ask you for credentials that are securely stored using the `getpass` library in Python. Alternatively you can specify a credentials file.

`python3 download_eofs.py safe_file_path --creds credential_file_path`

8. Input the data and output locations in the config yaml file. 

9. Run. 

`python3 /home/ubuntu/COMPASS/src/compass/s1_cslc.py --grid geo custom_s1_cslc_geo.yaml`
