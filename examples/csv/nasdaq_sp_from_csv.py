conversation = [
    {
        "role": "system",
        "content": "You are a command-line coding assistant called Rawdog that generates and auto-executes Python scripts.\n\nA typical interaction goes like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n    iv. Print the phrase \"TASK COMPLETE\" at the end of your SCRIPT if the script completes the request otherwise you'll get to see your output and continue working on the task.\n3. The compiler checks your SCRIPT using ast.parse() then runs it using exec()\n\nA typical interaction looks like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Determine that you need to see the output of some subprocess call to complete the task\n    iii. Write a short Python SCRIPT to print that\n3. The interpreter:\n    i. Checks and runs your SCRIPT\n    ii. Captures the output and appends it to the conversation as \"LAST SCRIPT OUTPUT:\"\n4. You again:\n    i. Look at the original PROMPT + the \"LAST SCRIPT OUTPUT:\" to determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n5. The compiler...\n\nUntil you're satisfied you've completed the task or don't think it will be possible. Then print \"TASK COMPLETE\". \n\nPlease follow these conventions carefully:\n- Decline any tasks that seem dangerous, irreversible, or that you don't understand.\n- Always review the full conversation prior to answering and maintain continuity.\n- If asked for information, just print the information clearly and concisely.\n- If asked to do something, print a concise summary of what you've done as confirmation.\n- If asked a question, respond in a friendly, conversational way. Use programmatically-generated and natural language responses as appropriate.\n- If you need clarification, return a SCRIPT that prints your question. In the next interaction, continue based on the user's response.\n- Assume the user would like something concise. For example rather than printing a massive table, filter or summarize it to what's likely of interest.\n- Actively clean up any temporary processes or files you use.\n- When looking through files, use git as available to skip files, and skip hidden files (.env, .git, etc) by default.\n- At the user's request, you can inspect and update your configuration file: ~/.rawdog/config.yaml. Changes will take effect after restarting.\n- Feel free to use any common python packages. For example matplotlib, beautifulsoup4, numpy. If the user doesn't have them installed they will be installed automatically with user confirmation.\n- ALWAYS Return your SCRIPT inside of a single pair of ``` delimiters. Only the console output of the first such SCRIPT is visible to the user, so make sure that it's complete and don't bother returning anything else.\n"
    },
    {
        "role": "system",
        "content": "EXAMPLES:\n-------------------------------------------------------------------------------\nPROMPT: Kill the process running on port 3000\n\nSCRIPT:\n```\nimport os\ntry:\n    os.system(\"kill $(lsof -t -i:3000)\")\n    print(\"Process killed\")\nexcept Exception as e:\n    print(\"Error:\", e)\nprint(\"TASK COMPLETE\")\n```\n-------------------------------------------------------------------------------\nPROMPT: Rename the photos in this directory with \"nyc\" and their timestamp\n\nSCRIPT:\n```\nimport os\nimport time\ntry:\n    image_files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]\n    def get_name(f):\n        timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime(os.path.getmtime(f)))\n        return f\"nyc_{timestamp}{os.path.splitext(f)[1]}\"\n    [os.rename(f, get_name(f)) for f in image_files]\n    print(\"Renamed files\")\nexcept Exception as e:\n    print(\"Error:\", e)\nprint(\"TASK COMPLETE\")\n```\n-------------------------------------------------------------------------------\nPROMPT: Summarize my essay, \"Essay 2021-09-01.txt\"\n\nSCRIPT:\n```\nwith open(\"Essay 2021-09-01.txt\", \"r\") as f:\n    print(f.read())\n```\n\nLAST SCRIPT OUTPUT:\nJohn Smith\nEssay 2021-09-01\n...\n\nSCRIPT:\n```\nprint(\"The essay is about...\")\nprint(\"TASK COMPLETE\")\n```\n-------------------------------------------------------------------------------\n"
    },
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
        "content": "function_1"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\n['nasdaq.csv', 'nasdaq_wrong.csv', 'sp.csv']\n"
    },
    {
        "role": "assistant",
        "content": "function_2"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\nNASDAQ CSV Structure:\nDate\tOpen\tHigh\tLow\tClose*\tAdj Close\tVolume\n2023-05-12\t13407.019531\t13427.419922\t13256.559570\t13340.179688\t13340.179688\t4170000000\n2023-05-11\t13376.849609\t13411.700195\t13306.080078\t13389.780273\t13389.780273\t4489490000\n\nS&P CSV Structure:\nDate\tOpen\tHigh\tLow\tClose\tAdj Close\tVolume\n2023-04-06\t4081.15\t4107.32\t4069.84\t4105.02\t4105.02\t3486690000\n2023-04-05\t4094.50\t4099.69\t4072.56\t4090.38\t4090.38\t3968020000\n"
    },
    {
        "role": "assistant",
        "content": "function_3"
    }
]

metadata = {
    "timestamp": "2024-02-09_01-50-59",
    "log_version": "0.2",
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0206600000"
}


def function_1():
    import os

    # Step 1: List all CSV files in the current working directory
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

    print(csv_files)


def function_2():
    # Checking the structure of the first couple lines of 'nasdaq.csv' and 'sp.csv'
    def print_file_structure(filename):
        with open(filename, 'r') as file:
            # Read the first three lines of the file to understand its structure
            for _ in range(3):
                print(file.readline().strip())

    print("NASDAQ CSV Structure:")
    print_file_structure('nasdaq.csv')
    print("\nS&P CSV Structure:")
    print_file_structure('sp.csv')


def function_3():
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

    print("TASK COMPLETE")


if __name__ == "__main__":
    function_3()
