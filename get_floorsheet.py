import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os


def get_floorsheet_response(page, limit):
    url = f"http://www.nepalstock.com/main/floorsheet/index/{page}/?contract-no=&stock-symbol=&buyer=&seller=&_limit={limit}"
    payload = {}
    headers = {
        'Cookie': 'ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22ad22513e47a925b8ff648f12ea9f9965%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A8%3A%2210.0.2.4%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A22%3A%22PostmanRuntime%2F7.26.10%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1616692291%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Dc56b2ad6a946eed94d6ecf89ab567dfc'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text)
    return soup


def extract_table(soup):
    try:
        table = soup.find("table", {"class": "table my-table"})
        rows = table.find_all("tr")
        container = []
        allowed = rows[2:]
        for row in allowed:
            attributes = row.find_all("td")
            if ((attributes[0].text).isdigit() == True):
                formatted = {
                    "S.N": attributes[0].text,
                    "ContractNo": attributes[1].text,
                    "StockSymbol": attributes[2].text,
                    "BuyerBroker": attributes[3].text,
                    "SellerBroker": attributes[4].text,
                    "Quantity": attributes[5].text,
                    "Rate": attributes[6].text,
                    "Amount": attributes[7].text,
                }
                container.append(formatted)
        return pd.DataFrame(container)
    except:
        return pd.DataFrame()


def initiate_extraction():
    try:
        items = 250000
        limit = 20000
        df = pd.DataFrame()
        for i in range(20):
            if ((i+1)*limit <= items):
                soup = get_floorsheet_response(i+1, limit)
                df_new = extract_table(soup)
                df = df.append(df_new, ignore_index=True)
                #filename = "floorsheet_{}.csv".format(datetime.today().strftime('%Y_%m_%d'))
        # df.to_csv(os.path.join('floorsheets',filename))
        return df
    except:
        print("Oops! Something went wrong.")
        return pd.DataFrame()

# df = initiate_extraction()


def company_list():
    path = os.path.join("data", "0_NepseCompanyList.csv")
    company_df = pd.read_csv(path)
    company_list = company_df['Symbol'].to_list()
    return company_list


def main():
    df = initiate_extraction()
    data = df
    print("Raw dataframe length:", len(data))
    data = data.drop_duplicates()
    print("Duplicate dropped dataframe dataframe length:", len(data))
    company_filtered = data[data['StockSymbol'].isin(company_list())]
    print("Filtered dataframe:", len(company_filtered))
    filename = "floorsheet_{}.csv".format(
        datetime.today().strftime('%Y_%m_%d'))
    company_filtered.to_csv(os.path.join('data', filename))
    return True


main()
