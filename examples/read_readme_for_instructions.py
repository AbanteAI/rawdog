# PROMPT INFORMATION
conversation = [
    {
        "role": "user",
        "content": "PROMPT: Can you read the readme and use the information to change rawdog to use mixtral with ollama?"
    }
]
metadata = {
    "model": "gpt-4",
    "cost": "0.0321300000",
    "timestamp": "2024-02-06_13-53-06"
}
# START SCRIPT
with open("README.md", "r") as f:
    guide_contents = f.read()
print(guide_contents)
print("CONTINUE")