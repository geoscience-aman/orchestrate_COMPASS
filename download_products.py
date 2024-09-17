import argparse
import asf_search as asf
import os
import getpass
import warnings

def get_credentials(credentials_file=None):
    """
    Retrieve credentials either from a credentials file or interactively from the user.
    
    Args:
        credentials_file (str, optional): Path to the credentials file.
    
    Returns:
        tuple: (username, password)
    """
    username = None
    password = None
    
    if credentials_file and os.path.exists(credentials_file):
        with open(credentials_file, 'r') as file:
            lines = file.read().splitlines()
            if len(lines) >= 2:
                username = lines[0]
                password = lines[1]
            else:
                print("Credentials file must contain at least two lines: username and password.")
                return None, None
    
    if not username or not password:
        # Prompt user for credentials
        print("Credentials not found or not provided. Please enter them.")
        username = input("Username: ")
        password = getpass.getpass("Password: ")

    return username, password

def download_product(file_id, download_dir, username, password):
    try:
        # Set credentials for ASF product search
        session = asf.ASFSession().auth_with_creds(username, password)
        
        # Search for the product
        product = asf.product_search(file_id)[0]  # Ensure the product exists
        
        # Download the product
        product.download(download_dir, session=session)
        print(f"Successfully downloaded {file_id} to {download_dir}")
    except Exception as e:
        print(f"Failed to download {file_id}: {str(e)}")

def main(products_file, download_dir, credentials_file=None):
    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)
    
    # Get credentials
    username, password = get_credentials(credentials_file)
    if username is None or password is None:
        print("Credentials are required. Exiting.")
        return
    
    try:
        with open(products_file, 'r') as file:
            file_ids = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: The file '{products_file}' does not exist.")
        return

    # Suppress warnings for existing files
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        for file_id in file_ids:
            download_product(file_id, download_dir, username, password)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Sentinel-1 products.')
    parser.add_argument('products_file', type=str, help='File containing list of product IDs to download.')
    parser.add_argument('download_dir', type=str, help='Directory where the products will be downloaded.')
    parser.add_argument('--credentials_file', type=str, help='Path to a file containing credentials.', default=None)

    args = parser.parse_args()
    main(args.products_file, args.download_dir, args.credentials_file)
