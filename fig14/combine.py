import os
import pandas as pd

# Define the base directory and output file
base_dir = "/root/new_results"  # Replace with the path to your folders
output_file = "combined_results.csv"

# Initialize an empty DataFrame
combined_df = pd.DataFrame()

# Iterate through the main folders
main_folders = ["results_cc_nonquant", "results_cc_quant", "results_noncc_nonquant", "results_noncc_quant"]
for main_folder in main_folders:
    main_folder_path = os.path.join(base_dir, main_folder)

    # Iterate through the subfolders (hf, vllm)
    for subfolder in ["hf", "vllm"]:
        subfolder_path = os.path.join(main_folder_path, subfolder)

        if os.path.exists(subfolder_path):
            # Iterate through the runs (subsubfolders)
            for run_folder in os.listdir(subfolder_path):
                run_folder_path = os.path.join(subfolder_path, run_folder)

                if os.path.isdir(run_folder_path):
                    # Find the CSV file in the run folder
                    for file in os.listdir(run_folder_path):
                        if file.endswith(".csv"):
                            csv_file_path = os.path.join(run_folder_path, file)

                            # Read the CSV file into a DataFrame
                            df = pd.read_csv(csv_file_path)

                            # Add metadata columns
                            df["Main_Folder"] = main_folder
                            df["Subfolder"] = subfolder
                            df["Run_Folder"] = run_folder

                            # Append to the combined DataFrame
                            combined_df = pd.concat([combined_df, df], ignore_index=True)

# Save the combined DataFrame to a CSV file
combined_df.to_csv(output_file, index=False)
print(f"Combined CSV saved to {output_file}")