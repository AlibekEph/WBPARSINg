from bs4 import BeautifulSoup
from lxml import html
import csv
import requests
import time
from multiprocessing import Pool
import json

def csv_writer(lsts, path):
    data = lsts
    print(len(data))
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            try:
                writer.writerow(line)
            except:
                continue

def csv_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    res = []
    for row in reader:
        res.append(" ".join(row))
    return res

csv_path = "urls_fiels/test_urls.csv"
urls = []
with open(csv_path, "r") as f_obj:
    urls = csv_reader(f_obj)

def get_result(url_):
    url = url_.split('/')
    req = requests.get(f'https://www.wildberries.ru/{url[4]}/product/data?').json()
    data = req['value']['data']
    name = data['productCard']['brandName'] + ' / ' + data['productCard']['goodsName']
    comments = data['productCard']['commentsCount']
    stars = data['productCard']['star']
    orders = data['productCard']['nomenclatures'][url[4]]['ordersCount']
    price = data['priceForProduct']['priceWithSale']
    return [url_, name, comments, stars, orders, price]

def main():
    with Pool(10) as p:
        result = p.map(get_result, urls[:20])
    csv_writer(result, "result_csv/test3.csv")
    print("ALL")

if __name__ == '__main__':
    result = []
    print("start")
    main()
