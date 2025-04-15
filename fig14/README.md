# Overview

This project consists of several Python scripts designed to run LLM inference tasks using different configurations on two different serving backends, namely VLLM and HuggingFace (HF). The scripts include:

- `quant.py`
- `nonquant.py`
- `quant_run.py`
- `nonquant_run.py`
- `combine.py`

The scripts include timing information for different inference sections (loading model, etc.).

## Script Descriptions and Usage

### `quant.py`

**Description:**
This script is responsible for processing a quantized model using AWQ, which means it deals with computations optimized for reduced precision. Quantized models typically provide lower memory usage, making them efficient for deployment on edge devices or limited-resource hardware.

**Usage:**

For VLLM:
```sh
python quant.py --output-len <output-len> --num-prompts <batch_size> --input-len <input_length>
```

For HF:
```sh
python quant.py --output-len <output-len> --num-prompts <batch_size> --input-len <input_length> --backend <backend_type> --hf-max-batch-size <hf-max-batch-size>
```

### `nonquant.py`

**Description:**
This script handles the non-quantized version of the model, which retains full floating-point precision. While it consumes more memory and computational resources, it often provides higher accuracy.

**Usage:**

For VLLM:
```sh
python nonquant.py --output-len <output-len> --num-prompts <batch_size> --input-len <input_length>
```

For HF:
```sh
python nonquant.py --output-len <output-len> --num-prompts <batch_size> --input-len <input_length> --backend <backend_type> --hf-max-batch-size <hf-max-batch-size>
```

### `quant_run.py`

**Description:**
A driver script designed to execute the quantized model. It sets up the environment, loads the quantized model in `quant.py`, and runs inference on given input data. The script also includes logging and evaluation metrics.

**Usage:**
```sh
python quant_run.py
```

*Note:* You need to manually change the output folder name.

### `nonquant_run.py`

**Description:**
This script serves as the execution pipeline for the non-quantized model. It follows the same structure as `quant_run.py` but calls functions from `nonquant.py` to perform inference without quantization. The script also includes logging and evaluation metrics.

**Usage:**
```sh
python nonquant_run.py
```

*Note:* You need to manually change the output folder name.

### `combine.py`

**Description:**
A utility script that merges or compares results from `quant.py` and `nonquant.py`. It may be used to analyze accuracy differences, generate reports, or combine predictions from both models for further evaluation.

**Usage:**
```sh
python combine.py
```
