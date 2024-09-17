import argparse
import getpass
import os
from pathlib import Path
from eof.download import download_eofs

def load_credentials_from_file(filepath):
    """Load credentials from a plain text file."""
    with open(filepath, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        return username, password

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Download Sentinel-1 EOFs securely.")
    parser.add_argument(
        'sentinel_file', 
        type=str, 
        help="Path to the Sentinel-1 SAFE file"
    )
    parser.add_argument(
        '--creds', 
        type=str, 
        help="Path to the text file containing ASF credentials"
    )
    args = parser.parse_args()

    # Determine how to get credentials
    if args.creds and Path(args.creds).exists():
        asf_user, asf_password = load_credentials_from_file(args.creds)
        print(f"Using credentials from file: {args.creds}")
    else:
        # Securely input credentials (username and password)
        asf_user = getpass.getpass("Enter ASF Username (hidden): ")
        asf_password = getpass.getpass("Enter ASF Password (hidden): ")

    # Notify user that download is starting
    print(f"Starting download for Sentinel file: {args.sentinel_file}...")

    # Call the download function and capture the return value (list of paths)
    downloaded_file_paths = download_eofs(
        sentinel_file=args.sentinel_file,
        asf_user=asf_user,
        asf_password=asf_password
    )

    # Convert each PosixPath to a readable string if necessary
    readable_paths = [str(Path(p)) for p in downloaded_file_paths]

    # Notify user that download has completed
    print("Download completed.")
    for path in readable_paths:
        print(f"File has been downloaded to: {path}")

if __name__ == '__main__':
    main()
