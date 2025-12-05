import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = "https://books.toscrape.com/"

# Your "watchlist" – like client saying:
# "Tell me if this goes below this price"
WATCHLIST = {
    # "partial product name": target_price_in_pounds
    "A Light in the Attic": 50.00,
    "Tipping the Velvet": 20.00,
    "Soumission": 40.00,
}

def scrape_prices():
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")

    items = []

    for product in products:
        name = product.h3.a["title"]
        price_text = product.find("p", class_="price_color").text.strip()  # e.g. '£53.74'

        # Remove currency sign and convert to float
        clean_price = price_text.replace("Â", "").replace("£", "").strip()
        price_value = float(clean_price)

        items.append({
            "Product Name": name,
            "Price": price_value
        })

    return items

def check_alerts(items):
    alerts = []

    for item in items:
        name = item["Product Name"]
        price = item["Price"]

        for watch_name, target_price in WATCHLIST.items():
            if watch_name.lower() in name.lower():
                if price <= target_price:
                    alerts.append({
                        "Product": name,
                        "Current Price": price,
                        "Target Price": target_price,
                        "Status": "ALERT – Price at or below target"
                    })
                else:
                    alerts.append({
                        "Product": name,
                        "Current Price": price,
                        "Target Price": target_price,
                        "Status": "No alert – Still above target"
                    })

    return alerts

if __name__ == "__main__":
    print("\n🔍 Checking live prices...")
    items = scrape_prices()

    alerts = check_alerts(items)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not alerts:
        print("No watched products found on this page.")
    else:
        print(f"\n⏱ Checked at: {now}\n")
        for alert in alerts:
            print(f"{alert['Product']}")
            print(f"  Current: £{alert['Current Price']}")
            print(f"  Target : £{alert['Target Price']}")
            print(f"  Status : {alert['Status']}")
            print("-" * 40)

        # Log to CSV for history
        df = pd.DataFrame(alerts)
        df["Checked At"] = now
        df.to_csv("price_alert_log.csv", mode="a", index=False, header=False)

        print("\n✅ Logged to price_alert_log.csv")
