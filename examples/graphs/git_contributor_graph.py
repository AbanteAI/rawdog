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

    print("TASK COMPLETE")


if __name__ == "__main__":
    function_1()
