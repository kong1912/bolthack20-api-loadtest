# Locust Load Testing Project

This project is designed to perform load testing on the API hosted at https://healthcare-0y63.onrender.com using Locust. The load tests will simulate multiple users interacting with the API endpoints, allowing for performance evaluation and stress testing.

## Project Structure

- **locustfile.py**: Contains the Locust load testing script. It defines user behavior and tasks to be executed during the load test, including the necessary JWT token for authentication.
  
- **requirements.txt**: Lists the dependencies required for the project, including Locust and any other necessary libraries.

- **README.md**: This documentation file provides instructions on how to set up and run the load tests, as well as relevant information about the API being tested.

## Setup Instructions

1. **Clone the Repository**: 
   Clone this repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**:
   ```
   cd locust-loadtest
   ```

3. **Install Dependencies**:
   Ensure you have Python installed, then install the required packages using:
   ```
   pip install -r requirements.txt
   ```

4. **Run Locust**:
   Start the Locust load testing server with the following command:
   ```
   locust -f locustfile.py
   ```

5. **Access the Web Interface**:
   Open your web browser and navigate to `http://localhost:8089` to access the Locust web interface. Here, you can configure the number of users and the spawn rate.

## API Information

The API being tested is hosted at `https://healthcare-0y63.onrender.com`. Ensure you have the necessary JWT token for authentication, which should be included in the headers of your requests as specified in the `locustfile.py`.

## Notes

- Make sure to monitor the performance metrics during the load tests to identify any potential bottlenecks or issues with the API.
- Adjust the number of simulated users and the spawn rate based on your testing requirements.