import subprocess
import requests
import time
import os
import sys

# Parses arguments into usable formats
def parse_arguments(args):
    if len(args) != 3:
        print("Usage: python copysync.py '<source_windows_path>' '<destination_windows_path>'")
        sys.exit(1)

    source_path = args[1]
    destination_path = args[2]
    return source_path, destination_path

# Converts Windows paths to Windows Subsystem for Linux paths
def convert_windows_path_to_wsl(windows_path):
    replace_backslash = windows_path.replace('\\', '/')
    replace_colon = replace_backslash.replace(':', '')

    linux_path = f"/mnt/{replace_colon}".lower()
    return linux_path

# Uses rsync to copy the source file to the target location
def copy_file_to_destination(source, destination):
    command = ["rsync", "-vz", source, destination]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("rsync completed successfully.")
        print(result.stdout)
    else:
        print("rsync failed.")
        print(result.stderr)


# Monitors "dirtyBytes" to see when the upload is complete
def check_dirty_bytes():
    url = "http://$(hostname).local:8280/cache/info"
    counter = 0

    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break
        data = response.json()

        # Validates dirtyBytes existence
        if "dirtyBytes" not in data:
            print("dirtyBytes key not found in the response.")
            break

        # Checks for end case
        if data['dirtyBytes'] == 0:
            break
        
        print(f"Time elapsed: {counter} seconds.")
        counter += 1
        # Time to retry
        time.sleep(1)


# Sends empty PUT request to synch changes
def send_put_request():
    url = "http://$(hostname):8280/app/sync"
    
    try:
        response = requests.put(url)
        response.raise_for_status()
        if 200 <= response.status_code <= 299:
            print("Synch completed successfully.")
        else:
            print(f"Sync failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    
    


def main():
    source, desintation = parse_arguments(sys.argv)
    source_path = convert_windows_path_to_wsl(source)
    destination_path = convert_windows_path_to_wsl(desintation)

    copy_file_to_destination(source_path, destination_path)
    check_dirty_bytes()
    send_put_request()




if __name__ == "__main__":
    main()