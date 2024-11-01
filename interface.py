import tkinter as tk
from tkinter import filedialog, messagebox, ttk, TclError
from xml.sax import parse

from system import CaesarCipher, TrithemiusCipher, BookCipher


class CryptoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Криптографічна система")
        self.geometry("700x500")

        self.cipher_type = tk.StringVar(value='caesar')
        self.language_var = tk.StringVar(value='ua')
        self.key_var = tk.IntVar()
        self.A_var = tk.IntVar()
        self.B_var = tk.IntVar()
        self.C_var = tk.IntVar()
        self.key_phrase_var = tk.StringVar()
        self.pangram_var = tk.StringVar()

        self.init_ui()
        self.create_menu()

    def init_ui(self):
        self.input_text = tk.Text(self, height=5, width=60)
        self.input_text.pack(pady=10)

        self.output_text = tk.Text(self, height=5, width=60)
        self.output_text.pack(pady=10)

        # cipher choise
        tk.Label(self, text="Виберіть тип шифрування:").pack()
        tk.Radiobutton(self, text="Шифр Цезаря", variable=self.cipher_type, value='caesar',
                       command=self.toggle_cipher_options).pack()
        tk.Radiobutton(self, text="Шифр Тритеміуса", variable=self.cipher_type, value='trithemius',
                       command=self.toggle_cipher_options).pack()
        tk.Radiobutton(self, text="Книжковий шифр", variable=self.cipher_type, value='book',
                       command=self.toggle_cipher_options).pack()

        tk.Label(self, text="Мова:").pack()
        self.language_menu = tk.OptionMenu(self, self.language_var, 'ua', 'en')
        self.language_menu.pack()

        self.key_frame = tk.Frame(self)
        tk.Label(self.key_frame, text="Ключ для шифру Цезаря:").pack(side=tk.LEFT)
        self.key_entry = tk.Entry(self.key_frame, textvariable=self.key_var)
        self.key_entry.pack(side=tk.LEFT)
        self.key_frame.pack(pady=5)

        self.trithemius_frame = tk.Frame(self)
        self.method_label = tk.Label(self.trithemius_frame, text="Метод шифру Тритеміуса:")
        self.method_label.pack(side=tk.LEFT)
        self.method_choice = ttk.Combobox(self.trithemius_frame,
                                          values=['Лінійне рівняння', 'Нелінійне рівняння', 'Гасло'])
        self.method_choice.pack(side=tk.LEFT)
        self.method_choice.bind("<<ComboboxSelected>>", self.show_trithemius_options)

        # coefficients
        self.coefficients_frame = tk.Frame(self)
        tk.Label(self.coefficients_frame, text="A:").pack(side=tk.LEFT)
        self.A_entry = tk.Entry(self.coefficients_frame, textvariable=self.A_var)
        self.A_entry.pack(side=tk.LEFT)
        tk.Label(self.coefficients_frame, text="B:").pack(side=tk.LEFT)
        self.B_entry = tk.Entry(self.coefficients_frame, textvariable=self.B_var)
        self.B_entry.pack(side=tk.LEFT)
        tk.Label(self.coefficients_frame, text="C:").pack(side=tk.LEFT)
        self.C_entry = tk.Entry(self.coefficients_frame, textvariable=self.C_var)
        self.C_entry.pack(side=tk.LEFT)

        # key phrase
        self.key_phrase_frame = tk.Frame(self)
        tk.Label(self.key_phrase_frame, text="Гасло:").pack(side=tk.LEFT)
        self.key_phrase_entry = tk.Entry(self.key_phrase_frame, textvariable=self.key_phrase_var)
        self.key_phrase_entry.pack(side=tk.LEFT)

        # pangram
        self.pangram_frame = tk.Frame(self)
        tk.Label(self.pangram_frame, text="Вірш (бажано панграма):").pack(side=tk.LEFT)
        self.pangram_entry = tk.Entry(self.pangram_frame, textvariable=self.pangram_var)
        self.pangram_entry.pack(side=tk.LEFT)

        self.pangram_info_frame = tk.Frame(self)
        tk.Label(self.pangram_info_frame, text='Якщо не ввести вірш, буде використано стандартний (див. "Допомога")').pack(side=tk.TOP)

        tk.Button(self, text="Шифрувати", command=self.encrypt_file).pack(pady=5)
        tk.Button(self, text="Розшифрувати", command=self.decrypt_file).pack(pady=5)

        self.toggle_cipher_options()

    def create_menu(self):
        menubar = tk.Menu(self)

        # меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Відкрити", command=self.open_file)
        file_menu.add_command(label="Зберегти", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.quit_app)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # меню "Допомога"
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про розробника", command=self.about_developer)
        help_menu.add_command(label="Стандартний ключ книжкового шифру", command=self.standard_book_key)
        menubar.add_cascade(label="Допомога", menu=help_menu)

        self.config(menu=menubar)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            content = self.output_text.get("1.0", tk.END).strip()
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

    def quit_app(self):
        self.quit()

    def toggle_cipher_options(self):
        cipher = self.cipher_type.get()
        if cipher == 'caesar':
            self.pangram_frame.pack_forget()
            self.pangram_info_frame.pack_forget()
            self.trithemius_frame.pack_forget()
            self.coefficients_frame.pack_forget()
            self.key_phrase_frame.pack_forget()
            self.key_frame.pack(pady=5)
        elif cipher == 'trithemius':
            self.key_frame.pack_forget()
            self.pangram_frame.pack_forget()
            self.pangram_info_frame.pack_forget()
            self.trithemius_frame.pack(pady=5)
        elif cipher == 'book':
            self.key_frame.pack_forget()
            self.trithemius_frame.pack_forget()
            self.coefficients_frame.pack_forget()
            self.key_phrase_frame.pack_forget()
            self.pangram_frame.pack(pady=5)
            self.pangram_info_frame.pack(pady=5)

    def show_trithemius_options(self, event=None):
        method = self.method_choice.get()
        if method == 'Лінійне рівняння':
            self.coefficients_frame.pack(pady=5)
            self.key_phrase_frame.pack_forget()
            self.C_entry.config(state=tk.DISABLED)
        elif method == 'Нелінійне рівняння':
            self.coefficients_frame.pack(pady=5)
            self.key_phrase_frame.pack_forget()
            self.C_entry.config(state=tk.NORMAL)
        elif method == 'Гасло':
            self.coefficients_frame.pack_forget()
            self.key_phrase_frame.pack(pady=5)

    def encrypt_file(self):
        cipher_type = self.cipher_type.get()
        input_text = self.input_text.get("1.0", tk.END).strip()
        language = self.language_var.get()

        if cipher_type == 'caesar':
            try:
                key = self.key_var.get()
            except TclError:
                messagebox.showerror(title="Неправильний тип!", message="Ключ повинен бути цілим числом!")
                return
            cipher = CaesarCipher(key)
            encrypted_text = cipher.encrypt(input_text, language=language)

        elif cipher_type == 'trithemius':
            method = self.method_choice.get()
            if method == 'Лінійне рівняння':
                try:
                    A, B = self.A_var.get(), self.B_var.get()
                except TclError:
                    messagebox.showerror(title="Неправильний тип!", message="Коефіцієнти повинні бути цілими числами!")
                    return
                cipher = TrithemiusCipher(A=A, B=B)
                encrypted_text = cipher.encrypt_linear(input_text, language=language)
            elif method == 'Нелінійне рівняння':
                try:
                    A, B, C = self.A_var.get(), self.B_var.get(), self.C_var.get()
                except TclError:
                    messagebox.showerror(title="Неправильний тип!", message="Коефіцієнти повинні бути цілими числами!")
                    return
                cipher = TrithemiusCipher(A=A, B=B, C=C)
                encrypted_text = cipher.encrypt_nonlinear(input_text, language=language)
            elif method == 'Гасло':
                try:
                    key_phrase = self.key_phrase_var.get()
                except TclError:
                    messagebox.showerror(title="Неправильний тип!", message="Гасло повинне бути стрічкою!")
                    return
                cipher = TrithemiusCipher(key_phrase=key_phrase)
                encrypted_text = cipher.encrypt_key_phrase(input_text, language=language)

        elif cipher_type == 'book':
            try:
                pangram = self.pangram_var.get()
            except TclError:
                messagebox.showerror(title="Неправильний тип!", message="Вірш повинен бути стрічкою!")
                return
            cipher = BookCipher(pangram=pangram, language=language)
            encrypted_text = cipher.encrypt(input_text)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, encrypted_text)

    def decrypt_file(self):
        cipher_type = self.cipher_type.get()
        input_text = self.input_text.get("1.0", tk.END).strip()
        language = self.language_var.get()

        if cipher_type == 'caesar':
            try:
                key = self.key_var.get()
            except TclError:
                messagebox.showerror(title="Неправильний тип!", message="Ключ повинен бути цілим числом!")
                return
            cipher = CaesarCipher(key)
            decrypted_text = cipher.decrypt(input_text, language=language)

        elif cipher_type == 'trithemius':
            method = self.method_choice.get()
            match method:
                case 'Лінійне рівняння':
                    try:
                        A, B = self.A_var.get(), self.B_var.get()
                    except TclError:
                        messagebox.showerror(title="Неправильний тип!", message="Коефіцієнти повинні бути цілими числами!")
                        return
                    cipher = TrithemiusCipher(A=A, B=B)
                    decrypted_text = cipher.decrypt_linear(input_text, language=language)
                case 'Нелінійне рівняння':
                    try:
                        A, B, C = self.A_var.get(), self.B_var.get(), self.C_var.get()
                    except TclError:
                        messagebox.showerror(title="Неправильний тип!",
                                             message="Коефіцієнти повинні бути цілими числами!")
                        return
                    cipher = TrithemiusCipher(A=A, B=B, C=C)
                    decrypted_text = cipher.decrypt_nonlinear(input_text, language=language)
                case 'Гасло':
                    try:
                        key_phrase = self.key_phrase_var.get()
                    except TclError:
                        messagebox.showerror(title="Неправильний тип!", message="Гасло повинне бути стрічкою!")
                        return
                    cipher = TrithemiusCipher(key_phrase=key_phrase)
                    decrypted_text = cipher.decrypt_key_phrase(input_text, language=language)
                case _:
                    messagebox.showerror("Помилка", "Неочікувана помилка розшифрування")

        elif cipher_type == 'book':
            try:
                pangram = self.pangram_var.get()
            except TclError:
                messagebox.showerror(title="Неправильний тип!", message="Вірш повинен бути стрічкою!")
                return
            cipher = BookCipher(pangram=pangram, language=language)
            decrypted_text = cipher.decrypt(input_text)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, decrypted_text)

    def about_developer(self):
        messagebox.showinfo("Про розробника", "Ця система розроблена Дмитром Стельмахом із групи ТВ-13")

    def standard_book_key(self):
        cipher = BookCipher(None, 'ua')
        ua_string = '\n'.join(cipher.ua_pangrams)
        en_string = '\n'.join(cipher.en_pangrams)
        messagebox.showinfo(title="Стандартні ключі книжкового шифру", message=f"Українською:\n\n{ua_string}\n\n"
                                                                               f"Англійською:\n\n{en_string}")

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()
