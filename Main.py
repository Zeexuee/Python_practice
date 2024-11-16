import pickle
import hashlib
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from ttkthemes import ThemedTk  # Untuk menggunakan tema modern

class Diary:
    def __init__(self, password_hash):
        self.entries = []
        self.password_hash = password_hash

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def autentikasi(self, password):
        if self.hash_password(password) == self.password_hash:
            return True
        else:
            return False

# ini branch ke-dua

    def tambah_entri(self, tanggal, tema, konten):
        entri = {'tanggal': tanggal, 'tema': tema, 'konten': konten}
        self.entries.append(entri)

    def lihat_entri(self):
        return "\n".join([f"Entri {i+1} - {entri['tanggal']} - {entri['tema']}\n{entri['konten']}\n{'-'*30}" for i, entri in enumerate(self.entries)])

    def hapus_entri(self, indeks):
        if 0 <= indeks < len(self.entries):
            del self.entries[indeks]

    def simpan_entri(self, filename='diary.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self.entries, file)

    def muat_entri(self, filename='diary.pkl'):
        try:
            with open(filename, 'rb') as file:
                self.entries = pickle.load(file)
        except FileNotFoundError:
            pass

def simpan_password_hash(password_hash, filename='password_hash.txt'):
    with open(filename, 'w') as file:
        file.write(password_hash)

def muat_password_hash(filename='password_hash.txt'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read().strip()
    else:
        return None

# Cek apakah password sudah pernah disetel
password_hash = muat_password_hash()

if not password_hash:
    root = ThemedTk(theme="arc")  # Menggunakan tema "arc" yang lebih modern
    root.withdraw()  # Sembunyikan jendela utama untuk input password pertama kali
    password = simpledialog.askstring("Set Password", "Set your diary password:", show="*")
    if password:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        simpan_password_hash(password_hash)
        messagebox.showinfo("Info", "Password berhasil disimpan.")
    root.deiconify()  # Tampilkan kembali jendela utama setelah input selesai

# Membuat instance diary dan memuat entri yang ada
diary = Diary(password_hash)
diary.muat_entri()

# GUI Application dengan tampilan modern
class DiaryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Diary Application")
        self.master.geometry("600x400")
        self.master.minsize(600, 400)  # Ukuran minimum jendela
        self.master.configure(bg='#F4F4F9')  # Latar belakang warna terang

        self.authenticated = False

        self.create_widgets()

    def create_widgets(self):
        # Frame utama dengan padding
        self.main_frame = tk.Frame(self.master, bg='#F4F4F9')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Area teks dengan scrollable untuk entri
        self.text_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=70, height=15, font=("Helvetica", 11), bd=0, bg="#FFFFFF", fg="#333333")
        self.text_area.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Tombol aksi
        self.view_button = tk.Button(self.main_frame, text="Lihat Entri", command=self.lihat_entri, font=("Helvetica", 10), bg="#5C6BC0", fg="white", relief="flat", height=2)
        self.view_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = tk.Button(self.main_frame, text="Tambah Entri", command=self.tambah_entri, font=("Helvetica", 10), bg="#81C784", fg="white", relief="flat", height=2)
        self.add_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.delete_button = tk.Button(self.main_frame, text="Hapus Entri", command=self.hapus_entri, font=("Helvetica", 10), bg="#E57373", fg="white", relief="flat", height=2)
        self.delete_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.save_button = tk.Button(self.main_frame, text="Simpan dan Keluar", command=self.simpan_keluar, font=("Helvetica", 10), bg="#4CAF50", fg="white", relief="flat", height=2)
        self.save_button.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

        self.auth_dialog()  # Memulai dialog autentikasi

    def auth_dialog(self):
        password = simpledialog.askstring("Password", "Masukkan password untuk mengakses diary:", show="*")
        if password and diary.autentikasi(password):
            self.authenticated = True
        else:
            messagebox.showerror("Error", "Password salah. Akses ditolak.")
            self.master.quit()  # Quit if authentication fails

    def lihat_entri(self):
        if not self.authenticated:
            self.auth_dialog()
        if self.authenticated:
            entries = diary.lihat_entri()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, entries)

    def tambah_entri(self):
        if not self.authenticated:
            self.auth_dialog()
        if self.authenticated:
            tema = simpledialog.askstring("Tema", "Masukkan tema entri:")
            konten = simpledialog.askstring("Konten", "Masukkan konten entri:")
            tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            diary.tambah_entri(tanggal, tema, konten)
            messagebox.showinfo("Info", "Entri berhasil ditambahkan.")
            self.lihat_entri()

    def hapus_entri(self):
        if not self.authenticated:
            self.auth_dialog()
        if self.authenticated:
            nomor_entri = simpledialog.askinteger("Hapus Entri", "Masukkan nomor entri yang akan dihapus:")
            if nomor_entri is not None and 0 < nomor_entri <= len(diary.entries):
                diary.hapus_entri(nomor_entri - 1)
                messagebox.showinfo("Info", "Entri berhasil dihapus.")
                self.lihat_entri()
            else:
                messagebox.showerror("Error", "Nomor entri tidak valid.")

    def simpan_keluar(self):
        diary.simpan_entri()
        messagebox.showinfo("Info", "Diary berhasil disimpan. Terima kasih!")
        self.master.quit()


# Running the GUI application with responsive layout
root = ThemedTk(theme="arc")  # Menggunakan tema arc dari ttkthemes
app = DiaryApp(root)
root.mainloop()
