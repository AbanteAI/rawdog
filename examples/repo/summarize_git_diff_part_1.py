conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/biobootloader/code/calculator, which IS a git repository.\nThe user's operating system is Darwin\n        ",
    },
    {"role": "user", "content": "summarize the git diff"},
]

metadata = {
    "model": "gpt-4-turbo-preview",
    "cost": "0.0119500000",
    "timestamp": "2024-02-09_12-25-47",
    "log_version": 0.1,
}


def main():
    import subprocess

    # Capture the output of git diff so I can see it to write the summary
    try:
        diff_output = subprocess.check_output(["git", "diff"], universal_newlines=True)
        print(diff_output)
        print("CONTINUE")
    except subprocess.CalledProcessError as e:
        print("Error running git diff:", e)


if __name__ == "__main__":
    main()
