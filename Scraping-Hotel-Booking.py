import mysql.connector
import time
import re
from playwright.sync_api import sync_playwright, TimeoutError

def main():
    # Koneksi ke database MySQL
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tripplaner')
    cursor = cnx.cursor()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # URL halaman pencarian Booking.com untuk Solo, Jawa Tengah, Indonesia
        page_url = 'https://www.booking.com/searchresults.id.html?ss=Solo%2C+Central+Java%2C+Indonesia&ssne=Bali&ssne_untouched=Bali&efdco=1&label=gen173rf-1FCAQoggI49ANIElgDaGiIAQGYARK4ARfIAQzYAQHoAQH4AQOIAgGiAgp0YXRyY2suY29tqAIDuALXjZayBsACAdICJDNiNDMwMjBiLTAxOWUtNGY2ZS05Mjg3LWMyMzQzMGVjYzUyOdgCBeACAQ&sid=7b4cf7fdddfa937af5f6aaba6d3031ed&aid=304142&lang=id&sb=1&src_elem=sb&src=index&dest_id=-2698531&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=63541d2eaa27001c&ac_meta=GhA2MzU0MWQyZWFhMjcwMDFjIAAoATICZW46BFNvbG9AAEoAUAA%3D&checkin=2024-05-23&checkout=2024-05-24&group_adults=2&no_rooms=1&group_children=0'
        page.goto(page_url, timeout=60000)

        # Meningkatkan timeout default untuk semua operasi berikutnya
        page.set_default_timeout(60000)

        # Loop untuk terus menggulir dan mengumpulkan data sampai tidak ada lagi data yang dimuat
        hotel_data = []
        while True:
            try:
                # Menunggu sampai kartu properti terlihat
                page.wait_for_selector('//div[@data-testid="property-card"]', timeout=60000)

                hotels = page.locator('//div[@data-testid="property-card"]').all()

                for hotel in hotels:
                    hotel_dict = {}
                    hotel_dict['nama_hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
                    hotel_dict['alamat'] = hotel.locator('//span[@data-testid="address"]').inner_text()

                    harga_text = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
                    # Hilangkan 'Rp ' dari string harga
                    harga_text = harga_text.replace('Rp ', '')
                    # Hapus titik sebagai pemisah ribuan
                    harga_text = harga_text.replace('.', '')
                    # Konversi ke tipe data integer
                    hotel_dict['harga'] = int(re.sub(r'[^\d]', '', harga_text))
                    hotel_dict['rating'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
                    hotel_dict['kota'] = 'Solo'  # Menambahkan nilai tetap ke dalam kolom "kota"
                    # Mengambil URL gambar langsung dari atribut 'src'
                    gambar_url = hotel.locator('//a[@data-testid="property-card-desktop-single-image"]/img').get_attribute('src')

                    # Menyimpan gambar langsung dari URL
                    hotel_dict['gambar'] = gambar_url

                    hotel_data.append(hotel_dict)

                # Menggulir ke bawah untuk memuat lebih banyak hasil
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(5)  # Tunggu beberapa detik untuk memuat lebih banyak hasil

                # Cek apakah ada elemen "Halaman Berikutnya" dan klik jika ada
                next_button = page.locator('//a[@aria-label="Halaman berikutnya"]')
                if next_button.is_visible():
                    next_button.click()
                    time.sleep(5)  # Tunggu beberapa detik untuk memuat halaman berikutnya
                else:
                    break  # Jika tidak ada elemen "Halaman Berikutnya", keluar dari loop

            except TimeoutError:
                print("Timeout saat menunggu kartu properti untuk dimuat")
                break

        # Memasukkan data ke dalam database MySQL
        for hotel_dict in hotel_data:
            try:
                add_hotel = (
                    "INSERT INTO hotels (nama_hotel, alamat, harga, rating, kota, images) VALUES (%(nama_hotel)s, %(alamat)s, %(harga)s, %(rating)s, %(kota)s, %(gambar)s)")
                cursor.execute(add_hotel, hotel_dict)
                cnx.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")

        # Menutup koneksi database
        cursor.close()
        cnx.close()

if __name__ == '__main__':
    main()
