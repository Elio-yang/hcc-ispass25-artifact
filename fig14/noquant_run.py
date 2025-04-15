import os
import csv
import subprocess

# Define configurations
batch_sizes = [1, 2, 4, 8, 16, 32, 64, 128]  # Values for --num-prompts
input_lengths = [128, 256, 512, 1024]  # Values for --input-len
backends = ['hf', 'vllm']  # Backend names
num_runs = 3  # Number of runs

# Loop over backends
for backend in backends:
    print(f"Running {backend} backend")

    # Create a folder for the backend
    backend_folder = f"./results_cc_nonquant/{backend}"
    os.makedirs(backend_folder, exist_ok=True)

    # Loop for each run
    for run_id in range(1, num_runs + 1):
        print(f"Run {run_id}/{num_runs} for {backend}")

        # Create a directory for the current run inside the backend folder
        run_folder = os.path.join(backend_folder, f"run_{run_id}")
        os.makedirs(run_folder, exist_ok=True)

        # CSV file to store results for this run
        output_csv = os.path.join(run_folder, f"{backend}-results.csv")

        # Write CSV headers (only once, if the file doesn't exist)
        if not os.path.exists(output_csv):
            with open(output_csv, mode="w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["batch_size", "input_length", "load_time", "gen_time", "ttft", "thruput"])

        # Loop through configurations and run commands
        for batch_size in batch_sizes:
            for input_length in input_lengths:
                # Base command
                base_command = f"nsys profile --trace=cuda,nvtx,osrt --cuda-memory-usage=true --output {run_folder}/{backend}-{batch_size}-{input_length} python nonquant.py --output-len 150"

                # Construct the command for the respective backend
                if backend == 'hf':
                    command = f"{base_command} --num-prompts {batch_size} --input-len {input_length} --backend hf --hf-max-batch-size 1024"
                else:
                    command = f"{base_command} --num-prompts {batch_size} --input-len {input_length}"

                # Run the command and capture the output
                print(f"Running: {command}")
                process = subprocess.run(command, shell=True, capture_output=True, text=True)

                # Parse the output for metrics
                output = process.stdout.splitlines()
                load_time = gen_time = ttft = thruput = None  # Default values

                for line in output:
                    if "load_time" in line:
                        load_time = float(line.split()[1].strip())
                    elif "gen_time" in line:
                        gen_time = float(line.split()[1].strip())
                    elif "ttft" in line:
                        ttft = float(line.split()[1].strip())
                    elif "thruput" in line:
                        thruput = float(line.split()[1].strip())

                print(load_time, gen_time, ttft, thruput)
                # Check if all metrics are present
                if None in (load_time, gen_time, ttft, thruput):
                    print(f"Missing metrics for batch_size={batch_size}, input_length={input_length}")
                    continue

                # Append results to the CSV file
                with open(output_csv, mode="a", newline="") as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([
                        batch_size,
                        input_length,
                        load_time,
                        gen_time,
                        ttft,
                        thruput,
                    ])