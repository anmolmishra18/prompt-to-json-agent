# llama_prompt.py
import json
import os
from transformers import pipeline

# Initialize distilgpt2 pipeline
try:
    # It's good practice to specify the device if you have a GPU, e.g., device=0 for the first GPU.
    # If no GPU is available, the pipeline will automatically default to CPU.
    pipe = pipeline("text-generation", model="distilgpt2")
except Exception as e:
    print(f"Error initializing text-generation pipeline: {e}")
    print("Please ensure the 'transformers' library is installed and the model 'distilgpt2' is available.")
    # Exit the script if the core functionality (pipeline) cannot be initialized.
    exit(1)

# Prompts to generate outputs from
prompts = [
    "Design a robotic arm for factory use using aluminum. It should",
    "Create a red gearbox with steel gears. The gearbox should",
    "Model a medieval throne for a fantasy game. The throne should"
]

log_file_path = "logs.json"
error_log_file_path = "error_log.txt"

# Generate and log responses
for prompt in prompts:
    try:
        # Generate continuation with sampling
        # max_new_tokens: The maximum number of tokens to generate. Increased to 50 for more complete outputs.
        # do_sample: If True, uses sampling; otherwise, uses greedy decoding.
        # temperature: Controls randomness; higher values mean more random outputs (e.g., 0.8 is moderately creative).
        # num_return_sequences: The number of sequences to return. Default is 1.
        response_list = pipe(prompt, max_new_tokens=50, do_sample=True, temperature=0.8, num_return_sequences=1)
        generated_text = response_list[0]["generated_text"]

        # Clean response: Replace multiple newlines with a single space and strip leading/trailing whitespace.
        # This ensures the output is suitable for a single-line log entry.
        cleaned_response = generated_text.replace("\n", " ").strip()

        # Prepare the log entry as a dictionary
        log_entry = {"prompt": prompt, "output": cleaned_response}

        # Log to file in JSON Lines (JSONL) format.
        # Each line in the file will be a valid JSON object.
        # Check if the file exists and is not empty to add a newline BEFORE the new entry.
        # This ensures each JSON object is on its own line, maintaining proper JSONL format,
        # even if the file was just created or didn't end with a newline previously.
        needs_newline = os.path.exists(log_file_path) and os.path.getsize(log_file_path) > 0

        with open(log_file_path, "a") as f:
            if needs_newline:
                f.write("\n")
            json.dump(log_entry, f)

        # Print the prompt and generated output for immediate feedback/debugging
        print(f"\nPrompt: {prompt}")
        print(f"Output: {cleaned_response}")

    except Exception as e:
        # Catch any exceptions that occur during text generation or file writing for a specific prompt.
        print(f"An error occurred while processing prompt '{prompt}': {e}")
        # Optionally, log the error details to a separate error file for later review.
        try:
            with open(error_log_file_path, "a") as error_f:
                error_f.write(f"Error processing prompt '{prompt}': {e}\n")
        except IOError as io_err:
            print(f"Could not write to error log file '{error_log_file_path}': {io_err}")

