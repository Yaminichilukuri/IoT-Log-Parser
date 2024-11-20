import base64
import re
import json
import pandas as pd

# Function to clean the Base64 string and handle padding issues
def clean_base64_string(encoded_str):
    # Remove any non-Base64 characters from the string
    encoded_str = re.sub(r'[^A-Za-z0-9+/=]', '', encoded_str)

    # Fix padding if necessary
    padding_needed = len(encoded_str) % 4
    if padding_needed != 0:
        encoded_str += '=' * (4 - padding_needed)

    return encoded_str

# Function to decode Base64 string, with padding fix and error handling
def decode_base64(encoded_str):
    try:
        # Clean the Base64 string
        encoded_str = clean_base64_string(encoded_str)

        # Skip invalid Base64 data
        if not is_valid_base64(encoded_str):
            print(f"Skipping invalid Base64 data: {encoded_str}")
            return None  # Skip invalid Base64 data

        # Try decoding the Base64 string
        decoded_bytes = base64.b64decode(encoded_str, validate=True)
        decoded_str = decoded_bytes.decode('utf-8')
        return decoded_str
    except base64.binascii.Error as e:
        print(f"Base64 decoding error: {e}, Data: {encoded_str}")
        # Log the Base64 string that caused the issue for further inspection
        with open("invalid_base64_logs.txt", "a") as log_file:
            log_file.write(f"Error decoding Base64: {e}, Data: {encoded_str}\n")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}, Data: {encoded_str}")
        return None

# Function to validate if the string is a valid Base64 encoded string
def is_valid_base64(encoded_str):
    # Check if the string contains only Base64-safe characters (A-Z, a-z, 0-9, +, /, =)
    base64_pattern = re.compile(r'^[A-Za-z0-9+/=]+$')
    
    # Check if the string matches the Base64 pattern
    if not base64_pattern.match(encoded_str):
        return False
    
    # Check if padding (equal signs) is valid
    padding = encoded_str.count("=")
    if padding > 2 or (padding == 1 and len(encoded_str) % 4 != 0):
        return False
    
    return True

# Function to parse the logs
def parse_logs(log_file):
    logs = []
    
    with open(log_file, "r") as file:
        for line in file:
            timestamp = None
            error_type = None
            base64_data = None
            json_data = None
            message = None

            # Extract timestamp
            timestamp_match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}', line)
            if timestamp_match:
                timestamp = timestamp_match.group(0)

            # Extract error types like IndexOutOfBoundsException, NullPointerException, etc.
            error_match = re.search(r'(IndexOutOfBoundsException|NullPointerException|KeyError|TimeoutError)', line)
            if error_match:
                error_type = error_match.group(0)

            # Extract Base64 encoded data
            base64_match = re.search(r'BASE64:([A-Za-z0-9+/=]+)', line)
            if base64_match:
                base64_data = decode_base64(base64_match.group(1))
                if base64_data is None:
                    # Skip this entry if Base64 decoding failed
                    continue

            # Extract JSON data
            json_match = re.search(r'\{.*\}', line)
            if json_match:
                try:
                    json_data = json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass  # Ignore malformed JSON

            # Store the parsed information in a dictionary
            logs.append({
                "timestamp": timestamp,
                "error_type": error_type,
                "base64_data": base64_data,
                "json_data": json_data,
                "message": line.strip()
            })

    return logs

# Path to the raw logs file
log_file = 'C:/Users/Admin/Desktop/IoT_Log_Parser/logs/raw_logs.txt'  # Replace with your actual log file path

# Parse the logs
parsed_logs = parse_logs(log_file)

# Convert parsed logs to a pandas DataFrame
df = pd.DataFrame(parsed_logs)

# Save structured data to CSV
output_path = 'C:/Users/Admin/Desktop/IoT_Log_Parser/data/structured_data.csv'  # Specify the correct path
df.to_csv(output_path, index=False)
print("Structured data saved to structured_data.csv")
