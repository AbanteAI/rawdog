# Rawdog 1.0: OLD DOG, NEW TRICKS

Old Dog:
* Natural language CLI
* Agentic: multi-call completions

New Tricks:
- Memory: save functions that work
- 


A function, `result = rawdog('do something')`

```
def rawdog(prompt):
    # Check if a program exists to do the thing
    tricks = remember(prompt)
    i_tricks = await completion(
        'Would any of the following functions complete the task below?'
        'If so, return the index. If not, return None.')

while True:
    program = rawdog(prompt)
    try:
        exec(program)
        if input('Remember how to do this?'):
            learn(prompt, program)
        break
    except Exception:
        if not input('Something went wrong, want me to try again?'):
            break
```



Tools
- message_user: print output to the user
- pause_for_feedback: give control flow back to user
- user_shell: execute something in the user's shell
- private_shell: execute something in a private shell, view output
- view: see contents of a file
- edit: update contents of a text file
- remember: look through preview conversation history
- wait
