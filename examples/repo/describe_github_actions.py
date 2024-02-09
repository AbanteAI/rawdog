conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/jakekoenig/mentat, which IS a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Does this project have github actions set up?"
    },
    {
        "role": "assistant",
        "content": "```\nimport os\n\n# Function to check if GitHub Actions are set up in a project\ndef check_github_actions_setup():\n    # Path to the GitHub Actions directory\n    actions_dir = os.path.join(\".github\", \"workflows\")\n    # Check if the directory exists\n    if os.path.isdir(actions_dir):\n        # List files in the GitHub Actions directory\n        actions_files = os.listdir(actions_dir)\n        if actions_files:\n            print(\"GitHub Actions are set up with the following workflows:\", actions_files)\n        else:\n            print(\"GitHub Actions directory is present but no workflows found.\")\n    else:\n        print(\"GitHub Actions are not set up.\")\n\ncheck_github_actions_setup()\n```"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\nGitHub Actions are set up with the following workflows: ['release.yml', 'benchmarks.yml', 'lint_and_test.yml']\n"
    },
    {
        "role": "user",
        "content": "What do they do?"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0154100000",
    "timestamp": "2024-02-09_01-03-02",
    "log_version": 0.1
}


def main():
    import os

    # Define a function to print the contents of GitHub Actions workflow files
    def print_workflow_contents(workflows):
        for workflow in workflows:
            workflow_path = os.path.join(".github", "workflows", workflow)
            print(f"Contents of {workflow}:\n")
            with open(workflow_path, "r") as file:
                print(file.read())
            print("\n" + "-"*80 + "\n")

    # List of workflow files
    workflow_files = ['release.yml', 'benchmarks.yml', 'lint_and_test.yml']
    print_workflow_contents(workflow_files)


if __name__ == "__main__":
    main()
