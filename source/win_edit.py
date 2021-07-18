import re
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import families
import tkinter.colorchooser as tkcolor

if __name__ == "__main__":
    from constants import *
else:
    from source.constants import *

class WinEdit:
    def __init__(self, parent=None):
        self.master = tk.Tk()
        self.master.geometry('550x385+50+50')
        self.master.title('Edit Editor - ApPunto')
        self.master.resizable(False, False)
        with open('source/json/editor.json', 'r') as f:
            self.editor = json.loads(f.read())
        with open('source/json/theme.json', 'r') as f:
            self.themes = json.loads(f.read())

        frames = ttk.Notebook(self.master)

        #--- Pagina dei temi --------------------------
        frame_theme = ttk.Frame(frames)
        list_btn_theme = ttk.Frame(frame_theme)
        for theme in self.themes.keys():
            if theme!=PERSONAL:
                btn_theme = ttk.Button(list_btn_theme, text=theme, command=lambda theme=theme: self._set_editor_(THEME, theme))
                btn_theme.pack(padx=10)
        btn_theme = ttk.Button(list_btn_theme, text='Personal', command=lambda theme=theme: self._set_editor_(THEME, PERSONAL))
        btn_theme.pack(padx=10)
        list_btn_theme.pack(pady=10, side=tk.LEFT)
        list_entry_theme = ttk.Frame(frame_theme)
        ttk.Label(list_entry_theme, text='Personal').pack(pady=10)
        ttk.Button(list_entry_theme, text='Background', command=self._set_entry_bg_).pack()
        self.entry_bg = ttk.Entry(list_entry_theme, width=23)
        self.entry_bg.insert(0, self.themes[PERSONAL][BACKGROUND])
        self.entry_bg['state'] = tk.DISABLED
        self.entry_bg.pack(pady=2)
        ttk.Button(list_entry_theme, text='Foreground', command=self._set_entry_fg_).pack()
        self.entry_fg = ttk.Entry(list_entry_theme, width=23)
        self.entry_fg.insert(0, self.themes[PERSONAL][FOREGROUND])
        self.entry_fg['state'] = tk.DISABLED
        self.entry_fg.pack(pady=2)
        ttk.Button(list_entry_theme, text='Tag Color', command=self._set_entry_tfg_).pack()
        self.entry_tfg = ttk.Entry(list_entry_theme, width=23)
        self.entry_tfg.insert(0, self.themes[PERSONAL][TAG_COLOR])
        self.entry_tfg['state'] = tk.DISABLED
        self.entry_tfg.pack(pady=2)
        self.entry_font_family = ttk.Combobox(list_entry_theme, value=families())
        self.entry_font_family.pack(pady=4)
        self.entry_font_family.current(22)
        self.entry_font_size = ttk.Combobox(list_entry_theme, value=[i for i in range(0, 45)])
        self.entry_font_size.pack(pady=2)
        self.entry_font_size.current(9)
        ttk.Button(list_entry_theme, text='Apply', command=self._set_personal_theme_).pack(pady=5)
        list_entry_theme.pack(pady=10, padx=30, side=tk.LEFT)
        self.exemple_text_area = tk.Text(frame_theme, width=30, height=17)
        self.exemple_text_area.insert(1.0, EXEMPLE_TEXT)
        self.exemple_text_area['state'] = tk.DISABLED
        self.exemple_text_area.pack(pady=10, side=tk.LEFT)
        frame_theme.pack()

        #--- Pagina dei Tools -------------------------
        frame_tools = ttk.Frame(frames)
        notebook_functs = ttk.Notebook(frame_tools)
        self.funtions = []
        for key, value in self.editor[FUNCTIONS].items():
            frame_funct = ttk.Frame(notebook_functs)
            tit_ent = ttk.Entry(frame_funct)
            tit_ent.pack(fill=tk.X, padx=10, pady=10)
            tit_ent.insert(0, value[TITLE])
            str_ent = tk.Text(frame_funct, height=12, font=('Bahnschrift SemiBold', 9))
            str_ent.pack(fill=tk.X, padx=10, pady=10)
            str_ent.insert(1.0, value[STRING])
            frame_funct.pack(expand=True)
            notebook_functs.add(frame_funct, text=f'  {key}   ')
            self.funtions.append([key, tit_ent, str_ent])
        notebook_functs.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        frame_tools.pack()

        #--- Pagina di Custum -------------------------
        frame_custum = ttk.Frame(frames)
        check_frame = ttk.Frame(frame_custum)
        self.custum_var = {}
        self.custum_var[SCROLL_BAR_X] = tk.IntVar(value=self.editor[SCROLL_BAR_X])
        ttk.Checkbutton(check_frame, text=SCROLL_BAR_X, onvalue=1, offvalue=0, variable=self.custum_var[SCROLL_BAR_X]).pack()
        self.custum_var[SCROLL_BAR_Y] = tk.IntVar(value=self.editor[SCROLL_BAR_Y])
        ttk.Checkbutton(check_frame, text=SCROLL_BAR_Y, onvalue=1, offvalue=0, variable=self.custum_var[SCROLL_BAR_Y]).pack()
        self.custum_var[MINISIZE] = tk.IntVar(value=self.editor[MINISIZE])
        ttk.Checkbutton(check_frame, text=MINISIZE, onvalue=1, offvalue=0, variable=self.custum_var[MINISIZE]).pack()
        self.custum_var[VIEW_PATCH] = tk.IntVar(value=self.editor[VIEW_PATCH])
        ttk.Checkbutton(check_frame, text=VIEW_PATCH, onvalue=1, offvalue=0, variable=self.custum_var[VIEW_PATCH]).pack()
        self.custum_var[VIEW_TAG] = tk.IntVar(value=self.editor[VIEW_TAG])
        ttk.Checkbutton(check_frame, text=VIEW_TAG, onvalue=1, offvalue=0, variable=self.custum_var[VIEW_TAG]).pack()
        self.custum_var[AUTO_INDENT] = tk.IntVar(value=self.editor[AUTO_INDENT])
        ttk.Checkbutton(check_frame, text=AUTO_INDENT, onvalue=1, offvalue=0, variable=self.custum_var[AUTO_INDENT]).pack()
        self.custum_var[LINK] = tk.IntVar(value=self.editor[LINK])
        ttk.Checkbutton(check_frame, text=LINK, onvalue=1, offvalue=0, variable=self.custum_var[LINK]).pack()
        self.custum_var[PROJECT_TREE] = tk.IntVar(value=self.editor[PROJECT_TREE])
        ttk.Checkbutton(check_frame, text=PROJECT_TREE, onvalue=1, offvalue=0, variable=self.custum_var[PROJECT_TREE]).pack()
        check_frame.pack(expand=True)
        ttk.Label(frame_custum, text=DANGER_CUSTUM_TEST, foreground='red').pack()
        frame_custum.pack()

        frames.add(frame_theme, text='Theme')
        frames.add(frame_tools, text='Tools')
        frames.add(frame_custum, text='Custom')
        frames.pack(expand=True, fill=tk.BOTH, side=tk.TOP, padx=10, pady=5)

        #--- Barra di salvataggio ---------------------
        bottom_bar = ttk.Frame(self.master, height=10)
        ttk.Button(bottom_bar, text='Exit', command=self.close).pack(padx=10, side=tk.RIGHT)
        ttk.Button(bottom_bar, text='Ok', command=lambda p=parent: self.ok(p)).pack(padx=10, side=tk.RIGHT)
        ttk.Button(bottom_bar, text='Apply', command=lambda p=parent: self.apply(p)).pack(padx=10, side=tk.RIGHT)
        bottom_bar.pack(expand=True, fill=tk.X, side=tk.TOP)

        self._update_()

    def save_editor(self):
        with open('source/json/editor.json', 'w') as f:
            json.dump(self.editor, f, indent=4)
    
    def save_theme(self):
        with open('source/json/theme.json', 'w') as f:
            json.dump(self.themes, f, indent=4)

    def apply(self, parent=None):
        for funct in self.funtions:
            self.editor[FUNCTIONS][funct[0]][TITLE] =  funct[1].get()
            self.editor[FUNCTIONS][funct[0]][STRING] = funct[2].get(1.0, tk.END)[:-1]
        for key in self.custum_var.keys():
            self.editor[key] = self.custum_var[key].get()
        self.save_editor()
        self.save_theme()
        if parent:
            parent._set_()

    def ok(self, parent=None):
        self.apply(parent)
        self.close()

    def close(self):
        self.master.destroy()

    def _set_editor_(self, attrib, value):
        self.editor[attrib] = value
        self._update_()

    def _set_theme_(self, name, attrib, value):
        self.themes[name][attrib] = value
        self._update_()

    def _update_(self):
        self.exemple_text_area[BACKGROUND] = self.themes[self.editor[THEME]][BACKGROUND]
        self.exemple_text_area[FOREGROUND] = self.themes[self.editor[THEME]][FOREGROUND]
        self.exemple_text_area[FONT] = (self.themes[self.editor[THEME]][FONT_FAMILY],self.themes[self.editor[THEME]][FONT_SIZE])
        for tag in self.exemple_text_area.tag_names():
            self.exemple_text_area.tag_delete(tag)
        text = self.exemple_text_area.get(1.0, tk.END).split('\n')
        for line, i in zip(text, range(1, len(text)+1)):
            for tag in re.finditer(r'</?[a-zA-Z]*\s*(\((\s*[a-zA-Z]*[0-9]*\=*\,*\'*\"*)*\))?>', line):
                start, end = tag.span()
                self.exemple_text_area.tag_add(TAG, str(i)+'.'+str(start+1), str(i)+'.'+str(end-1))
                self.exemple_text_area.tag_config(TAG, foreground=self.themes[self.editor[THEME]][TAG_COLOR])

    def _set_personal_theme_(self):
        self._set_theme_(PERSONAL, BACKGROUND, self.entry_bg.get())
        self._set_theme_(PERSONAL, FOREGROUND, self.entry_fg.get())
        self._set_theme_(PERSONAL, TAG_COLOR, self.entry_tfg.get())
        self._set_theme_(PERSONAL, FONT_FAMILY, self.entry_font_family.get())
        self._set_theme_(PERSONAL, FONT_SIZE, self.entry_font_size.get())

    def _set_entry_bg_(self):
        color = self.entry_bg.get()
        color = tkcolor.askcolor(color)
        if color[1]:
            self.entry_bg['state'] = tk.ACTIVE
            self.entry_bg.delete(0, tk.END)
            self.entry_bg.insert(0, color[1])
            self.entry_bg['state'] = tk.DISABLED

    def _set_entry_fg_(self):
        color = self.entry_fg.get()
        color = tkcolor.askcolor(color)
        if color[1]:
            self.entry_fg['state'] = tk.ACTIVE
            self.entry_fg.delete(0, tk.END)
            self.entry_fg.insert(0, color[1])
            self.entry_fg['state'] = tk.DISABLED

    def _set_entry_tfg_(self):
        color = self.entry_tfg.get()
        color = tkcolor.askcolor(color)
        if color[1]:
            self.entry_tfg['state'] = tk.ACTIVE
            self.entry_tfg.delete(0, tk.END)
            self.entry_tfg.insert(0, color[1])
            self.entry_tfg['state'] = tk.DISABLED

if __name__ == "__main__":
    we = WinEdit()
    we.master.mainloop()