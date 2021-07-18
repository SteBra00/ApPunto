import re
import sys
import json
import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font, families
from tkinter.messagebox import askyesnocancel, showerror

from source.constants import *
from source.win_edit import WinEdit


class ApPunto:
    """Classe Principale
        - args:
            master: tkinter.Tk()
        - return:
            NoneType
    -------------------------------------------------------"""
    def __init__(self, master, text=None):
        #--- Finestra base ----------------------------
        with open('source/json/editor.json', 'r') as f:
            editor = json.loads(f.read())
        self.view_tag = editor[VIEW_TAG]
        self.view_patch = editor[VIEW_PATCH]
        self.data = {NAME:DEFAULT_NAME, STATUS:SAVE}
        self.master = master
        self.master.resizable(False, False)
        self.master.protocol("WN_DELETE_WINDOW", on_closing)
        self.upgrade_title_window()

        #--- Barra del Menù ---------------------------
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        #------ Menù dropdown "File" ------------------
        menu_file = tk.Menu(self.menu, tearoff=0)
        menu_file.add_command(label="New File", accelerator="Ctrl+N", command=self.new_file)
        menu_file.add_command(label="Open File", accelerator="Ctrl+O", command=self.open_file)
        menu_file.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        menu_file.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_as)
        menu_file.add_separator()
        menu_file.add_command(label="Presents", accelerator="Ctrl+P", command=self.presents)
        menu_file.add_separator()
        menu_file.add_command(label="Restart", accelerator="Alt+R", command=restart)
        menu_file.add_command(label="Exit", accelerator="Alt+F4")
        self.menu.add_cascade(label="File", menu=menu_file)
        #------ Menù dropdown "Edit" ------------------
        menu_edit = tk.Menu(self.menu, tearoff=0)
        menu_edit.add_command(label="Editor", accelerator="Ctrl+Shift+E", command=self.change_editor)
        menu_add = tk.Menu(menu_edit, tearoff=0)
        for i in range(12):
            title = editor[FUNCTIONS][FUNCTS[i]][TITLE]
            accel = FUNCTS[i]
            if title!=VOID:
                menu_add.add_command(label=title, accelerator=accel, command=lambda i=i: self.function(i))
        menu_edit.add_cascade(label="Add", menu=menu_add)
        self.menu.add_cascade(label="Edit", menu=menu_edit)
        #------ Menù dropdown "About" -----------------
        menu_about = tk.Menu(self.menu, tearoff=0)
        menu_about.add_command(label="ApPunto", command=self.about_app)
        menu_about.add_command(label="ATGame", command=self.about_atg)
        self.menu.add_cascade(label="About", menu=menu_about)

        #--- Area Testuale ----------------------------
        self.textarea = tk.Text(self.master, width=32, height=30)
        self.miniarea = tk.Text(self.master, width=28, font=('', 2), state=tk.DISABLED)
        self.textarea.pack(fill=tk.Y, side=tk.LEFT)
        if editor[MINISIZE]:
            self.miniarea.pack(fill=tk.Y, side=tk.LEFT)
        if editor[SCROLL_BAR_Y]:
            scroll = tk.Scrollbar(self.master, command=self.textarea.yview, orient=tk.VERTICAL)
            self.textarea.configure(yscrollcommand=scroll.set)
            scroll.pack(side=tk.LEFT, fill=tk.Y)
        if text:
            self.open_file(text=text)
        elif len(sys.argv)>1:
            self.open_file(file=sys.argv[1])
            self.upgrade()
        
        #--- Settagio Iniziale ------------------------
        self._set_()
        self.shortcuts()

    def upgrade_title_window(self, event=None):
        """Aggiurna il titolo della finestra
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        if self.view_patch:
            title = self.data[NAME]
        else:
            title = self.data[NAME].split('/')[-1]
        self.master.title(title+' - '+APP_NAME)
    
    def upgrade(self, event=None):
        """Aggiurna lo stato del file attualmente aperto in "save" o "not save"
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        if self.view_tag:
            self.miniarea['state'] = tk.NORMAL
            if event:
                if event.char.isascii() and event.char.isalpha():
                    self.textarea.insert(self.textarea.index(tk.INSERT), event.char)
            self.data[STATUS] = NOT_SAVE
            for tag in self.textarea.tag_names():
                self.textarea.tag_delete(tag)
                self.miniarea.tag_delete(tag)
            text = self.textarea.get(1.0, tk.END)
            self.miniarea.delete(1.0, tk.END)
            self.miniarea.insert(1.0, text)
            for line, i in zip(text.split('\n'), range(1, len(text)+1)):
                for tag in re.finditer(r'</?[a-zA-Z]*\s*(\((\s*[a-zA-Z]*[0-9]*\=*\,*\'*\"*)*\))?>', line):
                    start, end = tag.span()
                    self.textarea.tag_add(TAG, str(i)+'.'+str(start+1), str(i)+'.'+str(end-1))
                    self.miniarea.tag_add(TAG, str(i)+'.'+str(start+1), str(i)+'.'+str(end-1))
                    self.textarea.tag_config(TAG, foreground=self.textarea.tag_color)
                    self.miniarea.tag_config(TAG, foreground=self.miniarea.tag_color)
            self.miniarea['state'] = tk.DISABLED
            if event:
                if event.char.isalpha():
                    return 'break'
        else:
            self.miniarea['state'] = tk.NORMAL
            text = self.textarea.get(1.0, tk.END)
            self.miniarea.delete(1.0, tk.END)
            self.miniarea.insert(1.0, text)
            self.miniarea['state'] = tk.DISABLED

    def new_file(self, event=None):
        """Svuota l'area testale dopo essersi accertato che lo stato del file sia "save"
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        True: "Successo"
                        False: "Fallita"
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        if self.data[STATUS]==NOT_SAVE:
            reply = askyesnocancel(title="File not save", message="Do you want save this file before closing?")
            if reply:
                self.save()
            elif reply==None:
                return False
        self.textarea.delete(1.0, tk.END)
        self.data[NAME] = DEFAULT_NAME
        self.data[STATUS] = SAVE
        self.upgrade_title_window()
        return True

    def open_file(self, text:str=None, file:str=None, event=None):
        """Apre un nuovo file dopo aver richiamato la funzione ApPunto.new_file()
            - args:
                text:   str (Carica nell'area testuale la stringa text)
                        NoneType (Verifica la condizione del parametro file)
                file:   str (Apri file già specificato)
                        NoneType (Apri finestra di richiesta file)
                event:  tkinter.Event()
                        NoneType
            - return:
                        True: "Successo"
                        False: "Fallita"
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        if self.new_file():
            if text:
                self.textarea.insert(1.0, text)
                name = None
            elif file:
                name = file
            else:
                name = filedialog.askopenfilename(
                    defaultextension=EXTENSION,
                    filetypes=[('ApPunto Files',EXTENSION),('ApPunto Scripts',EXTENSION_SCRIPT),('All Files','*.*')])
            if name:
                with open(name, 'r') as f:
                    self.textarea.insert(1.0, f.read())
                self.data[NAME] = name
                self.data[STATUS] = SAVE
                self.upgrade_title_window()
                self.upgrade(None)
                return True
        return False     

    def save(self, event=None):
        """Sovrascrive il file
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        if self.data[NAME]==DEFAULT_NAME:
            self.save_as()
        text = self.textarea.get(1.0, tk.END)
        with open(self.data[NAME], 'w') as f:
            f.write(text)
        self.data[STATUS] = SAVE
        self.upgrade_title_window()

    def save_as(self, event=None):
        """Salva il file
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        name = filedialog.asksaveasfilename(
            initialfile=DEFAULT_NAME+EXTENSION,
            defaultextension=EXTENSION,
            filetypes=[('ApPunto Files',EXTENSION),('ApPunto Scripts',EXTENSION_SCRIPT),('All Files','*.*')])
        if name:
            text = self.textarea.get(1.0, tk.END)
            with open(name, "w") as f:
                f.write(text)
            self.data[NAME] = name
            self.upgrade_title_window()

    def presents(self, event=None):
        """Apre la finestra di presentazione a cui passa il file da presentare
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        pass

    def change_editor(self, event=None):
        """Apre la finestra di settagio dell'editor
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        win = WinEdit(self)
        win.master.mainloop()

    def function(self, event):
        """Richiama la stringa in base al pulsante funzoine premuto per richiamare questo metodo
            - args:
                event:  tkinter.Event() (Chiamata Shortcuts)
                        int (Chiamata da Menù)
            - return:
                        NoneType
        -------------------------------------------------------"""
        with open('source/json/editor.json', 'r') as f:
            data = json.loads(f.read())
            if type(event)==int:
                text = data[FUNCTIONS][FUNCTS[event]][STRING]
            else:
                text = data[FUNCTIONS][event.keysym][STRING]
            self.textarea.insert(self.textarea.index(tk.INSERT), text)

    def about_app(self, event=None):
        """Apre la finestra di informazioni generali del programma ApPunto
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        pass

    def about_atg(self, event=None):
        """Apre la finestra di informazioni generali di A.T.Game
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        pass
    
    def _set_(self, event=None):
        """Imposta i parametri presenti del "editor.json" nel editor
            - args:
                event:  tkinter.Event()
                        NoneType
            - return:
                        NoneType
        (event e' una paramentro passato da tkinter negli shortcuts)
        -------------------------------------------------------"""
        with open('source/json/editor.json', 'r') as f:
            editor = json.loads(f.read())
            with open('source/json/theme.json', 'r') as f:
                theme = json.loads(f.read())[editor[THEME]]
            self.textarea[BACKGROUND] = theme[BACKGROUND]
            self.miniarea[BACKGROUND] = theme[BACKGROUND]
            self.textarea[FOREGROUND] = theme[FOREGROUND]
            self.miniarea[FOREGROUND] = theme[FOREGROUND]
            self.textarea[FONT] = (theme[FONT_FAMILY], theme[FONT_SIZE])
            self.miniarea[FONT] = (theme[FONT_FAMILY], 2)
            if self.view_tag:
                self.textarea.tag_color = theme[TAG_COLOR]
                self.miniarea.tag_color = theme[TAG_COLOR]
            else:
                self.textarea.tag_color = theme[FOREGROUND]
                self.miniarea.tag_color = theme[FOREGROUND]

    def _get_(self):
        return self.textarea.get(1.0, tk.END)

    def shortcuts(self):
        """Imposta gli shortcuts (scorciatoie da tastiera) nel editor
            - args:
                        NoneType
            - return:
                        NoneType
        -------------------------------------------------------"""
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Control-p>', self.presents)
        self.textarea.bind('<Control-E>', self.change_editor)
        self.textarea.bind('<F1>', self.function)
        self.textarea.bind('<F2>', self.function)
        self.textarea.bind('<F3>', self.function)
        self.textarea.bind('<F4>', self.function)
        self.textarea.bind('<F5>', self.function)
        self.textarea.bind('<F6>', self.function)
        self.textarea.bind('<F7>', self.function)
        self.textarea.bind('<F8>', self.function)
        self.textarea.bind('<F9>', self.function)
        self.textarea.bind('<F10>', self.function)
        self.textarea.bind('<F11>', self.function)
        self.textarea.bind('<F12>', self.function)
        self.textarea.bind('<Key>', self.upgrade)

def on_closing(event=None):
    """Verifica che il file sia salvato alla chisura dell'editor
        - args:
            event:  tkinter.Event()
                    NoneType
        - return:
                    NoneType
    -------------------------------------------------------"""
    
    if app.new_file():
        app.master.destroy()

def restart(event=None):
    global app
    text = app._get_()
    app.master.destroy()
    app = ApPunto(tk.Tk(), text)
    app.master.mainloop()

if __name__=='__main__':
    app = ApPunto(tk.Tk())
    app.master.mainloop()
