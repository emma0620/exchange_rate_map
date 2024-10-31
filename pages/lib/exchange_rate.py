import requests

def fetch_exchange_rates():
    url = 'https://rate.bot.com.tw/xrt/flcsv/0/day'  # 牌告匯率 CSV 網址
    rate = requests.get(url)  
    rate.encoding = 'utf-8'   
    rt = rate.text             
    rts = rt.split('\n')       
    exchange_rates = [] 

   
    currency_to_country = {
        'USD': ('United States of America', '美金'),
        'HKD': ('Hong Kong', '港幣'),
        'GBP': ('United Kingdom', '英鎊'),
        'AUD': ('Australia', '澳幣'),
        'CAD': ('Canada', '加拿大幣'),
        'SGD': ('Singapore', '新加坡幣'),
        'CHF': ('Switzerland', '瑞士法郎'),
        'JPY': ('Japan', '日圓'),
        'ZAR': ('South Africa', '南非幣'),
        'SEK': ('Sweden', '瑞典幣'),
        'NZD': ('New Zealand', '紐元'),
        'THB': ('Thailand', '泰幣'),
        'PHP': ('Philippines', '菲國比索'),
        'IDR': ('Indonesia', '印尼幣'),
        'EUR': ('Eurozone', '歐元'),
        'KRW': ('South Korea', '韓元'),
        'VND': ('Vietnam', '越南盾'),
        'MYR': ('Malaysia', '馬來幣'),
        'CNY': ('China', '人民幣'),
        'TWD': ('Taiwan', '台幣'),  
    }

    for line in rts:  
        try:
            data = line.split(',')  
            if len(data) > 12:  
                try:
                    rate = float(data[12]) if data[12] != '-' else 0  
                except ValueError:
                    continue  # 當遇到無法轉換的值時，跳過該項目

                currency_code = data[0]  # 第一個項目 (貨幣代碼)
                country_name = currency_to_country.get(currency_code, (None, None))[1]  # 獲取對應國家
                
                # 只有當有對應的國家時才添加
                if country_name:
                    currency_data = {
                        'country': currency_to_country[currency_code][0], 
                        'currency_zh': currency_to_country[currency_code][1],
                        'currency': currency_code,  
                        'rate': rate               
                    }
                    exchange_rates.append(currency_data)  
        except Exception as e:
            print(f"Error processing line: {line}, Error: {e}")

    exchange_rates.append({
        'country': 'Taiwan',
        'currency_zh': '台幣',
        'currency': 'TWD',
        'rate': 1
    })
    
    return exchange_rates
