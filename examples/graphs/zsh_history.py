conversation = [
    {
        "role": "user",
        "content": "make a graph showing my relative frequency of command line programs"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0194200000",
    "timestamp": "2024-02-07_12-04-14",
    "log_version": 0.1
}


def main():
    import os
    import matplotlib.pyplot as plt
    from collections import Counter

    # Use the history command to get a list of used commands
    # Assuming user's shell history command is compatible and contains relevant history
    try:
        # Read the history file directly for shells like zsh, this might change based on the shell used.
        # Common history files: ~/.bash_history for bash, ~/.zsh_history for zsh
        with open(os.path.expanduser('~/.zsh_history'), 'r') as history_file:
            commands = history_file.readlines()

        # Extract the command part (first word) from each line
        commands = [line.strip().split(';')[-1].split(' ')[0] for line in commands if ';' in line]  # Adjust for zsh history format

        # Count occurrences of each command
        command_counts = Counter(commands)

        # Sort commands by frequency
        sorted_commands = sorted(command_counts.items(), key=lambda item: item[1], reverse=True)

        # Considering only the top 10 frequent commands to keep the graph readable
        top_commands = dict(sorted_commands[:10])

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.bar(top_commands.keys(), top_commands.values(), color='skyblue')
        plt.xlabel('Command')
        plt.ylabel('Frequency')
        plt.title('Top 10 Most Used Command Line Programs')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
