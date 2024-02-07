conversation = [
    {
        "role": "user",
        "content": "Make a scatter plot of all the contributers to the current repo where the x axis is how many commits, the y axis is how many lines and the color is recency of last commit"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0241300000",
    "timestamp": "2024-02-07_11-57-41",
    "log_version": 0.1
}


def main():
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


if __name__ == "__main__":
    main()
