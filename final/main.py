import tkinter
from tkinter import filedialog

def main():
    root = tkinter.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
    print("\n선택된 폴더", dir_path)
    while True:
        print("hi")
        



if __name__ == "__main__":
    main()