import tkinter as tk
from tkinter import filedialog, messagebox, ttk, TclError

from system import EncryptionDES, DES


class CryptoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Криптографічна система")
        self.geometry("700x500")

        self.mode_var = tk.StringVar(value='ECB')
        self.key_var = tk.StringVar(value='')
        self.iv_var = tk.StringVar(value='')

        self.init_ui()
        self.create_menu()


    def init_ui(self):
        self.input_text = tk.Text(self, height=5, width=60)
        self.input_text.pack(pady=10)
        self.output_text = tk.Text(self, height=5, width=60)
        self.output_text.pack(pady=10)

        tk.Label(self, text="Оберіть режим DES:").pack()
        mode_options = ['ECB', 'CBC', 'CFB', 'OFB']
        self.mode_menu = tk.OptionMenu(self, self.mode_var, *mode_options,
                                       command=lambda _: self.toggle_des_options())
        self.mode_menu.pack()

        tk.Label(self, text="Введіть 8-байтовий ключ:").pack()
        self.key_entry = tk.Entry(self, textvariable=self.key_var, width=20)
        self.key_entry.pack(pady=5)

        self.iv_frame = tk.Frame(self)
        tk.Label(self.iv_frame, text="Також введіть 8-байтовий IV (для режимів CBC, CFB, OFB):").pack()
        self.iv_entry = tk.Entry(self.iv_frame, textvariable=self.iv_var, width=20)
        self.iv_frame.pack(pady=5)

        tk.Button(self, text="Зашифрувати", command=self.encrypt_text).pack(pady=5)
        tk.Button(self, text="Розшифрувати", command=self.decrypt_text).pack(pady=5)

        self.toggle_des_options()


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
        # help_menu.add_command(label="Стандартний ключ книжкового шифру", command=self.standard_book_key)
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

    def toggle_des_options(self):
        selected_mode = self.mode_var.get()
        if selected_mode == 'ECB':
            self.iv_frame.pack_forget()
        else:
            self.iv_frame.pack(pady=5)
            for widget in self.iv_frame.winfo_children():
                widget.pack()

        # self.update_idletasks()

    def encrypt_text(self):
        key = self.key_var.get().encode().ljust(8, b'\0')[:8]  # забезпечуємо завжди 8 байтів
        plaintext = self.input_text.get("1.0", tk.END).strip().encode()

        mode = getattr(DES, 'MODE_' + self.mode_var.get())

        if self.mode_var.get() == 'ECB':
            des_cipher = EncryptionDES(mode, key)
        else:
            iv = self.iv_var.get().encode().ljust(8, b'\0')[:8]
            des_cipher = EncryptionDES(mode, key, iv=iv)

        ciphertext = des_cipher.encrypt(plaintext)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", ciphertext.hex())

    def decrypt_text(self):
        key = self.key_var.get().encode().ljust(8, b'\0')[:8]  # забезпечуємо завжди 8 байтів
        ciphertext = bytes.fromhex(self.input_text.get("1.0", tk.END).strip())

        mode = getattr(DES, 'MODE_' + self.mode_var.get())

        if self.mode_var.get() == 'ECB':
            des_cipher = EncryptionDES(mode, key)
        else:
            iv = self.iv_var.get().encode().ljust(8, b'\0')[:8]
            des_cipher = EncryptionDES(mode, key, iv=iv)

        decrypted_text = des_cipher.decrypt(ciphertext)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", decrypted_text.decode(errors='ignore'))

    def about_developer(self):
        messagebox.showinfo("Про розробника", "Ця система розроблена Дмитром Стельмахом із групи ТВ-13")


if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()
