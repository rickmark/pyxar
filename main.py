# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from pyxar.reader import *


def main(file):
    reader = XarReader(open(file, "rb"))
    for file in reader.files:
        print(f"{file.id} {file.name}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('/Users/rickmark/Downloads/InstallAssistant.pkg')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
