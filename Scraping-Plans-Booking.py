import mysql.connector
import time
from playwright.sync_api import sync_playwright
import re

def main():
    # Koneksi ke database MySQL
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='')
    cursor = cnx.cursor()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page_url = 'https://flights.booking.com/flights/JKT.CITY-SOC.AIRPORT/?type=ONEWAY&adults=1&cabinClass=ECONOMY&children=&from=JKT.CITY&to=SOC.AIRPORT&fromCountry=ID&toCountry=ID&fromLocationName=Jakarta&toLocationName=Adisumarmo+International+Airport&depart=2024-06-12&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaGiIAQGYARK4ARfIAQzYAQHoAQH4AQuIAgGoAgO4ArCwlrIGwAIB0gIkZjJjZWNkMDAtMGM3Ni00OTcxLWEzYmItODM0YTRlYzk2ZjNi2AIG4AIB'
        page.goto(page_url)

        time.sleep(30)

        plans = page.locator('//div[@data-testid="searchresults_card"]').all()

        for pesawat in plans:
            pesawat_dict = {}
            pesawat_dict['nama_transportasi'] = pesawat.locator('//div[@data-testid="flight_card_carrier_0"]').inner_text()
            pesawat_dict['jenis'] = 'Pesawat'
            pesawat_dict['berangkat'] = pesawat.locator('//div[@data-testid="flight_card_segment_departure_airport_0"]').inner_text()
            pesawat_dict['tujuan'] = pesawat.locator('//div[@data-testid="flight_card_segment_destination_airport_0"]').inner_text()
            harga_text = pesawat.locator('//div[@class="FlightCardPrice-module__priceContainer___nXXv2"]').inner_text()
            # Hilangkan 'IDR' dari string harga
            harga_text = harga_text.replace('IDR', '')
            # Hapus titik sebagai pemisah ribuan
            harga_text = harga_text.replace('.', '')
            # Ganti koma sebagai pemisah desimal menjadi titik
            harga_text = harga_text.replace(',', '.')
            # Konversi ke tipe data float
            harga = float(re.sub(r'[^\d.]', '', harga_text))
            # Bulatkan harga ke angka terdekat
            harga = round(harga)
            pesawat_dict['harga'] = harga
            pesawat_dict['jam_keberangkatan'] = pesawat.locator('//div[@data-testid="flight_card_segment_departure_time_0"]').inner_text()
            pesawat_dict['jam_kedatangan'] = pesawat.locator('//div[@data-testid="flight_card_segment_destination_time_0"]').inner_text()
            pesawat_dict['kota'] = 'Solo'

            # Insert data into MySQL database
            add_pesawat = (
                "INSERT INTO transportasi (nama_transportasi, jenis_transportasi, berangkat, tujuan, harga, jam_keberangkatan, jam_kedatangan, kota) VALUES (%(nama_transportasi)s, %(jenis)s, %(berangkat)s, %(tujuan)s, %(harga)s, %(jam_keberangkatan)s, %(jam_kedatangan)s, %(kota)s)")
            cursor.execute(add_pesawat, pesawat_dict)
            cnx.commit()

        # Menutup koneksi database
        cursor.close()
        cnx.close()


if __name__ == '__main__':
    main()
