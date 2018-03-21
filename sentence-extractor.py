import os.path


listOfFiles = [f for f in os.listdir("input") if os.path.isfile(f)]
print(listOfFiles)