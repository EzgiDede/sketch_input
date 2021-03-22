from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter.messagebox import showinfo
import qd_data_ndjson_by_irem
import sketch_input_interface
import shutil
import to_npz
import os

def erase_previous_files():
    erase_content_of_file("./interface_ndjson_files/")
    erase_content_of_file("./interface_npz_files/")


def erase_content_of_file(folder):
    # Taken from: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def convert_to_npz():
    to_npz.ndjson_to_npz("./interface_ndjson_files/", "./interface_npz_files/")

def self_draw_clicked():
    sketch_input_interface.main()


def browse():
    root.sourceFile = filedialog.askopenfilename(parent=root, initialdir="/", title='Please select a directory')
    print(root.sourceFile)
    shutil.copyfile(root.sourceFile, "./interface_ndjson_files/chosen_simplified_qd.ndjson")


def get_subsample(i, categories, num):
    # Command to check randomness of categories which will be taken from QD
    if i == 0:  # random checkbox is unchecked
        qd_data_ndjson_by_irem.get_selected_qd_categories_subsample(categories, num)
    else:  # random is checked
        qd_data_ndjson_by_irem.get_random_qd_categories_subsample(num)


def get_from_qd_clicked():
    # opens a new frame to arrange categories and number of drawings
    sketch_frame.pack_forget()  # This must change because the back button will be added

    is_random_checked = IntVar()  # used in checkbutton 1 for true 0 for false

    # Frame
    qd_frame = LabelFrame(root, text="Quick Draw Data", padx=50, pady=80)
    qd_frame.pack()

    # Entry to take wanted number of drawings
    Label(qd_frame, text='Number of drawings you want: ').grid(columnspan=2, column=0, row=0)
    drawings_num = Entry(qd_frame)
    drawings_num.insert(0, "3")
    drawings_num.grid(columnspan=2, column=0, row=1)

    Label(qd_frame, text='Selected Categories:').grid(column=1, row=2)
    selected_categories_listbox = tk.Listbox(qd_frame, height=20, selectmode='extended')
    selected_categories_listbox.grid(column=1, row=3, padx=5)

    def done():
        get_subsample(is_random_checked.get(),
                      list(selected_categories_listbox.get(0, selected_categories_listbox.size())),
                      int(drawings_num.get()))
        selected_categories_listbox.delete(0, selected_categories_listbox.size())

    def back():
        sketch_frame.pack()
        qd_frame.destroy()

    # Done button to commence the action
    done_button = Button(qd_frame, text='Done',
                         command=done)
    done_button.grid(column=0, row=6)

    # Back button to return back
    back_button = Button(qd_frame, text='Back',
                         command=back)
    back_button.grid(column=1, row=6)

    # Random check button to enable random functionality
    random = Checkbutton(qd_frame, text="Random", variable=is_random_checked, onvalue=1, offvalue=0)
    random.grid(columnspan=2, column=0, row=5)

    # listbox for categories
    Label(qd_frame, text='Categories to add:').grid(column=0, row=2)
    categories_list = tk.StringVar(value=qd_data_ndjson_by_irem.open_and_read("./googleqd_categories"))
    categories_listbox = tk.Listbox(qd_frame, listvariable=categories_list, height=20, selectmode='extended')
    categories_listbox.grid(column=0, row=3)

    def select_category():
        # get selected indices
        selected_indices = categories_listbox.curselection()
        for index in selected_indices:
            if not categories_listbox.get(index) in selected_categories_listbox.get(0,
                                                                                    selected_categories_listbox.size()):
                selected_categories_listbox.insert(0, categories_listbox.get(index))

    def deselect_category():
        # delete selected categories
        selected_indices = selected_categories_listbox.curselection()
        for index in selected_indices:
            selected_categories_listbox.delete(index)

    # select button to add selected categories
    select_button = Button(qd_frame, text='Select',
                           command=select_category)
    select_button.grid(column=0, row=4)

    # deselect button to remove selected categories
    remove_button = Button(qd_frame, text='Remove',
                           command=deselect_category)
    remove_button.grid(column=1, row=4)

def done_clicked():
    sketch_frame.pack_forget()

    # Frame
    done_frame = LabelFrame(root, text="Embedding", padx=50, pady=80)
    done_frame.pack()

    Label(done_frame, text='Select the operation: ').grid(column=0, row=0)

    ndjson_button = Button(done_frame, text='Continuous save as ndjson') #command eklenecek
    ndjson_button.grid(column=0, row=1)

    to_npz_button = Button(done_frame, text='Continuous save as npz', command = convert_to_npz)
    to_npz_button.grid(column=1, row=1)

    tokdict_button = Button(done_frame, text='TokDict save as npz')  # command eklenecek
    tokdict_button.grid(column=2, row=1)

    def back():
        sketch_frame.pack()
        done_frame.destroy()

    # Back button to return back
    back_button = Button(done_frame, text='Back',
                         command=back)
    back_button.grid(column=3, row=1)

root = tk.Tk()
erase_previous_files()
root.title("Encoder")
sketch_frame = LabelFrame(root, text="What do you want to do?", padx=50, pady=30)
sketch_frame.pack(padx=100, pady=40)

draw_btn = Button(sketch_frame, text="Draw!", fg='blue', command=self_draw_clicked)
draw_btn.pack()

qd_btn = Button(sketch_frame, text="Get sketch from Quick Draw", fg='blue', command=get_from_qd_clicked)
qd_btn.pack()

browse_btn = Button(sketch_frame, text="Get sketch from your computer", fg='blue', command=browse)
browse_btn.pack()

done_btn = Button(sketch_frame, text="Done", fg='red', command=done_clicked)
done_btn.pack()

root.mainloop()
