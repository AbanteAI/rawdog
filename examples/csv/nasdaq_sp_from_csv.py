conversation = [
    {
        "role": "system",
        "content": "You are a command-line coding assistant called Rawdog that generates and auto-executes Python scripts.\n\nA typical interaction goes like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n3. The compiler checks your SCRIPT using ast.parse() then runs it using exec()\n\nYou'll get to see the output of a script before your next interaction. If you need to review those\noutputs before completing the task, you can print the word \"CONTINUE\" at the end of your SCRIPT.\nThis can be useful for summarizing documents or technical readouts, reading instructions before\ndeciding what to do, or other tasks that require multi-step reasoning.\nA typical 'CONTINUE' interaction looks like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Determine that you need to see the output of some subprocess call to complete the task\n    iii. Write a short Python SCRIPT to print that and then print the word \"CONTINUE\"\n3. The compiler\n    i. Checks and runs your SCRIPT\n    ii. Captures the output and appends it to the conversation as \"LAST SCRIPT OUTPUT:\"\n    iii. Finds the word \"CONTINUE\" and sends control back to you\n4. You again:\n    i. Look at the original PROMPT + the \"LAST SCRIPT OUTPUT:\" to determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n5. The compiler...\n\nWhen your script raises an exception, you'll get to review the error and try again:\n1. The user gives you a natural language PROMPT.\n2. You: Respond with a SCRIPT..\n3. The compiler\n    i. Executes your SCRIPT\n    ii. Catches an exception\n    iii. Adds it to the conversation\n    iv. If there are retries left, sends control back to you\n4. You again:\n    i. Look at the latest PROMPT, SCRIPT and Error message, determine what caused the error and how to fix it\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n5. The compiler...\n\nPlease follow these conventions carefully:\n- Decline any tasks that seem dangerous, irreversible, or that you don't understand.\n- Always review the full conversation prior to answering and maintain continuity.\n- If asked for information, just print the information clearly and concisely.\n- If asked to do something, print a concise summary of what you've done as confirmation.\n- If asked a question, respond in a friendly, conversational way. Use programmatically-generated and natural language responses as appropriate.\n- Assume the user would like something concise. For example rather than printing a massive table, filter or summarize it to what's likely of interest.\n- The user will likely not specify exact filenames. Use glob searches when looking for filenames in your SCRIPT.\n- Actively clean up any temporary processes or files you use.\n- When looking through files, use git as available to skip files, and skip hidden files (.env, .git, etc) by default.\n- Let exceptions propagate to the user (rather than catching them in your SCRIPT) so that you can retry.\n- At the user's request, you can inspect and update your configuration file: ~/.rawdog/config.yaml. Changes will take effect after restarting.\n- Feel free to use any common python packages. For example matplotlib, beautifulsoup4, numpy. If the user doesn't have them installed they will be installed automatically with user confirmation.\n- ALWAYS Return your SCRIPT inside of a single pair of ``` delimiters. Only the console output of the first such SCRIPT is visible to the user, so make sure that it's complete and don't bother returning anything else.\n"
    },
    {
        "role": "system",
        "content": "EXAMPLES:\n-------------------------------------------------------------------------------\nPROMPT: Kill the process running on port 3000\n\nSCRIPT:\n```\nimport os\nos.system(\"kill $(lsof -t -i:3000)\")\nprint(\"Process killed\")\n```\n-------------------------------------------------------------------------------\nPROMPT: Rename the photos in this directory with \"nyc\" and their timestamp\n\nSCRIPT:\n```\nimport os\nimport time\nimage_files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]\ndef get_name(f):\n    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime(os.path.getmtime(f)))\n    return f\"nyc_{timestamp}{os.path.splitext(f)[1]}\"\n[os.rename(f, get_name(f)) for f in image_files]\nprint(\"Renamed files\")\n```\n-------------------------------------------------------------------------------\nPROMPT: Summarize my essay\n\nSCRIPT:\n```\nimport glob\nfiles = glob.glob(\"*essay*.*\")\nwith open(files[0], \"r\") as f:\n    print(f.read())\nprint(\"CONTINUE\")\n```\n\nLAST SCRIPT OUTPUT:\n\nJohn Smith\nEssay 2021-09-01\n...\n\nSCRIPT:\n```\nprint(\"The essay is about...\")\n```\n-------------------------------------------------------------------------------\n"
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
        "content": "LAST SCRIPT OUTPUT:\n['nasdaq.csv', 'nasdaq_wrong.csv', 'sp.csv']\nCONTINUE\n"
    },
    {
        "role": "assistant",
        "content": "function_2"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\nNASDAQ CSV Structure:\nDate\tOpen\tHigh\tLow\tClose*\tAdj Close\tVolume\n2023-05-12\t13407.019531\t13427.419922\t13256.559570\t13340.179688\t13340.179688\t4170000000\n2023-05-11\t13376.849609\t13411.700195\t13306.080078\t13389.780273\t13389.780273\t4489490000\n\nS&P CSV Structure:\nDate\tOpen\tHigh\tLow\tClose\tAdj Close\tVolume\n2023-04-06\t4081.15\t4107.32\t4069.84\t4105.02\t4105.02\t3486690000\n2023-04-05\t4094.50\t4099.69\t4072.56\t4090.38\t4090.38\t3968020000\nCONTINUE\n"
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
    print("CONTINUE")


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
    print("CONTINUE")


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


if __name__ == "__main__":
    function_3()
