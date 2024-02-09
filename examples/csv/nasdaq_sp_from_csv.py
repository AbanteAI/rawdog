conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/jakekoenig/kalshiMarketMaker/data, which is NOT a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Can you make a graph that shows the price performance of the S&P and NASDAQ on top of each other? You should find the data you need in the cwd."
    },
    {
        "role": "assistant",
        "content": "```python\nimport os\n\n# Step 1: List all CSV files in the current working directory\ncsv_files = [f for f in os.listdir('.') if f.endswith('.csv')]\n\nprint(csv_files)\nprint(\"CONTINUE\")\n```"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\n['nasdaq.csv', 'nasdaq_wrong.csv', 'sp.csv']\nCONTINUE\n"
    },
    {
        "role": "assistant",
        "content": "```python\n# Checking the structure of the first couple lines of 'nasdaq.csv' and 'sp.csv'\ndef print_file_structure(filename):\n    with open(filename, 'r') as file:\n        # Read the first three lines of the file to understand its structure\n        for _ in range(3):\n            print(file.readline().strip())\n\nprint(\"NASDAQ CSV Structure:\")\nprint_file_structure('nasdaq.csv')\nprint(\"\\nS&P CSV Structure:\")\nprint_file_structure('sp.csv')\nprint(\"CONTINUE\")\n```"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\nNASDAQ CSV Structure:\nDate\tOpen\tHigh\tLow\tClose*\tAdj Close\tVolume\n2023-05-12\t13407.019531\t13427.419922\t13256.559570\t13340.179688\t13340.179688\t4170000000\n2023-05-11\t13376.849609\t13411.700195\t13306.080078\t13389.780273\t13389.780273\t4489490000\n\nS&P CSV Structure:\nDate\tOpen\tHigh\tLow\tClose\tAdj Close\tVolume\n2023-04-06\t4081.15\t4107.32\t4069.84\t4105.02\t4105.02\t3486690000\n2023-04-05\t4094.50\t4099.69\t4072.56\t4090.38\t4090.38\t3968020000\nCONTINUE\n"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0206600000",
    "timestamp": "2024-02-09_01-50-59",
    "log_version": 0.1
}


def main():
    import pandas as pd
    import matplotlib.pyplot as plt

    # Load data from the CSVs
    nasdaq_data = pd.read_csv('nasdaq.csv', sep='\t')
    sp_data = pd.read_csv('sp.csv', sep='\t')

    # Converting 'Date' from string to datetime for both datasets for proper plotting
    nasdaq_data['Date'] = pd.to_datetime(nasdaq_data['Date'])
    sp_data['Date'] = pd.to_datetime(sp_data['Date'])

    # Plotting
    plt.figure(figsize=(10, 6))

    # NASDAQ
    plt.plot(nasdaq_data['Date'], nasdaq_data['Close*'], label='NASDAQ')

    # S&P
    plt.plot(sp_data['Date'], sp_data['Close'], label='S&P 500')

    # Title and Labels
    plt.title('Price Performance of the S&P 500 and NASDAQ')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()

    # Show plot
    plt.show()


if __name__ == "__main__":
    main()
