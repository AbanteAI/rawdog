conversation = [
    {
        "role": "user",
        "content": "Can you make my most recent screenshot greyscale?"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0153300000",
    "timestamp": "2024-02-07_12-41-50",
    "log_version": 0.1,
    "note": "I partially wrote this one because gpt likes to like in the current directory for screenshots. Not where macos puts them, the Desktop."
}


def main():
    import os
    from PIL import Image
    import sys

    # Retrieve all screenshot files
    desktop = os.path.expanduser("~/Desktop")
    screenshot_files = [os.path.join(desktop, f) for f in os.listdir(desktop) if f.lower().startswith('screenshot') and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not screenshot_files:
        print("No screenshot files found.")
        sys.exit()

    # Sort files by modified time, most recent first
    screenshot_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Load the most recent screenshot
    try:
        image = Image.open(screenshot_files[0])
        # Convert to greyscale
        grey_image = image.convert('L')
        grey_image_path = screenshot_files[0][:-4] + "_greyscale" + screenshot_files[0][-4:]
        grey_image.save(grey_image_path)
        print(f"Converted {screenshot_files[0]} to greyscale.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
