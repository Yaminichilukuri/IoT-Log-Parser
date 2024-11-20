import pandas as pd
import matplotlib.pyplot as plt
import json
import time  # Importing time module for measuring time

# Time taken to create visualizations
start_time = time.time()

# Function to parse a log entry
def parse_log_entry(log_entry):
    try:
        log_data = json.loads(log_entry)
        
        # Extracting basic fields
        user = log_data.get('user')
        timestamp = log_data.get('timestamp')
        ip = log_data.get('ip')
        event = log_data.get('event')
        details = log_data.get('details', {})

        # Extracting nested details like item_id, quantity, and price
        item_id = details.get('item_id')
        quantity = details.get('quantity')
        price = details.get('price')

        return {
            "user": user,
            "timestamp": timestamp,
            "ip": ip,
            "event": event,
            "item_id": item_id,
            "quantity": quantity,
            "price": price,
        }

    except Exception as e:
        print(f"Error parsing log entry: {e}")
        return None

# Function to process logs and convert them to DataFrame
def process_logs(input_file):
    data = []
    with open(input_file, "r") as file:
        for line in file:
            if not line.strip():
                continue
            
            parsed_data = parse_log_entry(line.strip())
            if parsed_data:
                data.append(parsed_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

# Function to plot event frequency
def plot_event_frequency(df):
    """
    Plot event frequency.
    """
    event_counts = df['event'].value_counts()
    event_counts.plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title('Event Frequency')
    plt.xlabel('Event Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function to plot price distribution
def plot_price_distribution(df):
    """
    Plot the distribution of price values.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(df['price'].dropna(), bins=30, color='orange', edgecolor='black')  # Drop NaN values for better visualization
    plt.title('Price Distribution')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function to plot quantity vs price relationship
def plot_quantity_vs_price(df):
    """
    Plot quantity vs price relationship.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(df['quantity'].dropna(), df['price'].dropna(), alpha=0.7, color='green')  # Drop NaN values for scatter plot
    plt.title('Quantity vs Price')
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function to plot error type frequency
def plot_error_type_frequency(df):
    """
    Plot the frequency of error types.
    """
    # Filter events that contain 'error' and count their occurrences
    error_counts = df[df['event'].str.contains('error', case=False, na=False)]  # case-insensitive search for 'error'
    if not error_counts.empty:
        error_type_counts = error_counts['event'].value_counts()
        error_type_counts.plot(kind='bar', figsize=(10, 6), color='red')
        plt.title('Error Type Frequency')
        plt.xlabel('Error Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("No error events found in the data.")

# Main function to execute the script
def main():
    input_file = 'C:/Users/Admin/Desktop/IoT_Log_Parser/logs/raw_logs.txt'  # Provide the path to your log file

    # Process the logs and convert to DataFrame
    df = process_logs(input_file)
    
    # Plot the visualizations
    plot_event_frequency(df)  # Event Frequency
    plot_price_distribution(df)  # Price distribution
    plot_quantity_vs_price(df)  # Quantity vs Price
    plot_error_type_frequency(df)  # Error type frequency

    # Measure time for visualization creation
    end_time = time.time()
    visualization_time = end_time - start_time
    print(f"Data visualization took {visualization_time:.4f} seconds.")

if __name__ == "__main__":
    main()
