from src.log_parser import process_logs
from src.web_server_parser import process_web_server_logs
from src.visualizations import plot_temperature

# Process IoT logs
process_logs("logs/sample_log.txt", "data/structured_data.csv")

# Visualize temperature data
plot_temperature("data/structured_data.csv")

# Process web server logs (if any)
# process_web_server_logs("logs/server_log.txt", "data/web_server_metrics.csv")
