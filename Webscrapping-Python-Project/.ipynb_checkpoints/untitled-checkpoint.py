from bs4 import BeautifulSoup
import requests
import lxml
import time
import csv
import random

def webscraper(url, file_name):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=header)

    print("Processing...")

    num = random.randint(3, 7)
    time.sleep(num)

    if response.status_code == 200:
        print("Connected to the website")
        html_content = response.text

        # Creating soup 
        soup = BeautifulSoup(html_content, 'lxml')
        hotel_divs = soup.find_all('div', role='listitem')

    else:
        print(f"Connection Failed! {response.status_code}")
        return  # Stop execution if connection fails

    with open(f"{file_name}_data.csv", 'w', encoding='utf-8', newline='') as file_csv:
        writer = csv.writer(file_csv)

        writer.writerow(["Hotel_Name", "Location", "Price", "Rating", "Scores", "Reviews", "Url"])

        for hotel in hotel_divs:
            hotel_name = hotel.find('div', class_="f6431b446c a15b38c233")
            location = hotel.find('span', class_="aee5343fdb def9bc142a")
            price = hotel.find('span', class_="f6431b446c fbfd7c1165 e84eb96b1f")
            ratings = hotel.find('div', class_="a3b8729ab1 e6208ee469 cb2cbb3ccb")
            score = hotel.find('div', class_="a3b8729ab1 d86cee9b25")
            review = hotel.find('div', class_="abf093bdfe f45d8e4c32 d935416c47")
            url = hotel.find('a', href=True)

            # Using get_text(strip=True) to handle NoneType
            hotel_name = hotel_name.get_text(strip=True) if hotel_name else "N/A"
            location = location.get_text(strip=True) if location else "N/A"
            price = price.get_text(strip=True) if price else "N/A"
            ratings = ratings.get_text(strip=True) if ratings else "N/A"
            score = score.get_text(strip=True).split(" ")[-1] if score else "N/A"
            review = review.get_text(strip=True) if review else "N/A"
            url = url['href'] if url else "N/A"

            writer.writerow([hotel_name, location, price, ratings, score, review, url])

    print(f"Data successfully saved in {file_name}_data.csv")


# User Inputs
if __name__ = "__main__"
    url = input("Please Enter the URL: ")
    file_name = input("Please Enter the File Name: ")
    
    webscraper(url, file_name)
