import rasterio
from rasterio.crs import CRS as rcrs
from rasterio import warp
import cartopy
import cartopy.crs as ccrs

NSIDCNorthPolarStereo_25km = {
    'pixel_width': 25000,
    'pixel_height': 25000,
    'ccrs': {
        'central_latitude': 90.0,
        'central_longitude': -45.0,
        'false_easting': 0.0,
        'false_northing': 0.0,
        'true_scale_latitude': 70 
    },
    'bounds': [-3850000.000, 3750000., -5350000., 5850000.000]
}
Hughs1880Ellps = ccrs.Globe(datum=None, semimajor_axis=6378273., semiminor_axis=6356889.449)
NSIDCNorthPolarStereo_crs = ccrs.Stereographic(**src_proj['ccrs'], globe=src_globe)
    
    #define 25-km EASE2 grid
EASE2_25km = {
    'pixel_width': 25067.5,
    'pixel_height': 25067.5,
    'ccrs': {
        'central_latitude': 90.,
        'central_longitude': 0.,
        'false_easting': 0.0,
        'false_northing': 0.0
    },
    'bounds': [-4524683.8, 4524683.8, -4524683.8, 4524683.8],
    'size': (361, 361),
}
EASE2_Globe = ccrs.Globe(datum=None, semimajor_axis=6371228, semiminor_axis=6371228)
EASE2_crs = ccrs.LambertAzimuthalEqualArea(**dst_proj['ccrs'], globe=dst_globe)


def regrid_PS2EASE(data):
    
    src_rcrs = rcrs.from_string(NSIDCNorthPolarStereo_crs.proj4_init)
    #src_rcrs = rcrs.from_string('+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +a=6378273 +b=6356889.449 +units=m +no_defs')

    dst_rcrs = rcrs.from_string(EASE2_crs.proj4_init)
    #dst_rcrs = rcrs.from_string('+proj=laea +lat_0=90 +lon_0=0 +x_0=0 +y_0=0 +a=6371228 +b=6371228 +units=m +no_defs')

    # Get shape of source grid
    source_height, source_width = data.shape

    # Define source affine transformation
    src_transform = rasterio.Affine(NSIDCNorthPolarStereo_25km['pixel_width'],  # pixel width
                                    0.,                      # row rotation
                                    NSIDCNorthPolarStereo_25km['bounds'][0],   # Left coordinate
                                    0.,                      # Column rotation
                                    -1*NSIDCNorthPolarStereo_25km['pixel_height'], # pixel height
                                    NSIDCNorthPolarStereo_25km['bounds'][3])

    # Define destination affine transformation
    dst_transform = rasterio.Affine(dst_proj['pixel_width'], # pixel width
                                0.,                      # row rotation
                                dst_proj['bounds'][0],   # Left coordinate
                                0.,                      # Column rotation
                                -1*dst_proj['pixel_height'], # pixel height
                                dst_proj['bounds'][3])
    #Initialize the destination arrays
    data_ease=np.empty(dst_size,dtype=float)
    #do reprojection
    warp.reproject(source=data.astype(float), 
              src_crs=src_rcrs,
              src_nodata=np.nan,
              src_transform=src_transform,
              destination=data_ease,
              dst_transform=dst_transform,
              dst_crs=dst_rcrs,
              dst_nodata=np.nan,
              SOURCE_EXTRA=0,
              resampling=warp.Resampling.nearest)
    return(data_ease)
 