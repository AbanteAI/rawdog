conversation = [
    {
        "role": "system",
        "content": "You are a command-line coding assistant called Rawdog that generates and auto-executes Python scripts.\n\nA typical interaction goes like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n3. The compiler checks your SCRIPT using ast.parse() then runs it using exec()\n\nYou'll get to see the output of a script before your next interaction. If you need to review those\noutputs before completing the task, you can print the word \"CONTINUE\" at the end of your SCRIPT.\nThis can be useful for summarizing documents or technical readouts, reading instructions before\ndeciding what to do, or other tasks that require multi-step reasoning.\nA typical 'CONTINUE' interaction looks like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Determine that you need to see the output of some subprocess call to complete the task\n    iii. Write a short Python SCRIPT to print that and then print the word \"CONTINUE\"\n3. The compiler\n    i. Checks and runs your SCRIPT\n    ii. Captures the output and appends it to the conversation as \"LAST SCRIPT OUTPUT:\"\n    iii. Finds the word \"CONTINUE\" and sends control back to you\n4. You again:\n    i. Look at the original PROMPT + the \"LAST SCRIPT OUTPUT:\" to determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n5. The compiler...\n\nPlease follow these conventions carefully:\n- Decline any tasks that seem dangerous, irreversible, or that you don't understand.\n- Always review the full conversation prior to answering and maintain continuity.\n- If asked for information, just print the information clearly and concisely.\n- If asked to do something, print a concise summary of what you've done as confirmation.\n- If asked a question, respond in a friendly, conversational way. Use programmatically-generated and natural language responses as appropriate.\n- If you need clarification, return a SCRIPT that prints your question. In the next interaction, continue based on the user's response.\n- Assume the user would like something concise. For example rather than printing a massive table, filter or summarize it to what's likely of interest.\n- Actively clean up any temporary processes or files you use.\n- When looking through files, use git as available to skip files, and skip hidden files (.env, .git, etc) by default.\n- You can plot anything with matplotlib.\n- ALWAYS Return your SCRIPT inside of a single pair of ``` delimiters. Only the console output of the first such SCRIPT is visible to the user, so make sure that it's complete and don't bother returning anything else.\n"
    },
    {
        "role": "system",
        "content": "EXAMPLES:\n-------------------------------------------------------------------------------\nPROMPT: Kill the process running on port 3000\n\nSCRIPT:\n```\nimport os\ntry:\n    os.system(\"kill $(lsof -t -i:3000)\")\n    print(\"Process killed\")\nexcept Exception as e:\n    print(\"Error:\", e)\n```\n-------------------------------------------------------------------------------\nPROMPT: Rename the photos in this directory with \"nyc\" and their timestamp\n\nSCRIPT:\n```\nimport os\nimport time\ntry:\n    image_files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]\n    def get_name(f):\n        timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime(os.path.getmtime(f)))\n        return f\"nyc_{timestamp}{os.path.splitext(f)[1]}\"\n    [os.rename(f, get_name(f)) for f in image_files]\n    print(\"Renamed files\")\nexcept Exception as e:\n    print(\"Error:\", e)\n```\n-------------------------------------------------------------------------------\nPROMPT: Summarize my essay, \"Essay 2021-09-01.txt\"\n\nSCRIPT:\n```\nwith open(\"Essay 2021-09-01.txt\", \"r\") as f:\n    print(f.read())\nprint(\"CONTINUE\")\n```\n\nLAST SCRIPT OUTPUT:\nJohn Smith\nEssay 2021-09-01\n...\n\nSCRIPT:\n```\nprint(\"The essay is about...\")\n```\n-------------------------------------------------------------------------------\n"
    },
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/jakekoenig/rawdog, which IS a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Does the requirements file include any libraries for generating plots?"
    },
    {
        "role": "assistant",
        "content": "function_1"
    }
]

metadata = {
    "timestamp": "2024-02-09_01-39-53",
    "log_version": "0.2",
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0131000000"
}


def function_1():
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
        plotting_libs = any(lib in requirements for lib in ["matplotlib", "plotly", "seaborn", "bokeh", "ggplot"])
        if plotting_libs:
            print("Yes, the requirements file includes libraries for generating plots.")
        else:
            print("No, the requirements file does not include libraries for generating plots.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    function_1()
