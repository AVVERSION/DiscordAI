#THIS CODE WORKS! For a generator type of reply, leave this code as it is, for a regular reply, remove/comment lines 7 and 8, remove ', streaming=True' from line 6 and uncomment line 9

from gpt4all import GPT4All
model = GPT4All("llama-2-7b-chat.ggmlv3.q4_0.bin", model_path="/workspaces/DiscordAI/")
print("Model loaded")
output = model.generate("How to make popcorns?", streaming=True)
for i in output:
    print(i, end="")
# print(output)