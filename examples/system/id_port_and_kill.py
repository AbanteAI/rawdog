conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-08.\nThe current working directory is /Users/jakekoenig/rawdog, which IS a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Can you tell me what process is using port 8050?"
    },
    {
        "role": "assistant",
        "content": "```\nimport subprocess\n\ntry:\n    result = subprocess.check_output([\"lsof\", \"-i\", \":8050\"], stderr=subprocess.STDOUT).decode()\n    if result:\n        print(\"Process using port 8050:\\n\", result.split(\"\\n\")[1].split()[0], \"-\", result.split(\"\\n\")[1].split()[1])\n    else:\n        print(\"No process is currently using port 8050.\")\nexcept Exception as e:\n    print(\"Error:\", e)\n```"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\nProcess using port 8050:\n Python - 57756\n"
    },
    {
        "role": "user",
        "content": "Can you kill that process?"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0123700000",
    "timestamp": "2024-02-07_12-33-37",
    "log_version": 0.1
}


def main():
    import os

    try:
        os.system("kill 57756")
        print("Process 57756 killed.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
