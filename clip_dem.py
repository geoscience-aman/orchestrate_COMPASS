import argparse
import xml.etree.ElementTree as ET
from osgeo import gdal, ogr

# Function to expand the bounding box by a buffer size
def add_buffer_to_bounds(bounds, buffer):
    min_x, min_y, max_x, max_y = bounds
    return [min_x - buffer, min_y - buffer, max_x + buffer, max_y + buffer]

# Set up argument parser
parser = argparse.ArgumentParser(description="Clip a TIFF file using WKT polygon from an XML file.")
parser.add_argument("input_tiff", type=str, help="Path to the input TIFF file.")
parser.add_argument("xml_file", type=str, help="Path to the XML file containing the WKT polygon.")
parser.add_argument("output_tiff", type=str, help="Path to save the output clipped TIFF file.")
parser.add_argument("--buffer", type=float, default=0.1, help="Buffer size to expand the clipping bounds (in the same units as the raster).")
args = parser.parse_args()

# Parse the XML file to extract the WKT polygon
tree = ET.parse(args.xml_file)
root = tree.getroot()

# Find the WKT polygon in the XML file
wkt_polygon = root.findtext('.//ESA_TILEOUTLINE_FOOTPRINT_WKT').strip()

# Create an OGR geometry object from the WKT
geom = ogr.CreateGeometryFromWkt(wkt_polygon)

# Get the envelope (bounding box) of the polygon
min_x, max_x, min_y, max_y = geom.GetEnvelope()

# Add buffer to the bounding box
buffer = args.buffer
expanded_bounds = add_buffer_to_bounds([min_x, min_y, max_x, max_y], buffer)

# Use gdalwarp to clip the input TIFF using the expanded bounding box
gdal.Warp(args.output_tiff, args.input_tiff, outputBounds=expanded_bounds, format='GTiff')

print(f"Clipped TIFF saved as {args.output_tiff}")
