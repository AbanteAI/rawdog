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
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/jake/market/data, which is NOT a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "nasdaq.csv and sp.csv have slightly different date and number formats. Can you change sp.csv to have the same format as nasdaq.csv?"
    },
    {
        "role": "assistant",
        "content": "function_1"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\nNasdaq File Sample:\n    Date\\tOpen\\tHigh\\tLow\\tClose*\\tAdj Close\\tVolume\n0  2023-05-12\\t13407.019531\\t13427.419922\\t13256....\n1  2023-05-11\\t13376.849609\\t13411.700195\\t13306....\n2  2023-05-10\\t13308.410156\\t13384.419922\\t13204....\n3  2023-05-09\\t13228.639648\\t13254.809570\\t13193....\n4  2023-05-08\\t13247.089844\\t13302.429688\\t13193....\n\nSP File Sample:\n                                                                          Date\\tOpen\\tHigh\\tLow\\tClose*\\tAdj Close**\\tVolume\nApr 06 2023\\t4 081.15\\t4 107.32\\t4 069.84\\t4 105.02\\t4 105.02\\t3 486 690                                                  0 \nApr 05 2023\\t4 094.50\\t4 099.69\\t4 072.56\\t4 090.38\\t4 090.38\\t3 968 20                                                   0 \nApr 04 2023\\t4 128.03\\t4 133.13\\t4 086.87\\t4 100.60\\t4 100.60\\t4 227 800                                                  0 \nApr 03 2023\\t4 102.20\\t4 127.66\\t4 098.79\\t4 124.51\\t4 124.51\\t4 234 700                                                  0 \nMar 31 2023\\t4 056.18\\t4 110.75\\t4 056.18\\t4 109.31\\t4 109.31\\t4 525 120                                                  0 \n\n"
    },
    {
        "role": "assistant",
        "content": "function_2"
    }
]

metadata = {
    "timestamp": "2024-02-09_00-52-03",
    "log_version": "0.2",
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0286200000",
    "Note": "I touched up the response to have prints, fix the column name, and remove commas instead of spaces"
}


def function_1():
    import pandas as pd

    # Reading the files to compare their formats
    nasdaq_df = pd.read_csv("nasdaq.csv")
    sp_df = pd.read_csv("sp.csv")

    # Inspecting the first few rows to understand the date and number formats
    print("Nasdaq File Sample:")
    print(nasdaq_df.head())
    print("\nSP File Sample:")
    print(sp_df.head())
    print("\nCONTINUE")


def function_2():
    import pandas as pd
    from datetime import datetime

    print("I will make the following changes to sp.csv:")
    print("1. Convert date from 'MMM DD, YYYY' to 'YYYY-MM-DD'")
    print("2. Remove commas from numbers")
    print("3. Rename Adj Close** column to Adj Close")

    # Function to convert date from 'MMM DD YYYY' to 'YYYY-MM-DD'
    def convert_date(date_str):
        return datetime.strptime(date_str, '%b %d, %Y').strftime('%Y-%m-%d')

    # Function to clean number formats by removing commas (used as thousands separators)
    def clean_number(number_str):
        return number_str.replace(",", "").replace("\t", "")

    # Read sp.csv with proper delimiter and converters to handle date and number formatting
    sp_df = pd.read_csv(
        "sp.csv",
        delimiter='\t',
        converters={
            0: convert_date,  # Assuming the first column is 'Date'
            1: clean_number,  # Assuming remaining columns are numbers where spaces can appear
            2: clean_number,
            3: clean_number,
            4: clean_number,
            5: clean_number,
            6: clean_number,
        },
        header=0,
        names=['Date', 'Open', 'High', 'Low', 'Close*', 'Adj Close', 'Volume']  # Standardizing column names
    )

    # Write the cleaned data back to sp.csv matching the nasdaq.csv format
    sp_df.to_csv("sp.csv", index=False, sep='\t')

    print("sp.csv format has been updated to match nasdaq.csv.")

    print("TASK COMPLETE")


if __name__ == "__main__":
    function_2()
