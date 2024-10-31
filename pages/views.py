
from django.shortcuts import render
import requests
from .lib.exchange_rate import fetch_exchange_rates
from .lib.map import map
from django.http import JsonResponse

def index(request):
    exchange_rates=fetch_exchange_rates()
    html_path=map(exchange_rates)
    return render(request, "pages/index.html", {"exchange_rates": exchange_rates, "html_path": html_path})



def exchange_calculation(request):
    exchange_rates = fetch_exchange_rates()  # 獲取匯率
    results = None  # 初始化結果為 None
    print("exchangeTest")

    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))  # 用戶輸入的金額，默認為0
        currency_from = request.POST.get('currency_from')  # 從哪種幣別兌換
        currency_to = request.POST.get('currency_to')  # 換成哪種幣別
        
        # 將匯率轉換為字典，便於查找
        exchange_rate_dict = {rate['currency']: rate['rate'] for rate in exchange_rates}

        # 獲取幣別的匯率
        rate_from = exchange_rate_dict.get(currency_from)
        rate_to = exchange_rate_dict.get(currency_to)

        # 計算兌換結果
        if rate_from and rate_to and rate_to != 0:  # 確保匯率不為0，避免除以0的錯誤
            results = round((amount / rate_to) * rate_from,2)

            print(results)

    # 返回 JSON 響應，告訴前端重新整理頁面
    return JsonResponse({ 'results': results})


def about(request):
    return render(request, "pages/about.html")
