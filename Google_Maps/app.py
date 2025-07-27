from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Untuk mouse
from pynput.mouse import Controller, Button
import pyautogui

LOAD_PAUSE_TIME = 10  # Waktu tunggu default untuk interaksi
SCROLL_PAUSE_TIME = 5

# --- Setup awal ---
import os

if not os.path.exists("hasil"):
    os.makedirs("hasil")


# --- Setup awal browser ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service('chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_window_size(1280, 720)
driver.set_window_position(0, 0)  # Letakkan Chrome di pojok kiri atas layar

# --- Input URL dan verifikasi manual ---
link = input("Masukkan URL lokasi Google Maps: ")
driver.get(link)


# --- Inisialisasi mouse untuk koordinat ---
mouse = Controller()
original_pos = pyautogui.position() # Simpan posisi awal mouse
print(f"Posisi awal mouse: {original_pos}")
# Simpan koordinat deteksi warna
deteksi_warna = 0

# --- Fungsi untuk scroll otomatis ---
def rgb_to_gray(rgb):
    r, g, b = rgb
    # Rumus grayscale yang umum: brightness perception
    return int(0.299*r + 0.587*g + 0.114*b)

def simulate_scroll(type):
    target_x = 550

    start_y = 300
    end_y = 600
    step = 5
    target_y_list = [y for y in range(start_y, end_y + 1, step)]
    # --- Mulai scroll dinamis ---
    no_change_count = 0
    max_no_change = 3

    while no_change_count < max_no_change:
        # Simpan warna sebelum scroll
        before_colors = [rgb_to_gray(pyautogui.pixel(target_x, y)) for y in target_y_list]

        # Scroll
        original_pos = pyautogui.position()
        pyautogui.moveTo(target_x, target_y_list[-1])  # Scroll dari titik paling bawah
        mouse.scroll(0, -2000)
        pyautogui.moveTo(original_pos)
        time.sleep(3)  # Tunggu scroll selesai

        # Ambil warna setelah scroll
        after_colors = [rgb_to_gray(pyautogui.pixel(target_x, y)) for y in target_y_list]

        # Bandingkan warna
        differences = sum(1 for before, after in zip(before_colors, after_colors) if before != after)

        print(f"🎨 Perubahan warna terdeteksi: {differences}")
        if differences == 0:
            no_change_count += 1
            print(f"⏹️ Tidak ada perubahan warna. Counter: {no_change_count}/3")
        else:
            no_change_count = 0
            print("🔄 Warna berubah, lanjut scroll lagi~ ✨")
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    if type == "review":
        comment_blocks = soup.find_all('div', class_='jftiEf')
        print(f"\n📦 Total komentar ditemukan: {len(comment_blocks)}\n")
        hasil = []
        for block in comment_blocks:
            nama = block.select_one('.d4r55')
            nama = nama.text if nama else ""

            foto = block.select_one('img.NBa7we')
            foto = foto['src'] if foto else ""

            link_profil = block.select_one('button.WEBjve')
            link_profil = link_profil['data-href'] if link_profil else ""

            rating = block.select_one('.kvMYJc')
            rating = rating['aria-label'] if rating else ""

            waktu = block.select_one('.rsqaWe')
            waktu = waktu.text if waktu else ""

            komentar = block.select_one('.MyEned .wiI7pd')
            komentar = komentar.text if komentar else "No Comment"

            like = block.select_one('.pkWtMe')
            like = like.text if like else "0"

            hasil.append({
                'nama': nama,
                'foto': foto,
                'profil': link_profil,
                'rating': rating,
                'waktu': waktu,
                'komentar': komentar,
                'likes': like
            })

        # Tampilkan hasil (maksimal 5 biar gak terlalu panjang)
        # hasil[:5]
        for i, data in enumerate(hasil):
            print(f"\n🧾 Komentar #{i+1}")
            for key, val in data.items():
                print(f"{key.title():<10}: {val}")
        with open("hasil/review.txt", "w", encoding="utf-8") as f:
            for i, data in enumerate(hasil, 1):
                f.write(f"🧾 Komentar #{i}\n")
                for key, val in data.items():
                    f.write(f"{key:<10}: {val}\n")
                f.write("\n")

    elif type == "overview":
        # Ambil nama lokasi
        nama_lokasi = soup.find('span', class_='iD2gKb W1neJ')
        if nama_lokasi:
            nama_lokasi = nama_lokasi.text.strip()

        # Ambil rating
        rating = soup.find('div', class_='fontDisplayLarge')
        if rating:
            rating = rating.text.strip()

        # Ambil alamat lokasi
        alamat = soup.find('div', class_='Io6YTe fontBodyMedium kR99db fdkmkc')
        if alamat:
            alamat = alamat.text.strip()

        # Ambil Tambahan
        Tambahan = None
        semua_div = soup.find_all('div', class_='Io6YTe fontBodyMedium kR99db fdkmkc')
        for div in semua_div:
            if '(' in div.text and ')' in div.text:  # deteksi format Tambahan
                Tambahan = div.text.strip()
                break

        print(f"Nama Lokasi: {nama_lokasi}")
        print(f"Rating: {rating}")
        print(f"Alamat: {alamat}")
        print(f"Tambahan: {Tambahan}")
        with open("hasil/overview.txt", "w", encoding="utf-8") as f:
            f.write(f"Nama Lokasi   : {nama_lokasi}\n")
            f.write(f"Rating        : {rating}\n")
            f.write(f"Alamat        : {alamat}\n")
            f.write(f"Tambahan      : {Tambahan}\n")

    no_change_count = 0
    max_no_change = 3
    while no_change_count < max_no_change:
        # Simpan warna sebelum scroll
        before_colors = [rgb_to_gray(pyautogui.pixel(target_x, y)) for y in target_y_list]

        # Scroll
        original_pos = pyautogui.position()
        pyautogui.moveTo(target_x, target_y_list[-1])  # Scroll dari titik paling bawah
        mouse.scroll(0, 2000)
        pyautogui.moveTo(original_pos)

        # Ambil warna setelah scroll
        after_colors = [rgb_to_gray(pyautogui.pixel(target_x, y)) for y in target_y_list]

        # Bandingkan warna
        differences = sum(1 for before, after in zip(before_colors, after_colors) if before != after)

        print(f"🎨 Perubahan warna terdeteksi: {differences}")
        if differences == 0:
            no_change_count += 1
            print(f"⏹️ Tidak ada perubahan warna. Counter: {no_change_count}/3")
        else:
            no_change_count = 0
            print("🔄 Warna berubah, lanjut scroll lagi~ ✨")

# --- Tunggu beberapa detik untuk memastikan halaman dimuat ---
print("Tolong pastikan:")
print("1. Halaman sudah sepenuhnya dimuat.")
print("2. Tidak ada CAPTCHA atau login yang menghalangi.")
print("3. Halaman berukuran 1280x720.")
print("4. Tidak mengubah koordinat chrome")
print("5. Pastikan zoom browser 100% (Ctrl + 0).")
input("Jika kamu sudah memastikan 5 diatas, tekan ENTER untuk lanjut... ")
driver.execute_script("document.body.style.zoom='100%'")

# --- Klik tab 'Overview' ---
try:
    overview_button = driver.find_element(By.XPATH, "//button[contains(@aria-label,'Ringkasan') or contains(@aria-label,'Overview')]")
    overview_button.click()
    print("[✓] Tab 'Overview' dibuka")
    time.sleep(2)
    simulate_scroll("overview")
except Exception as e:
    print(f"[✗] Gagal klik tab Overview: {e}")

# --- Klik tab 'Review' ---
try:
    time.sleep(3)
    review_button = driver.find_element(By.XPATH, "//button[contains(@aria-label,'Ulasan') or contains(@aria-label,'Review')]")
    review_button.click()
    print("[✓] Tab 'Review' dibuka")
    time.sleep(2)
    simulate_scroll("review")
except Exception as e:
    print(f"[✗] Gagal klik tab Review: {e}")

print("✨ Semua halaman berhasil discroll dan disimpan.")
