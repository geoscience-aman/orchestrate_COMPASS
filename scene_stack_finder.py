import argparse
import asf_search as asf
import csv

def calculate_relative_orbit(metadata):
    """
    Calculate the relative orbit number based on the absolute orbit number and satellite platform.

    Args:
        metadata (dict): A dictionary containing metadata of the Sentinel-1 product.

    Returns:
        int: The relative orbit number.
    """
    platform = metadata.get('platform', '')
    absolute_orbit = metadata.get('orbit', 0)

    if platform == 'Sentinel-1A':
        relative_orbit = (absolute_orbit - 73) % 175 + 1
    elif platform == 'Sentinel-1B':
        relative_orbit = (absolute_orbit - 27) % 175 + 1
    else:
        raise ValueError("Unknown platform. Unable to determine relative orbit number.")

    return relative_orbit

def print_csv_header():
    print("fileID,pathNumber,temporalBaseline,perpendicularBaseline")

def print_csv_row(item):
    print(f"{item.properties['fileID']},{item.properties['pathNumber']},"
          f"{item.properties.get('temporalBaseline', 'N/A')},"
          f"{item.properties.get('perpendicularBaseline', 'N/A')}")

def main(granule, max_neighbors=None, max_perpendicular_baseline=None, max_temporal_baseline=None, id_file=None):
    """
    Main function to search for Sentinel-1 products and filter them based on the granule.

    Args:
        granule (str): The granule identifier for the Sentinel-1 product.
        max_neighbors (int, optional): The maximum number of neighboring products to include in the stack list.
        max_perpendicular_baseline (float, optional): The maximum perpendicular baseline value for filtering.
        max_temporal_baseline (float, optional): The maximum temporal baseline value for filtering.
        id_file (str, optional): The file to save only the file IDs. If None, no file will be saved.
    """
    product_name = granule + '-SLC'

    # Querying the product
    product_results = asf.product_search(product_name)
    assert len(product_results) == 1, 'Length of product results is not 1.'
    product = product_results[0]

    # Calculate the relative orbit for the product
    product_relative_orbit = calculate_relative_orbit(product.properties)

    # Retrieve the stack list with the same relative orbit and other conditions
    stack_list = [item for item in product.stack()
                  if calculate_relative_orbit(item.properties) == product_relative_orbit]

    if max_perpendicular_baseline is not None:
        stack_list = [item for item in stack_list
                      if item.properties.get('perpendicularBaseline') is not None and
                      abs(item.properties['perpendicularBaseline']) < max_perpendicular_baseline]

    if max_temporal_baseline is not None:
        stack_list = [item for item in stack_list
                      if item.properties.get('temporalBaseline') is not None and
                      abs(item.properties['temporalBaseline']) < max_temporal_baseline]

    if max_neighbors is not None:
        stack_list = list(reversed(stack_list))[:max_neighbors]

    # Print all item properties in CSV format
    print_csv_header()
    for item in stack_list:
        print_csv_row(item)

    # Optionally output only file IDs to a separate file
    if id_file:
        with open(id_file, 'w', newline='') as idfile:
            idfile.write("\n".join(item.properties['fileID'] for item in stack_list))
        print(f"File IDs saved to {id_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Sentinel-1 granule.')
    parser.add_argument('granule', type=str, help='The granule identifier for the Sentinel-1 product.')
    parser.add_argument('--max_neighbors', type=int, help='The maximum number of neighboring products to include in the stack list.')
    parser.add_argument('--max_perpendicular_baseline', type=float, help='The maximum perpendicular baseline value for filtering.')
    parser.add_argument('--max_temporal_baseline', type=float, help='The maximum temporal baseline value for filtering.')
    parser.add_argument('--id_file', type=str, help='Optional file to save only the file IDs. If not provided, no file will be saved.')

    args = parser.parse_args()
    main(args.granule, args.max_neighbors, args.max_perpendicular_baseline, args.max_temporal_baseline, args.id_file)
