conversation = [
    {
        "role": "user",
        "content": "What's the first paragraph of the wikipedia page on fourier transformations?"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0130300000",
    "timestamp": "2024-02-07_12-55-57",
    "log_version": 0.1
}


def main():
    import requests
    from bs4 import BeautifulSoup

    # Fetch the content of the Wikipedia page on Fourier transformations
    url = "https://en.wikipedia.org/wiki/Fourier_transform"
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first paragraph under the 'mw-parser-output' class which typically contains the article content
    first_paragraph = soup.find("div", class_="mw-parser-output").p.get_text()

    print(first_paragraph)


if __name__ == "__main__":
    main()
