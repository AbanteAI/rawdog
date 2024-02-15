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
        "content": "Today's date is 2024-02-08.\nThe current working directory is /Users/jakekoenig/rawdog, which IS a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Make a scatter plot of all the contributers to the current repo where the x axis is how many commits, the y axis is how many lines and the color is recency of last commit"
    },
    {
        "role": "assistant",
        "content": "function_1"
    }
]

metadata = {
    "timestamp": "2024-02-07_11-57-41",
    "log_version": "0.2",
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0241300000"
}


def function_1():
    import subprocess
    import matplotlib.pyplot as plt
    import datetime

    # Extracting the contributors' names, their commits count, and the dates of their last commit
    result = subprocess.run(
        ['git', 'shortlog', '-sn', '--all'],
        stdout=subprocess.PIPE, text=True
    )
    contributors = [line.split('\t') for line in result.stdout.strip().split('\n')]

    commit_data = {}
    for commits, name in contributors:
        commits = commits.strip()
        # Counting the lines contributed by each contributor
        lines_result = subprocess.run(['git', 'log', '--author=' + name, '--pretty=tformat:', '--numstat'], stdout=subprocess.PIPE, text=True)
        lines_added = sum([int(line.split()[0]) for line in lines_result.stdout.strip().split('\n') if line])

        # Finding the date of the last commit by each contributor
        date_result = subprocess.run(['git', 'log', '--author=' + name, '--format=%at', '-1'], stdout=subprocess.PIPE, text=True)
        last_commit_date = datetime.datetime.fromtimestamp(int(date_result.stdout.strip()))
        last_commit_recency = (datetime.datetime.now() - last_commit_date).days

        commit_data[name] = {
            'commits': int(commits),
            'lines': lines_added,
            'recency': last_commit_recency,
        }

    # Preparing data for the scatter plot
    names = list(commit_data.keys())
    commits = [commit_data[name]['commits'] for name in names]
    lines = [commit_data[name]['lines'] for name in names]
    recency = [commit_data[name]['recency'] for name in names]

    # Convert recency to colors
    max_recency = max(recency)
    colors = [255 - (r/max_recency)*255 for r in recency]

    fig, ax = plt.subplots()
    scatter = ax.scatter(commits, lines, c=colors, cmap='cool')

    # Creating a color bar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Days since last commit (more recent - cooler)')

    ax.set_xlabel('Number of commits')
    ax.set_ylabel('Number of lines contributed')
    ax.set_title('Contributor Activity in Current Repo')

    plt.show()


if __name__ == "__main__":
    function_1()
