import requests
from bs4 import BeautifulSoup
import pandas as pd


print('輸入股票代碼 查詢此 累季財務比率表')
stock_num = input()


url = f'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX%5FM%5FQUAR%5FACC&STOCK_ID={stock_num}&QRY_TIME=20203'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'referer': 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID={stock_num}'
}

resp = requests.post(url, headers=headers)
resp.encoding = 'utf-8'
# 根據 HTTP header 的編碼解碼後的內容資料（ex. UTF-8）
raw_html = resp.text
print('raw_html', raw_html)

soup = BeautifulSoup(raw_html, 'html.parser')



cash_flow_rows = soup.select('#row95 td nobr')
print('cash_flow_rows', cash_flow_rows)

# 將 Cash Flow 數值儲存到 list 中
cash_flow_list = []
for cash_flow_row in cash_flow_rows:
    # text 屬性可以取出我們在標籤內的值
    print(cash_flow_row.text)
    cash_flow_list.append(cash_flow_row.text)

    
# 透過選擇器選取到我們要的資料
roe_rows = soup.select('#row8 td nobr')
print(roe_rows)

# 將 ROE 數值儲存到 list 中
roe_list = []
for roe_row in roe_rows:
    # text 屬性可以取出我們在標籤內的值
    print(roe_row.text)
    roe_list.append(roe_row.text)
    

#property seansonal growth
psg_rows=soup.select('#row36 td nobr')
print(psg_rows)

psg_list=[]
for psg_row in psg_rows:
    print(psg_row.text)
    psg_list.append(psg_row.text)

    
# 將資料轉為 DataFrame
df = pd.DataFrame({
    '每股自由現金流量 (元)': cash_flow_list,
    '股東權益報酬率': roe_list,
    '資產總額季成長率': psg_list
})
# 第一列是標頭欄位，將第一列移除
df = df.drop(0)

df.to_csv(f'info_{stock_num}.csv', index=False)






