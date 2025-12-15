import os
import glob
import pandas as pd

# Set the working directory to the path where you are running the script
current_directory = r"C:\Users\Acer\Documents\GitHub\uitm-devops-challenge_trio\rentverse-datasets-main\output\output\output"
os.chdir(current_directory)

# Find all files ending with .csv
extension = 'csv'
all_filenames = [i for i in glob.glob(f'*.{extension}')]

# Create a list to hold dataframes that successfully load
list_of_dfs = []

for filename in all_filenames:
    # Check if the file is empty before trying to read it
    if os.stat(filename).st_size == 0:
        print(f"Skipping empty file: {filename}")
        continue
    else:
        try:
            # Read the file and append to the list
            df = pd.read_csv(filename)
            list_of_dfs.append(df)
            print(f"Successfully read: {filename}")
        except pd.errors.EmptyDataError:
            print(f"Could not parse data from file (might have only headers): {filename}")
        except Exception as e:
            # Catch other potential reading errors (e.g., bad encoding)
            print(f"An error occurred while reading {filename}: {e}")


# Combine all data frames in the list if the list is not empty
if list_of_dfs:
    combined_csv = pd.concat(list_of_dfs, ignore_index=True)
    output_path = os.path.join(current_directory, "combined_csv.csv")
    combined_csv.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nSuccessfully merged {len(list_of_dfs)} files into combined_csv.csv")
else:
    print("\nNo non-empty CSV files were found to merge.")

# Note: The output file will be created in the same directory as the input files.