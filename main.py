import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, messagebox
from grammar.grammar import Parser
from environment.ast import Ast
from environment.environment import Environment
from environment.execute import RootExecuter

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OLCScript IDE")

        # Centrar ventana
        def center_window(width, height):
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            root.geometry(f"{width}x{height}+{x}+{y}")

        # Tamaño inicial y mínimo
        self.root.geometry("850x550")
        self.root.minsize(850,550)

        # Menu bar
        self.menu_bar = tk.Menu(root)

        # Elementos de boton "Archivo"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Abrir", command=self.open_file)
        self.file_menu.add_command(label="Guardar", command=self.save_file)
        self.file_menu.add_command(label="Guardar como", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.exit_app)
        # boton "Archivo" en menu bar
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        # boton "Ejecutar" en menu bar
        self.menu_bar.add_command(label="Ejecutar", command=self.run)
        # boton "Reportes" en menu bar
        self.menu_bar.add_command(label="Reportes", command=lambda: print("Reportes"))

        # Agregar menu bar a root
        self.root.config(menu=self.menu_bar)

        # Panel
        self.panel = tk.PanedWindow(root, orient=tk.VERTICAL)
        self.panel.pack(fill=tk.BOTH, expand=True)

        # Area de texto superior
        self.text_area = scrolledtext.ScrolledText(self.panel, width=60, height=12, font=("Calibri", 12), padx=3, pady=7, bd=0, highlightthickness=1, highlightbackground="#D7DBDD", highlightcolor="#087cd4")
        self.panel.add(self.text_area, stretch="always")

        # Frame para los botones
        self.button_frame = tk.Frame(self.panel, bg="white")
        self.panel.add(self.button_frame, stretch="never")

        # Boton "Consola"
        self.console_button = tk.Button(self.button_frame, text="Consola", bd=0, command=self.show_console)
        self.console_button.grid(row=0, column=0, padx=2)

        # Boton "Tabla de Símbolos"
        self.symbol_table_button = tk.Button(self.button_frame, text="Tabla de Símbolos", bd=0, bg="white", command=self.show_symbols_table)
        self.symbol_table_button.grid(row=0, column=1, padx=3)

        # Boton "Errores"
        self.errors_button = tk.Button(self.button_frame, text="Errores", bd=0, bg="white", command=self.show_errors)
        self.errors_button.grid(row=0, column=2, padx=3)

        # Etiqueta posicion cursor
        self.position_lbl = tk.Label(self.button_frame, anchor="e", text="Linea: 1, Columna: 1      ", bd=0, bg="white")
        self.position_lbl.grid(row=0, column=3,  sticky="nsew")

        # Configura la expansion de la etiqueta
        self.button_frame.columnconfigure(3, weight=1)

        # Frame para la tabla de símbolos y area de texto inferior
        self.output_frame = tk.Frame(self.panel)
        self.panel.add(self.output_frame, stretch="always")

        # Crear consola
        self.console = scrolledtext.ScrolledText(self.output_frame, width=60, height=8, font=("Calibri", 12), padx=3, pady=7, bd=0, highlightthickness=1, highlightbackground = "#D7DBDD", highlightcolor= "#D7DBDD")
        self.console.config(state="disabled")

        # Crear estilo para tabla
        style = ttk.Style()
        style.configure("newStyle.Treeview", bd=0, highlightthickness=1, highlightbackground = "gray", highlightcolor = "gray", font=('Calibri', 11))
        style.configure("newStyle.Treeview.Heading", font=('Calibri', 11,'bold'))
        style.layout("newStyle.Treeview", [('newStyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Crear tabla de símbolos
        self.symbols_table = ttk.Treeview(self.output_frame, style="newStyle.Treeview")
        # Configurar columnas
        self.symbols_table["columns"] = ("ID", "Tipo simbolo", "Tipo dato", "Ambito", "Linea", "Columna")
        # configurar columnas
        self.symbols_table.column("#0", anchor=tk.W, width=0, stretch=tk.NO)
        self.symbols_table.column("ID", anchor=tk.W, width=175)
        self.symbols_table.column("Tipo simbolo", anchor=tk.W, width=175)
        self.symbols_table.column("Tipo dato", anchor=tk.W, width=155)
        self.symbols_table.column("Ambito", anchor=tk.W, width=175)
        self.symbols_table.column("Linea", anchor=tk.W, width=75)
        self.symbols_table.column("Columna", anchor=tk.W, width=75)
        # Configurar encabezados
        self.symbols_table.heading("#0", text="", anchor=tk.W)
        self.symbols_table.heading("ID", text="ID", anchor=tk.W)
        self.symbols_table.heading("Tipo simbolo", text="Tipo simbolo", anchor=tk.W)
        self.symbols_table.heading("Tipo dato", text="Tipo dato", anchor=tk.W)
        self.symbols_table.heading("Ambito", text="Ambito", anchor=tk.W)
        self.symbols_table.heading("Linea", text="Linea", anchor=tk.W)
        self.symbols_table.heading("Columna", text="Columna", anchor=tk.W)

        # Crear tabla de errores #
        self.errors_table = ttk.Treeview(self.output_frame, style="newStyle.Treeview")
        # Configurar columnas
        self.errors_table["columns"] = ("No.", "Tipo error", "Descripcion", "Ambito", "Linea", "Columna")
        # configurar columnas
        self.errors_table.column("#0", anchor=tk.W, width=0, stretch=tk.NO)
        self.errors_table.column("No.", anchor=tk.W, width=50, stretch=tk.NO)
        self.errors_table.column("Tipo error", anchor=tk.W, width=125)
        self.errors_table.column("Descripcion", anchor=tk.W, width=380)
        self.errors_table.column("Ambito", anchor=tk.W, width=125)
        self.errors_table.column("Linea", anchor=tk.W, width=75)
        self.errors_table.column("Columna", anchor=tk.W, width=75)
        # Configurar encabezados
        self.errors_table.heading("No.", text="No.", anchor=tk.W)
        self.errors_table.heading("Tipo error", text="Tipo error", anchor=tk.W)
        self.errors_table.heading("Descripcion", text="Descripcion", anchor=tk.W)
        self.errors_table.heading("Ambito", text="Ambito", anchor=tk.W)
        self.errors_table.heading("Linea", text="Linea", anchor=tk.W)
        self.errors_table.heading("Columna", text="Columna", anchor=tk.W)

        # Inicializar atributos
        self.symbols = []
        self.errors = []

        # Mostrar area de texto por defecto al inicio
        self.show_console()

        # Configurar la expansion del Frame inferior
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        # Centrar ventana
        center_window(850, 550)

        # Vincular eventos al área de texto
        self.text_area.bind("<KeyRelease>", self.get_position)
        self.text_area.bind("<ButtonRelease-1>", self.get_position)

        # Inicializar atributos
        self.path_file = ""
        self.content_file = ""

    ### Metodos ###
    # Menu bar
    def open_file(self):
        filename = filedialog.askopenfilename(initialdir="/Desktop", title="Selecciona un archivo", filetypes=(("Archivos OLC", "*.olc"), ("Todos los archivos", "*.*")))
        if filename:
            self.path_file = filename
            with open(self.path_file, 'r') as file:
                self.content_file = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("0.0", self.content_file)

    def save_file(self):
        if self.path_file != "":
            with open(self.path_file, 'w') as file:
                file.write(self.text_area.get("1.0", tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        filename = filedialog.asksaveasfilename(initialdir="/Desktop", title="Guardar como", filetypes=(("Archivos OLC", "*.olc"), ("Todos los archivos", "*.*")))
        if filename:
            self.path_file = filename
            with open(self.path_file, 'w') as file:
                file.write(self.text_area.get("1.0", tk.END))
    
    def exit_app(self):
        if self.path_file != "" and self.text_area.get("1.0", tk.END).rstrip("\n") != self.content_file:
            response = messagebox.askquestion("Mensaje de confirmacion", "¿Deseas guardar los cambios?")
            if response == 'yes':               
                self.save_file()
            self.root.quit()
        if self.path_file == "" and self.text_area.get("1.0", tk.END).rstrip("\n") != "":
            response = messagebox.askquestion("Mensaje de confirmacion", "¿Deseas guardar el archivo?")
            if response == 'yes':
                self.save_file_as()
            self.root.quit()
        self.root.quit()

    def run(self):
        content_text_area = self.text_area.get("1.0", tk.END)
        # Creación del entorno global
        env = Environment(None, 'GLOBAL')
        # Creación del AST
        ast = Ast()
        # Creación del parser
        parser = Parser()
        # [inst1, inst2, inst2]
        instructionsArr = parser.interpretar(content_text_area)
        # Ejecución
        RootExecuter(instructionsArr, ast, env)
        # Estructurando respuesta
        res = {"result": True,"console":ast.getConsole(),"errors":ast.getErrors()}
        print(res)
        content_console = ast.getConsole()
        self.console.config(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.insert(tk.END, content_console)
        self.console.config(state="disabled")
        self.show_console()

    def show_console(self):
        # Ocultar scrollbars de la tabla si existen
        self.hide_table_scrollbars()
        # ocultar tabla de simbolos y tabla de errores
        if self.symbols_table:
            self.symbols_table.grid_forget()
        if self.errors_table:
            self.errors_table.grid_forget()
        # Cambiar color de boton seleccionado
        self.console_button.config(bg="#E6E6E6")
        self.symbol_table_button.config(bg="white")
        self.errors_button.config(bg="white")
        # Mostrar consola
        self.console.grid(row=0, column=0, sticky="nsew")

    def show_symbols_table(self):    
        # Ocultar consola y tabla de errores
        if self.console:
            self.console.grid_forget()
        if self.errors_table:
            self.errors_table.grid_forget()
        # Cambiar color de boton seleccionado
        self.console_button.config(bg="white")
        self.symbol_table_button.config(bg="#E6E6E6")
        self.errors_button.config(bg="white")
        # Limpiar tabla
        self.symbols_table.delete(*self.symbols_table.get_children())
        # Agregar simbolos
        if len(self.symbols) > 0:
            for symbol in self.symbols:
                self.symbols_table.insert("", "end", values=(symbol['ID'], symbol['type_symbol'], symbol['datatype'], symbol['ambit'], symbol['line'], symbol['column']))
        # Mostrar tabla
        self.symbols_table.grid(row=0, column=0, sticky="nsew")    
        # Scrollbars
        y_scrollbar = tk.Scrollbar(self.output_frame, orient=tk.VERTICAL, command=self.symbols_table.yview)
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        # Configurar scrollbars
        self.symbols_table.configure(yscrollcommand=y_scrollbar.set)

    def show_errors(self):
        # ocultar consola y tabla de simbolos
        if self.console:
            self.console.grid_forget()
        if self.symbols_table:
            self.symbols_table.grid_forget()
        # Cambiar color de boton seleccionado
        self.console_button.config(bg="white")
        self.symbol_table_button.config(bg="white")
        self.errors_button.config(bg="#E6E6E6")    
        # Limpiar tabla
        self.errors_table.delete(*self.errors_table.get_children())
        # Agregar errores
        if len(self.errors) > 0:
            for i, error in enumerate(self.errors):
                #self.errors_table.insert("", "end", values=(str(i+1), error['type'], error['description'], error['ambit'], error['line'], error['column']))
                self.errors_table.insert("", "end", values=(str(i+1), error.type, error.description, error.ambit, error.line , error.column))
        # Mostrar tabla
        self.errors_table.grid(row=0, column=0, sticky="nsew")
        # Scrollbars
        y_scrollbar = tk.Scrollbar(self.output_frame, orient=tk.VERTICAL, command=self.errors_table.yview)
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        # Configurar scrollbars
        self.errors_table.configure(yscrollcommand=y_scrollbar.set)

    def get_position(self, event):
        index = self.text_area.index(tk.INSERT)
        line, column = index.split('.')
        position_text = f"Línea: {line}, Columna: {str(int(column)+1)}      "
        self.position_lbl.config(text=position_text)

    # Oculta scrollbars de la tabla si existen
    def hide_table_scrollbars(self):
        for child in self.output_frame.winfo_children():
            if isinstance(child, tk.Scrollbar):
                child.grid_forget()            

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()