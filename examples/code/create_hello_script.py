conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/biobootloader/code/calculator, which is NOT a git repository.\nThe user's operating system is Darwin\n        ",
    },
    {"role": "user", "content": "make me a script that says hello to the user"},
]

metadata = {
    "model": "gpt-4-turbo-preview",
    "cost": "0.0118700000",
    "timestamp": "2024-02-09_12-19-26",
    "log_version": 0.1,
    "note": "non-finetuned rawdog just prints it directly, instead of writing a file. to generate this I added more detail to what I asked, which I removed here.",
}


def main():
    filename = "hello_script.py"
    content = """print("Hello, user!")"""

    try:
        with open(filename, "w") as file:
            file.write(content)
        print(f"Script written to {filename}")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
