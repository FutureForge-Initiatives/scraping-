from playwright.sync_api import sync_playwright
import time

def main():

    destination = [
        "SOLO"
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

            submitButton = page.get_by_test_id("train-desktop-search-form-cta")
            submitButton.click()

            listTicketEl = page.get_by_test_id("train-desktop-search-result-list-departure")
            listTicketEl.wait_for()

            listTicket = page.get_by_test_id("train-desktop-search-result-list-departure-item").all()

            for ticket in listTicket:
                trainName = ticket.locator("h3").first.inner_text()
                print(trainName)
                trainPrice = ticket.locator("h2").first.inner_text()
                print(trainPrice)


        time.sleep(10)

        browser.close()

if __name__ == '__main__':
    main()
