#!/usr/bin/env python
import argparse
import time

from openai import OpenAI

client = OpenAI()

parser = argparse.ArgumentParser(description="Fine tuning GPT-3")
parser.add_argument(
    "--file", type=str, default=None, help="Data file to use for fine tuning"
)
args = parser.parse_args()

f = client.files.create(file=open(args.file, "rb"), purpose="fine-tune")

print("Uploaded: ", f)
while True:
    time.sleep(30)
    f = client.files.retrieve(f.id)
    if f.status == "processed":
        break

print(client.fine_tuning.jobs.create(training_file=f.id, model="gpt-3.5-turbo-1106"))
