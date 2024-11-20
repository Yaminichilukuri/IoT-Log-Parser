import re
import base64
import json
import pandas as pd

def parse_web_server_logs(log_line):
    """
    Parse a single web server log line, including Base64-encoded logs.
    """
    # Check if the line contains a Base64 encoded entry
    if log_line.startswith("BASE64:"):
        # Extract Base64 part
        base64_data = log_line.replace("BASE64:", "").strip()
        try:
            # Decode Base64 data
            decoded_data = base64.b64decode(base64_data).decode('utf-8')
            # Try to parse the decoded data as JSON
            parsed_data = json.loads(decoded_data)
            return parsed_data
        except Exception as e:
            print(f"Error decoding Base64 data: {e} - Data: {log_line}")
            return None
    else:
        # If not Base64, parse as regular log
        pattern = r"(\d+\.\d+\.\d+\.\d+|\w+_\d+) - - \[(.*?)\] \"(.*?)\" (\d+) (\d+)"
        match = re.match(pattern, log_line)
        if match:
            ip, timestamp, request, status_code, size = match.groups()
            return {"IP": ip, "Timestamp": timestamp, "Request": request, "Status": int(status_code), "Size": int(size)}
        else:
            print(f"Skipping malformed log entry: {log_line}")
            return None

def process_web_server_logs(input_file, output_file):
    """
    Process web server logs and save metrics to a CSV.
    """
    data = []
    with open(input_file, "r") as log_file:
        for line in log_file:
            parsed = parse_web_server_logs(line)
            if parsed:
                data.append(parsed)

    if data:
        # Convert to DataFrame and save
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f"Web server log metrics saved to {output_file}")
    else:
        print("No valid log entries found.")

# Example of usage
input_file = 'C:/Users/Admin/Desktop/IoT_Log_Parser/logs/raw_logs.txt'  # Provide the actual path to your log file
output_file = 'C:/Users/Admin/Desktop/IoT_Log_Parser/data/structured_data.csv'  # Specify the correct output file path
process_web_server_logs(input_file, output_file)
