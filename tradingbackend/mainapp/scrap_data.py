from selenium import webdriver
import time
import pandas as pd
import psycopg2
conn = psycopg2.connect(database="coindb",
                        host="localhost",
                        user="shubham",
                        password="admin",
                        port="5432")

def get_data():
    url = "https://coinmarketcap.com/"
    table_locator = "xpath", "//table"

    driver = webdriver.Chrome()
    driver.get(url)
    i = 0
    while i < 8:
        driver.execute_script("window.scrollBy(0, window.innerHeight)")
        driver.execute_script("window.scrollBy(0, window.innerHeight)")
        time.sleep(2)
        i += 1
    table_webelement = driver.find_element(*table_locator)
    table_html = table_webelement.get_attribute("outerHTML")

    # load the HTML table to Pandas DataFrame

    dataframes = pd.read_html(table_html)
    table_dataframe = dataframes[0]
    return table_dataframe

def update_data():

    while True:

        df = get_data()

        df = df[["Name", "Price", "Volume(24h)","1h %","24h %","7d %","Market Cap","Circulating Supply"]]
        df["Name"] = df["Name"].apply(lambda x: x.split(" ")[0])
        df["Price"] = df["Price"].apply(lambda x: float(x.replace(",", "").replace("$", "")))


        df["Volume(24h)"] = df["Volume(24h)"].apply(lambda x: str(x).split(" ")[0].replace(",", "").replace("$", ""))
        df["1h %"] = df["1h %"].apply(lambda x: str(x).split(" ")[0].replace(",", "").replace("$", ""))
        df["24h %"] = df["24h %"].apply(lambda x: str(x).split(" ")[0].replace(",", "").replace("$", ""))
        df["7d %"] = df["7d %"].apply(lambda x: str(x).split(" ")[0].replace(",", "").replace("$", ""))

        df["Circulating Supply"] = df["Circulating Supply"].apply(lambda x: str(x).split(" ")[0].replace(",", "").replace("$", ""))
        #defining connection
        conn = psycopg2.connect(database="coindb",
                                host="localhost",
                                user="shubham",
                                password="admin",
                                port="5432")
        cursor = conn.cursor()
        for index, val in df.iterrows():
            try:

                cursor.execute(f"""SELECT coin_name FROM mainapp_coindata where coin_name='{val['Name']}'""")
                data=cursor.fetchone()

                #if coin name doesn't exist then insert it into table.
                if data==None:

                    cursor.execute(f"""INSERT INTO mainapp_coindata(coin_name, coin_price, coin_volume, coin_1h_per
                            ,coin_24h_per,coin_7d_per, coin_mkt_cap, coin_circulating_supply)
                             VALUES ('{val['Name']}' ,{val['Price']}, '{val['Volume(24h)']}',
                              '{val['1h %']}', '{val['24h %']}', '{val['7d %']}','{val['Market Cap']}','{val['Circulating Supply']}')""")

                    conn.commit()
                else:

                    #update existing coin
                    cursor.execute(f"""UPDATE mainapp_coindata set coin_price={val['Price']}
                                                ,coin_volume ='{val['Volume(24h)']}'
                                                , coin_1h_per ='{val['1h %']}'
                                                ,coin_24h_per ='{val['24h %']}'
                                                ,coin_7d_per ='{val['7d %']}'
                                                , coin_mkt_cap ='{val['Market Cap']}'
                                                , coin_circulating_supply ='{val['Circulating Supply']}'                                                
                                                  where coin_name='{val['Name']}'""")
                    conn.commit()

            except Exception as e:
                print(e)
        conn.close()
        time.sleep(3)

update_data()