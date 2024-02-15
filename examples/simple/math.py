conversation = [
    {
        "role": "system",
        "content": "You are a command-line coding assistant called Rawdog that generates and auto-executes Python scripts.\n\nA typical interaction goes like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n3. The compiler checks your SCRIPT using ast.parse() then runs it using exec()\n\nYou'll get to see the output of a script before your next interaction. If you need to review those\noutputs before completing the task, you can print the word \"CONTINUE\" at the end of your SCRIPT.\nThis can be useful for summarizing documents or technical readouts, reading instructions before\ndeciding what to do, or other tasks that require multi-step reasoning.\nA typical 'CONTINUE' interaction looks like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Determine that you need to see the output of some subprocess call to complete the task\n    iii. Write a short Python SCRIPT to print that and then print the word \"CONTINUE\"\n3. The compiler\n    i. Checks and runs your SCRIPT\n    ii. Captures the output and appends it to the conversation as \"LAST SCRIPT OUTPUT:\"\n    iii. Finds the word \"CONTINUE\" and sends control back to you\n4. You again:\n    i. Look at the original PROMPT + the \"LAST SCRIPT OUTPUT:\" to determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n5. The compiler...\n\nPlease follow these conventions carefully:\n- Decline any tasks that seem dangerous, irreversible, or that you don't understand.\n- Always review the full conversation prior to answering and maintain continuity.\n- If asked for information, just print the information clearly and concisely.\n- If asked to do something, print a concise summary of what you've done as confirmation.\n- If asked a question, respond in a friendly, conversational way. Use programmatically-generated and natural language responses as appropriate.\n- If you need clarification, return a SCRIPT that prints your question. In the next interaction, continue based on the user's response.\n- Assume the user would like something concise. For example rather than printing a massive table, filter or summarize it to what's likely of interest.\n- Actively clean up any temporary processes or files you use.\n- When looking through files, use git as available to skip files, and skip hidden files (.env, .git, etc) by default.\n- At the user's request, you can inspect and update your configuration file: ~/.rawdog/config.yaml. Changes will take effect after restarting.\n- Feel free to use any common python packages. For example matplotlib, beautifulsoup4, numpy. If the user doesn't have them installed they will be installed automatically with user confirmation.\n- ALWAYS Return your SCRIPT inside of a single pair of ``` delimiters. Only the console output of the first such SCRIPT is visible to the user, so make sure that it's complete and don't bother returning anything else.\n"
    },
    {
        "role": "system",
        "content": "EXAMPLES:\n-------------------------------------------------------------------------------\nPROMPT: Kill the process running on port 3000\n\nSCRIPT:\n```\nimport os\nos.system(\"kill $(lsof -t -i:3000)\")\nprint(\"Process killed\")\n```\n-------------------------------------------------------------------------------\nPROMPT: Rename the photos in this directory with \"nyc\" and their timestamp\n\nSCRIPT:\n```\nimport os\nimport time\nimage_files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]\ndef get_name(f):\n    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime(os.path.getmtime(f)))\n    return f\"nyc_{timestamp}{os.path.splitext(f)[1]}\"\n[os.rename(f, get_name(f)) for f in image_files]\nprint(\"Renamed files\")\n```\n-------------------------------------------------------------------------------\nPROMPT: Summarize my essay\n\nSCRIPT:\n```\nimport glob\nfiles = glob.glob(\"*essay*.*\")\nwith open(files[0], \"r\") as f:\n    print(f.read())\nprint(\"CONTINUE\")\n```\n\nLAST SCRIPT OUTPUT:\n\nJohn Smith\nEssay 2021-09-01\n...\n\nSCRIPT:\n```\nprint(\"The essay is about...\")\n```\n-------------------------------------------------------------------------------\n"
    },
    {
        "role": "system",
        "content": "Today's date is 2024-02-14 13:33:57.\nThe current working directory is /Users/jakekoenig/rawdog, which IS a git repository.\nThe user's operating system is Darwin.\nThe contents of the current working directory are:\n2024-02-05 07:56:58      11339 bytes LICENSE\n2024-02-14 13:22:51         32 bytes requirements.txt\n2024-02-07 09:47:43          4 items /dist\n2024-02-14 13:22:51        630 bytes pyproject.toml\n2024-02-13 09:38:11      60746 bytes training_data.jsonl\n2024-02-05 07:56:58          1 items /rawdog\n2024-02-13 08:58:21       5247 bytes script_2024-02-13_08-58-21.py\n2024-02-14 08:47:33        308 bytes todo\n2024-02-13 01:40:23       3081 bytes README.md\n2024-02-05 07:57:14         45 bytes .gitignore\n2024-02-07 09:47:28          5 items /.env\n2024-02-14 13:26:01         13 items /examples\n2024-02-13 13:19:10          3 items /scripts\n2024-02-14 09:25:18       3380 bytes octagon.png\n2024-02-14 13:22:51         13 items /.git\n2024-02-09 02:29:04      58388 bytes old_training_data.jsonl\n2024-02-14 08:46:44          4 items /my_env\n2024-02-05 07:56:58          1 items /src\nThe last commit message is: Pip install not found modules (#61)\n\nIf the llm tries to use a module that cannot be found then prompt the\r\nuser to install it with pip.\r\nMisc:\r\n* Moved execution specific utils from utils to execute_script\r\n* Removed almost all the requirements\r\n* Give errors from the script to the llm (was broken by move to subprocess)\r\n\r\nCo-authored-by: biobootloader <128252497+biobootloader@users.noreply.github.com>\r\n\r\n---------\r\n\r\nCo-authored-by: biobootloader <128252497+biobootloader@users.noreply.github.com>"
    },
    {
        "role": "user",
        "content": "1+9*3-11+7^7+(1+1)*(2+2)"
    },
    {
        "role": "assistant",
        "content": "function_1"
    }
]

metadata = {
    "timestamp": "2024-02-14_13-34-27",
    "log_version": 0.2,
    "model": "gpt-4",
    "cost": "0.0525300000"
}


def function_1():
    print(1 + 9 * 3 - 11 + 7 ** 7 + (1+1) * (2+2))


if __name__ == "__main__":
    function_1()
