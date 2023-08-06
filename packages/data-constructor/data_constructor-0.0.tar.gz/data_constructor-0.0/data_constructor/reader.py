import os
def reader(file):
    os.chdir('../old')
    f = open(file, 'r')
    print(f.read())