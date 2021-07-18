import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog

root = tk.Tk()
root.geometry("650x450")
root.title("Studia")
root.withdraw()

page = []
for elem in tkinter.simpledialog.askstring("Inserisci le pagine", "Separa con una virgola ','\nPer fare una sequelza separa con un trattino '-'\nEsempio: '1, 3, 5, 8-10'").split(','):
    if '-' in elem:
        elem = elem.split('-')
        for i in range(int(elem[0]), int(elem[1])+1):
            page.append(str(i))
    else:
        page.append(str(int(elem)))

page = list(dict.fromkeys(page))
print(page)


root.deiconify()


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox(tk.ALL)
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

page_frame = ScrollableFrame(root)
for p in page:
    tk.Checkbutton(page_frame.scrollable_frame, text=p, justify=tk.LEFT).pack()
page_frame.pack(side=tk.LEFT, fill=tk.Y)

text_area = tk.Text(root, background='#333333', foreground='#ffffff',width=110, height=45, insertbackground="#cccccc")
text_area.pack(side=tk.RIGHT, expand=True)

root.mainloop()
