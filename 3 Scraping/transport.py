from playwright.sync_api import sync_playwright
import time

def main():

    destination = [
        "Solo"
    ]

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page_url = 'https://www.traveloka.com/id-id/kereta-api'
        page.goto(page_url)

        asal = page.get_by_placeholder("Asal")
        asal.wait_for()

        for dest in destination:
            asal.click()
            asal.fill(dest)
            asalText = page.get_by_text("SLO - Solo Balapan - Solo", exact=True)
            asalText.click()

            tujuan = page.get_by_placeholder("Tujuan")
            tujuan.wait_for()
            tujuan.click()
            tujuan.fill("Madiun")
            tujuanText = page.get_by_text("MN - Madiun - Madiun", exact=True)
            tujuanText.click()
            
            # tanggal = page.get_by_test_id('train-desktop-search-form-departure-date-input-calendar').click
            tanggal = page.get_by_test_id('train-desktop-search-form-departure-date-input-value')
            tanggal.click()
            calendar = page.get_by_test_id('train-desktop-search-form-departure-date-input-calendar')
            # Pilih tanggal yang diinginkan (misalnya, 28)
            calendarTest = page.get_by_test_id('date-cell-28-6-2024') # Format Date (date-cell-dd-m-yyyy)
            calendarTest.click()
            
            
            submitButton = page.get_by_test_id("train-desktop-search-form-cta")
            submitButton.click()

            listTicketEl = page.get_by_test_id("train-desktop-search-result-list-departure")
            listTicketEl.wait_for()

            listTicket = page.get_by_test_id("train-desktop-search-result-list-departure-item").all()

            for ticket in listTicket:
                trainName = ticket.locator("h3").nth(0).inner_text()
                print("Nama Kereta:", trainName)
                
                trainClass = ticket.locator("div.css-901oao").nth(0).inner_text()
                print("Kelas Kereta:", trainClass )
                
                trainType = 'Kereta Api'
                print("Jenis Kendaraan : ", trainType)
                
                
                
                trainOrigin = ticket.locator("div.css-901oao").nth(1).inner_text()
                print("Asal:", trainOrigin )
                
                traindestination = ticket.locator("div.css-901oao").nth(2).inner_text()
                print("Tujuan:", traindestination )
                
                trainDescription = ticket.locator("div.css-901oao").nth(3).inner_text()
                print("Keterangan:", trainDescription )
                
                # Mendapatkan waktu keberangkatan
                trainDeparture = ticket.locator("h3").nth(1).inner_text()
                print("Jam Berangkat:", trainDeparture)

                # Mendapatkan waktu kedatangan
                trainArrival = ticket.locator("h3").nth(2).inner_text()
                print("Jam Kedatangan:", trainArrival)

                # Mendapatkan durasi perjalanan
                trainDuration = ticket.locator("h3").nth(3).inner_text()
                print("Durasi:", trainDuration)

                # Mendapatkan harga
                trainPrice = ticket.locator("h2").inner_text()
                print("Harga ",trainPrice)
                
                trainDate = "28 Juni 2024"
                print ("Tanggal : ", trainDate)
                
                trainCity = "Madiun"
                print ("Kota tujuan : ", trainCity)


        time.sleep(7)

        browser.close()

if __name__ == '__main__':
    main()
