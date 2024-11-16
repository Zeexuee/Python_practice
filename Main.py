import pickle
import hashlib
from datetime import datetime
import os

class Diary:
    def __init__(self, password_hash):
        self.entries = []
        self.password_hash = password_hash

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def autentikasi(self):
        input_password = input("Masukkan password: ")
        if self.hash_password(input_password) == self.password_hash:
            return True
        else:
            print("Password salah! Akses ditolak.")
            return False

    def tambah_entri(self, tanggal, tema, konten):
        if self.autentikasi():
            entri = {'tanggal': tanggal, 'tema': tema, 'konten': konten}
            self.entries.append(entri)
            print("Entri berhasil ditambahkan.")

    def lihat_entri(self):
        if self.autentikasi():
            if not self.entries:
                print("Tidak ada entri ditemukan.")
            else:
                for i, entri in enumerate(self.entries, 1):
                    print(f"\nEntri {i} - {entri['tanggal']} - {entri['tema']}")
                    print(entri['konten'])
                    print("-" * 30)

    def hapus_entri(self, indeks):
        if self.autentikasi():
            if 0 <= indeks < len(self.entries):
                del self.entries[indeks]
                print("Entri berhasil dihapus.")
            else:
                print("Nomor entri tidak valid.")

    def simpan_entri(self, filename='diary.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self.entries, file)
        print("Diary berhasil disimpan.")

    def muat_entri(self, filename='diary.pkl'):
        try:
            with open(filename, 'rb') as file:
                self.entries = pickle.load(file)
            print("Diary berhasil dimuat.")
        except FileNotFoundError:
            print("Tidak ada diary yang tersimpan. Memulai dengan diary kosong.")

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
    password = input("Set your diary password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    simpan_password_hash(password_hash)
    print("Password berhasil disimpan.")

# Membuat instance diary dan memuat entri yang ada
diary = Diary(password_hash)
diary.muat_entri()

while True:
    print("\nMenu Diary")
    print("(T)ambah Entri")
    print("(L)ihat Entri")
    print("(H)apus Entri")
    print("(S)impan dan Keluar")

    pilihan = input("Pilih opsi: ").lower()

    if pilihan == 't':
        tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tema = input("tema: ")
        konten = input("entri:\n")
        diary.tambah_entri(tanggal, tema, konten)
    
    elif pilihan == 'l':
        diary.lihat_entri()

    elif pilihan == 'h':
        nomor_entri = int(input("Masukkan nomor entri yang akan dihapus: ")) - 1
        diary.hapus_entri(nomor_entri)

    elif pilihan == 's':
        diary.simpan_entri()
        print("Selamat tinggal!")
        break

    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
