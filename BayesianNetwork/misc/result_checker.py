import json
import sys

file_one = None
file_two = None
success = True
with open(sys.argv[1], "r") as f:
    file_one = json.load(f)
with open(sys.argv[2], "r") as f:
    file_two = json.load(f)

for i in range(len(file_one)):
    file_one[i]["answer"] = "{:.10f}".format(file_one[i]["answer"])
    file_two[i]["answer"] = "{:.10f}".format(file_two[i]["answer"])
    if file_one[i] != file_two[i]:
        print("DIFFERENT")
        print(file_one[i])
        print(file_two[i])
        success = False
        break

if success:
    print("SUCCESS")