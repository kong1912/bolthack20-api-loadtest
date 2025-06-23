import subprocess
import os
from datetime import datetime

tags = [
    "signup",
    "signin",
    "users",
    "get_all",
    "get_by_id",
    "create",
    "chats",
    "get_all_ids"
]

report_folder = datetime.now().strftime("report/report_%Y%m%d_%H%M%S")
os.makedirs(report_folder, exist_ok=True)

# log_folder = "logs"
# for file in os.listdir(log_folder):
#     file_path = os.path.join(log_folder, file)
#     if os.path.isfile(file_path):
#         os.remove(file_path)

# for tag in tags:
#     print(f"Running Locust for tag: {tag}")
    
subprocess.run([
        "locust",
        "-f", "locustfile.py",
        # "--tags", tag,
        "--headless",
        "--html", os.path.join(report_folder, f"report.html")
    ])

# processes = []
# for tag in tags:
#     print(f"Starting Locust for tag: {tag}")
#     p = subprocess.Popen([
#         "locust",
#         "-f", "locustfile.py",
#         "--tags", tag,
#         "--headless",
#         "-u", "50",           # number of users
#         "-r", "50",           # Ramp up rate
#         "-t", "10m",          # Test duration
#         "--html", os.path.join(report_folder, f"report_{tag}.html")
#     ])
#     processes.append(p)

# # Wait for all processes to finish
# for p in processes:
#     p.wait()