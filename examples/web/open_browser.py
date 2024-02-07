conversation = [
    {
        "role": "user",
        "content": "Can you open github in a browser searching for projects using sqlite3?"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0109300000",
    "timestamp": "2024-02-07_13-03-38",
    "log_version": 0.1
}


def main():
    import webbrowser

    webbrowser.open("https://github.com/search?q=sqlite3")
    print("Opened GitHub in browser with search for projects using sqlite3.")


if __name__ == "__main__":
    main()
