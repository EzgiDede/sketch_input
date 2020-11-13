import numpy as np
from sklearn.manifold import TSNE
import os
import statistics
from quickdraw import QuickDrawData
import cv2 as cv2
from scipy.spatial import distance as dstnc
import PIL.Image
import tkinter as tk
from tkinter import *

global label1, label2, label3, listbox1, listbox2, listbox3, entry, button

directory = "./embeddings_dir/"

all_embeddings = []  # a list of tuples (key_id , embedding_vector, class_name)
latent_space = np.zeros((1, 128))
class_list = []
id_list = []
id_vector = {}
latent_dictionary = dict()
the_dict = {}

for filename in os.listdir(directory):
    if filename.endswith("embeddings_new.npz"):
        file_name = filename
        embeddings = np.load(directory + file_name, allow_pickle=True, encoding="latin1")
        for embedding in embeddings["embeddings"]:
            embed_vector = embedding[0]
            key_id = embedding[1]
            id_list.append(key_id)
            class_name_raw = embedding[2]
            class_name = class_name_raw.split(str(key_id))[0]

            latent_space = np.concatenate((latent_space, embed_vector))
            class_list.append(class_name)

latent_space = latent_space[1:, :]
latent_space_tsne = TSNE(n_components=2).fit_transform(latent_space)

for i in range(len(latent_space_tsne)):
    id_vector[id_list[i]] = [(latent_space_tsne[i, :])[0], (latent_space_tsne[i, :])[1]]

for i in range(len(class_list)):
    label = class_list[i]
    x_float = (latent_space_tsne[i, :])[0]
    y_float = (latent_space_tsne[i, :])[1]

    if label not in latent_dictionary.keys():
        latent_dictionary[label] = [[x_float], [y_float]]
    else:
        old_value_list = latent_dictionary[label]
        old_value_list[0].append(x_float)
        old_value_list[1].append(y_float)
        latent_dictionary[label] = old_value_list

class_keys = list(latent_dictionary.keys())

for i in range(len(class_keys)):
    the_x = statistics.mean(latent_dictionary[class_keys[i]][0])
    the_y = statistics.mean(latent_dictionary[class_keys[i]][1])
    the_dict[class_keys[i]] = [the_x, the_y]


def find(different_object, the_object, closer, K):
    # closer can be True or False. If True, it means closest. If False, it means farthest.
    the_point = the_dict.get(the_object)
    distance = []
    coordinates = latent_dictionary.get(different_object)

    for i in range(len(coordinates[0])):
        xy = [coordinates[0][i], coordinates[1][i]]
        dist = dstnc.euclidean(the_point, xy)
        distance.append(dist)

    for M in range(K):
        if closer:
            the_distance = min(distance)
        elif not closer:
            the_distance = max(distance)

        for i in range(len(distance)):
            if distance[i] == the_distance:
                index = i
                break

        coordinate = [coordinates[0][index], coordinates[1][index]]
        for key in id_vector:
            if id_vector.get(key) == coordinate:
                the_id = key
                break

        qd = QuickDrawData()
        doodle = qd.get_drawing(different_object)
        while not doodle.key_id == the_id:
            doodle = qd.get_drawing(different_object)
            found = True
        if found:
            DEFAULT_SIZE_WHITE_CHANNEL = (1000, 1000, 1)
            canvas = np.ones(DEFAULT_SIZE_WHITE_CHANNEL, dtype="uint8") * 255
            cv2.namedWindow('Window')
            my_stroke_list = doodle.image_data
            for N in my_stroke_list:
                x_list = N[0]
                y_list = N[1]
                for point in range((len(x_list) - 1)):
                    cv2.line(canvas, (x_list[point], y_list[point]), (x_list[point + 1], y_list[point + 1]), (0, 0, 0), 2)
            cv2.imwrite("./png_sketches/" + different_object + "_" + the_object + "_" + str(closer) + "_" + str(M) + ".png", canvas)

            distance.pop(index)
            coordinates[0].pop(index)
            coordinates[1].pop(index)

        else:
            print("Image cannot be found.")


# 5 pizza most like the circle
# find("pizza", "circle", True, 5)
with open('googleqd_categories') as f:
     categories = [line.rstrip() for line in f]

def command():
    global listbox1, listbox2, listbox3, entry, button
    if listbox3.get(listbox3.curselection()) == "closest":
        var = True
    else:
        var = False
    num = int(entry.get())
    first = listbox1.get(listbox1.curselection())
    second = listbox2.get(listbox2.curselection())
    find(first, second, var, num)

    new_im = PIL.Image.new('RGB', (num * 1000, 1000), (250, 250, 250))
    for i in range(num):
        img = PIL.Image.open("./png_sketches/" + first + "_" + second + "_" + str(var) + "_" + str(i) + ".png")
        new_im.paste(img, (i*1000, 0))
    new_im.save("merged_images.png", "PNG")
    new_im.save(
        "./merged_images/" + str(num) + "_" + first + "_" + listbox3.get(listbox3.curselection()) + "to" + "_" + second + ".png",
        "PNG")
    new_im.show()




top = tk.Tk()
label1 = Label(top, text="unusual object")
label1.grid(row=0, column=0)

listbox1 = Listbox(top, yscrollcommand=True, exportselection=0)
listbox1.insert(END, *categories)
listbox1.grid(row=1, column=0)

label2 = Label(top, text="the object")
label2.grid(row=0, column=1)

listbox2 = Listbox(top, yscrollcommand=True, exportselection=0)
listbox2.insert(END, *categories)
listbox2.grid(row=1, column=1)

label3 = Label(top, text="closest/furthest")
label3.grid(row=2, column=0)

listbox3 = Listbox(top, yscrollcommand=True, exportselection=0)
listbox3.insert(END, "closest")
listbox3.insert(END, "furthest")
listbox3.grid(row=3, column=0)

label3 = Label(top, text="# of drawings")
label3.grid(row=2, column=1)

entry = Entry()
entry.grid(row=3, column=1)

button = Button(top, text= "Find!", command=command)
button.grid(row=4, column=1)

top.mainloop()
