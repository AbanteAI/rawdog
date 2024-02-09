conversation = [
    {
        "role": "system",
        "content": "Today's date is 2024-02-09.\nThe current working directory is /Users/jakekoenig/rawdog, which IS a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Can you import all the classes defined in src/rawdog/ to its __init__.py?"
    }
]

metadata = {
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0185800000",
    "timestamp": "2024-02-09_02-03-37",
    "log_version": 0.1
}


def main():
    import os
    import ast

    # Define the source directory and target __init__.py
    src_directory = "src/rawdog"
    init_file = os.path.join(src_directory, "__init__.py")

    # List all the .py files in src/rawdog/ directory
    src_files = [f for f in os.listdir(src_directory) if f.endswith('.py') and f != "__init__.py"]

    # Prepare a list to hold import statements
    imports = []

    # Extract class names from each file
    for src_file in src_files:
        full_path = os.path.join(src_directory, src_file)
        with open(full_path, "r") as file:
            file_content = file.read()
            try:
                parsed_ast = ast.parse(file_content)
                for node in ast.walk(parsed_ast):
                    if isinstance(node, ast.ClassDef):
                        # If a class name is found, prepare the import statement
                        class_name = node.name
                        module_name = src_file[:-3]  # Remove .py extension
                        imports.append(f"from .{module_name} import {class_name}")
            except SyntaxError:
                continue

    # Write the import statements to __init__.py
    if imports:
        with open(init_file, "w") as init_f:
            for imp in imports:
                init_f.write(imp + "\n")

    print("Classes imported to __init__.py.")


if __name__ == "__main__":
    main()
