conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-08.\nThe current working directory is /Users/jakekoenig/rawdog, which IS a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "can you draw the mandelbrot set?"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0153600000",
    "timestamp": "2024-02-07_12-12-09",
    "log_version": 0.1
}


def main():
    import numpy as np
    import matplotlib.pyplot as plt

    def mandelbrot(c, max_iter):
        z = 0
        n = 0
        while abs(z) <= 2 and n < max_iter:
            z = z*z + c
            n += 1
        return n

    width, height = 800, 600
    max_iter = 30

    x = np.linspace(-2.5, 1, width)
    y = np.linspace(-1, 1, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y

    Z = np.vectorize(mandelbrot)(C, max_iter)

    plt.imshow(Z, cmap='hot', extent=(-2.5, 1, -1, 1))
    plt.colorbar()
    plt.title('Mandelbrot Set')
    plt.show()


if __name__ == "__main__":
    main()
