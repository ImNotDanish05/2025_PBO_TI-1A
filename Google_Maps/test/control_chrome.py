from pynput.mouse import Controller, Button
import pyautogui
import time
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

print("Gerakin mouse ke posisi yang kamu mau ya, Danish Senpai~ ✨")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service('chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_window_size(1280, 720)
driver.set_window_position(0, 0)  # Letakkan Chrome di pojok kiri atas layar

# --- Input URL dan verifikasi manual ---
link = "https://www.google.com/maps/place/Gedung+Direktorat+POLINES/@-7.0529595,110.4334173,18z/data=!4m10!1m2!2m1!1sPOLINES!3m6!1s0x2e708c0374ca46c1:0x2b0b2f7472560a54!8m2!3d-7.0520893!4d110.4355963!15sCgdQT0xJTkVTWgkiB3BvbGluZXOSAQdjb2xsZWdlmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU55YTBscWJHRm5FQUWqATwKCy9nLzEyMzJqMHFyEAEyHhABIhqf0CVgSRdciVhEk8ma_n1pddkBBmIj7Uhi1zILEAIiB3BvbGluZXPgAQD6AQQIVxBJ!16s%2Fg%2F11c5b17v1k?entry=ttu&g_ep=EgoyMDI1MDcyMy4wIKXMDSoASAFQAw%3D%3D"
driver.get(link)

input("Enter kalau sudah keload")
# while True:
#     x, y = pyautogui.position()
#     print(f"Koordinat: ({x}, {y})   ", end="\r")
#     time.sleep(0.2)

mouse = Controller()

# Simulasi: scroll di koordinat tertentu
target_x, target_y = 800, 500

# Simpan posisi awal
original_pos = pyautogui.position()

# Pindah ke titik scroll
pyautogui.moveTo(target_x, target_y)
time.sleep(0.1)

# Scroll ke bawah (angka positif = ke atas, negatif = ke bawah)
mouse.scroll(0, -2000)  # Scroll ke bawah 2000 unit

# Balikin posisi mouse
pyautogui.moveTo(original_pos)
