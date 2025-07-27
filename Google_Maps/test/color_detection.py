from pynput.mouse import Controller
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

mouse = Controller()

# --- Setup Chrome ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service('chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_window_size(1280, 720)
driver.set_window_position(0, 0)

# --- Buka halaman ---
link = "https://www.google.com/maps/place/Gedung+Direktorat+POLINES/@-7.0529595,110.4334173,18z/data=!4m10!1m2!2m1!1sPOLINES!3m6!1s0x2e708c0374ca46c1:0x2b0b2f7472560a54!8m2!3d-7.0520893!4d110.4355963!15sCgdQT0xJTkVTWgkiB3BvbGluZXOSAQdjb2xsZWdlmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU55YTBscWJHRm5FQUWqATwKCy9nLzEyMzJqMHFyEAEyHhABIhqf0CVgSRdciVhEk8ma_n1pddkBBmIj7Uhi1zILEAIiB3BvbGluZXPgAQD6AQQIVxBJ!16s%2Fg%2F11c5b17v1k?entry=ttu&g_ep=EgoyMDI1MDcyMy4wIKXMDSoASAFQAw%3D%3D"
driver.get(link)
input("Enter kalau sudah keload")

# --- Fungsi untuk ambil warna dari posisi tertentu ---
def get_colors(x, y_list):
    return [pyautogui.pixel(x, y) for y in y_list]

# --- Setup koordinat ---
target_x = 550

start_y = 300
end_y = 600
step = 5
target_y_list = [y for y in range(start_y, end_y + 1, step)]

# --- Fungsi konversi RGB ke Grayscale ---
def rgb_to_gray(rgb):
    r, g, b = rgb
    # Rumus grayscale yang umum: brightness perception
    return int(0.299*r + 0.587*g + 0.114*b)

# --- Mulai scroll dinamis ---
no_change_count = 0
max_no_change = 3

print("🌀 Mulai scroll dinamis berdasarkan warna, Danish Senpai~ 💖")

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

print("✅ Scroll selesai! Udah mentok bawah~ 😎 *Aku kasih selimut ke kamu* 💕")
