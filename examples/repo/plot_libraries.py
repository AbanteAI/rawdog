conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/jakekoenig/rawdog, which IS a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Does the requirements file include any libraries for generating plots?"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0131000000",
    "timestamp": "2024-02-09_01-39-53",
    "log_version": 0.1
}


def main():
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
    main()
