import os.path

inputPath = os.path.join(os.getcwd(), "input")

listOfFiles = [os.path.join(inputPath, f) for f in os.listdir(inputPath) if os.path.isfile(os.path.join(inputPath, f))]

for f in listOfFiles:
    print(f)
    with open(f, 'r') as content_file:
        content = content_file.read()
        print(content)
