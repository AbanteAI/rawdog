conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/biobootloader/code/calculator, which IS a git repository.\nThe user's operating system is Darwin\n        ",
    },
    {
        "role": "user",
        "content": "summarize the git diff",
    },
    {
        "role": "assistant",
        "content": '``` \nimport subprocess\n\n# Attempt to capture the output of git diff\ntry:\n    diff_output = subprocess.check_output(["git", "diff"], universal_newlines=True)\n    print(diff_output)\n    print("CONTINUE")\nexcept subprocess.CalledProcessError as e:\n    print("Error running git diff:", e)\n```',
    },
    {
        "role": "user",
        "content": 'LAST SCRIPT OUTPUT:\ndiff --git a/hello_script.py b/hello_script.py\nindex fe57e1f..d0872b1 100644\n--- a/hello_script.py\n+++ b/hello_script.py\n@@ -1 +1,2 @@\n-print("Hello, user!")\n\\ No newline at end of file\n+name = input("What is your name? ")\n+print(f"Hello, {name}!")\n\nCONTINUE\n',
    },
]

metadata = {
    "model": "gpt-4-turbo-preview",
    "cost": "0.0131800000",
    "timestamp": "2024-02-09_12-25-50",
    "log_version": 0.1,
}


def main():
    print(
        "'hello_script.py' was modified. It now prompts the user for their name and uses it when it says hello."
    )


if __name__ == "__main__":
    main()
