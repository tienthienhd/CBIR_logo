from tkinter import *


class QueryComponent:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack(side=LEFT)
        lbl_name = Label(frame, text='name image')
        lbl_image = Label(frame, text='Image', anchor=CENTER, height=10, width=30, bg='gray')
        btn_query = Button(frame, text='Query')

        lbl_name.pack()
        lbl_image.pack()
        btn_query.pack()


class ResultComponent:
    def __init__(self, master):
        # Create a frame for the canvas and scrollbar
        frame = Frame(master)
        frame.pack(side=RIGHT)

        # Add a canvas in that frame
        canvas = Canvas(frame, bg="yellow")
        canvas.grid(row=0, column=0)

        # Create a vertical scrollbar linked to the canvas
        vsbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=0, sticky=EW)
        canvas.configure(yscrollcommand=vsbar.set)

        result_frame = Frame(canvas, bg='red', bd=2)


        results = [None] * 10

        img_per_row = 4
        for row in range(len(results) // img_per_row):
            for col in range(img_per_row):
                idx = row * img_per_row + col
                if idx >= len(results):
                    break
                print(idx, row, col)
                results[idx] = Label(frame, text='Result',
                                     anchor=CENTER, height=10, width=30, bg='gray')
                if col == 0:
                    results[idx].grid(row=row, padx=10, pady=10)

                else:
                    results[idx].grid(row=row, column=col, padx=10, pady=10)









root = Tk()
main_frame = Frame(root, width=500, height=500)
main_frame.pack()
query = QueryComponent(main_frame)
result = ResultComponent(main_frame)
root.mainloop()
