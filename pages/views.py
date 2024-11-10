import requests
from django.http import JsonResponse
from django.shortcuts import render

from .lib.exchange_rate import fetch_exchange_rates
from .lib.map import map


def index(request):
    exchange_rates = fetch_exchange_rates()
    html_path = map(exchange_rates)
    return render(
        request,
        "pages/index.html",
        {"exchange_rates": exchange_rates, "html_path": html_path},
    )


def exchange_calculation(request):
    exchange_rates = fetch_exchange_rates()  # 獲取匯率
    results = None

    if request.method == "POST":
        amount = float(request.POST.get("amount", 0))
        currency_from = request.POST.get("currency_from")
        currency_to = request.POST.get("currency_to")

        # 將匯率轉換為字典，便於查找
        exchange_rate_dict = {rate["currency"]: rate["rate"] for rate in exchange_rates}

        # 獲取幣別的匯率
        rate_from = exchange_rate_dict.get(currency_from)
        rate_to = exchange_rate_dict.get(currency_to)

        if rate_from and rate_to and rate_to != 0:
            results = round((amount / rate_to) * rate_from, 2)

    # 返回 JSON 響應，告訴前端重新整理頁面
    return JsonResponse({"results": results})


def about(request):
    return render(request, "pages/about.html")
