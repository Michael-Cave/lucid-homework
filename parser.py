import sys
import os
from collections import deque
from datetime import datetime

# Parses command-line arguments
def parse_arguments(args):
    
    # Checks if the correct number of arguemnts have been given.
    if len(args) < 4 or len(args) > 5:
        print("Invalid syntax. Usage: script_name <target_file_path> <target_date> <optional_stop_date> <search_term>")
        sys.exit(1)

    # Extracts the file path and search term
    file_path = args[1]
    search_term = args[-1]
    
    # Handles the start date and optional stop date
    start_date = args[2]
    stop_date = None
    if len(args) == 5:
        stop_date = args[3]
    
    # Returns the appropriate arguments depending on if a stop date is given
    if stop_date == None:
        return file_path, start_date, search_term
    else :
        return file_path, start_date, stop_date, search_term
    


# Converts date strings to valid datetime objects
def parse_date_from_string(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")

# Checks if the log date is within the target range
def log_date_within_range(log_date_str, start_date, stop_date=None):
    log_date = datetime.strptime(log_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()

    # Returns true if the log date is on the target date or if the log date is within the target range
    if stop_date == None:
        return log_date == start_date
    else:
        return start_date <= log_date <= stop_date
    

# Filters logs by date and saves them to a seperate file for ease of work
def filter_logs_by_date(file_path, start_date_str, stop_date_str=None):
    start_date = parse_date_from_string(start_date_str).date()

    # Sets stop date as None unless specifically given.
    stop_date = parse_date_from_string(stop_date_str).date() if stop_date_str else None

    # Grabs the original file name from the file path
    original_file_name = os.path.basename(file_path).split('.')[0]

    # Sets a date range for the target file path filename
    if stop_date:
        date_range = f'{start_date_str}-{stop_date_str}'
    else:
        date_range = f'{start_date_str}'

    # Sets a target path for the filtered logs file
    target_file_path = f'./parsed log chunks/{original_file_name}_{date_range}.txt'

    # Checks if the target file already exists
    if os.path.exists(target_file_path):
        print(f'File {target_file_path} already exists. No need to filter again.')
        return target_file_path

    with open(file_path, 'r') as file, open(target_file_path, 'w') as target_file:
        in_date_range = False
        reached_target_date = False

        for line in file:
            try:
                log_date_str = line.split("|")[0].strip()
                if log_date_within_range(log_date_str, start_date, stop_date):
                    in_date_range = True
                    reached_target_date = True
                else:
                    in_date_range = False
            except ValueError:
                if not in_date_range:
                    continue
            if in_date_range:
                target_file.write(line)

            if not in_date_range and reached_target_date:
                break
    
    return target_file_path

# Searches through the filtered logs for the search term and prints out the hit line and the five lines above and below for context
def search_filtered_log(target_file_path, search_term):

    prev_lines = deque(maxlen=6)

    post_match_counter = 0

    with open(target_file_path, 'r') as file:
        for line in file:

            # Checks if a match has been made in the past five lines and prints the next line for context
            # Also check for the search term and resets the counter if found
            if post_match_counter > 0:
                print(line, end=' ')
                if search_term in line:
                    post_match_counter = 5
                else:
                    post_match_counter -= 1
                continue

            prev_lines.append(line)
            
            # Prints the previous five lines and current line for context
            if search_term in line:
                for pline in list(prev_lines)[:-1]:
                    print(pline, end=' ')
                print(line, end=' ')
                post_match_counter = 5




def main():

    # Grabs the arguments from parse_arguments
    args = parse_arguments(sys.argv)

    # Sets the arguments based on which flavor of args returned
    if len(args) == 3:
        file_path, start_date, search_term = args
        stop_date = None
    elif len(args) == 4:
        file_path, start_date, stop_date, search_term = args


    target_file = filter_logs_by_date(file_path, start_date, stop_date)
    search_filtered_log(target_file, search_term)



if __name__ == "__main__":
    main()