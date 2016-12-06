from evaluate_user import evaluate_user

from Tkinter import *
from ScrolledText import ScrolledText
from ttk import Frame, Button, Label, Style
import re

class EvaluatorWindow(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.parent.title("Twitter Judge")
        self.style = Style()
        self.style.theme_use("default")

        output_frame = Frame(self, relief = RIDGE, borderwidth = 1)
        output_frame.pack(anchor = N, fill = BOTH, expand = True)

        output_text = ScrolledText(output_frame)
        self.output_text = output_text
        output_text.pack(fill = BOTH, expand = True)

        input_frame = Frame(self, height = 32)
        input_frame.pack(anchor = S, fill = X, expand = False)

        user_label = Label(input_frame, text = "Enter username:")
        user_label.pack(side = LEFT)
        judge_button = Button(input_frame, text = "Judge!", command = lambda: judge(user_entry.get(), self))
        judge_button.pack(side = RIGHT)
        user_entry = Entry(input_frame)
        user_entry.pack(fill = X, padx = 5, pady = 5, expand = True)

        self.pack(fill = BOTH, expand = True)


    # Write results to the output as if this is an open file
    def write(self, output):
        self.output_text.insert(INSERT, output)
        self.output_text.see('insert')
        self.output_text.update()
        return len(output)


def judge(user_id, output_file):
    # strip away the '@' if the user included it
    user_id = re.sub('@','', user_id)
    # Notify the user if the attempt failed for any reason
    if user_id != 'exit' and evaluate_user(user_id, output_file) == 1:
        print("An error occured.\n")

def main():

    window = Tk()
    window.geometry("450x600")
    app = EvaluatorWindow(window)
    window.mainloop()

if __name__ == "__main__":
    main()