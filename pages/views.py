from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import requests
from django.http import HttpResponse, JsonResponse
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


def rate_history(request, currency):
    # Step 1: 抓取匯率資料
    url = f"https://rate.bot.com.tw/xrt/flcsv/0/L3M/{currency}"
    response = requests.get(url)

    if response.status_code != 200:
        return HttpResponse("無法取得匯率資料", status=404)

    # Step 2: 讀取 CSV 資料
    data = response.text
    df = pd.read_csv(StringIO(data), header=1, encoding="utf-8-sig")

    # 確認欄位名稱是否正確
    df.columns = [ "資料日期", "幣別", "匯率買入標籤", "現金買入", "即期買入", "遠期10天買入", "遠期30天買入", "遠期60天買入", "遠期90天買入", 
        "遠期120天買入", "遠期150天買入", "遠期180天買入", "匯率賣出標籤", "現金賣出"] + list(
        df.columns[14:]
    )

    # 保留所需欄位並轉換資料格式
    df = df[["資料日期", "現金買入", "現金賣出"]].dropna()
    df["資料日期"] = pd.to_datetime(df["資料日期"], format="%Y%m%d", errors="coerce")
    df["現金買入"] = pd.to_numeric(df["現金買入"], errors="coerce")
    df["現金賣出"] = pd.to_numeric(df["現金賣出"], errors="coerce")

    # 刪除任何缺失值
    df = df.dropna()

    # Step 3: 使用 Plotly 繪製匯率走勢圖
    fig = px.line(
        df,
        x="資料日期",
        y=["現金買入", "現金賣出"],
        labels={"value": "匯率", "variable": "匯率類型"},
        title=f"{currency} 匯率最近三個月走勢圖",
    )
    fig.update_layout(
        xaxis_title="資料日期", yaxis_title="匯率", template="plotly_white"
    )

    # Step 4: 儲存 Plotly 圖表為 HTML 文件
    html_path = f"static/images/{currency}_rate_history.html"
    fig.write_html(html_path)

    # Step 5: 回傳 iframe HTML 片段
    html_content = f"""
    <iframe src="/{html_path}" width="100%" height="400px" frameborder="0"
            style="background-color: #D1AEAD; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); border-radius: 5px;">
    </iframe>
    """
    return HttpResponse(html_content)


def about(request):
    return render(request, "pages/about.html")
