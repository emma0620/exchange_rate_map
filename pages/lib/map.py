import geopandas as gpd
import plotly.express as px

def map(exchange_rates):
    # 將匯率資料轉換為字典
    rates_dict = {rate['country']: (rate['rate'], rate['currency']) for rate in exchange_rates}
    
    
    world = gpd.read_file("data/ne_110m_admin_0_countries.shp")
    
    # 添加匯率和幣別資料到地圖數據
    world['exchange_rate'] = world['NAME'].map(lambda country: rates_dict.get(country, (None, None))[0])
    world['currency'] = world['NAME'].map(lambda country: rates_dict.get(country, (None, None))[1])

   
    fig = px.choropleth(
        world,
        geojson=world.geometry,
        locations=world.index,
        color="exchange_rate",
        hover_name="NAME",
        hover_data={'exchange_rate': True},
        color_continuous_scale="Viridis",
        labels={'exchange_rate': '匯率'}
    )

    # 自訂 hovertemplate
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>幣別: %{customdata[1]}<br>匯率: %{z:.5f}<extra></extra>",
        hovertext=world['NAME'],
        customdata=world[['exchange_rate', 'currency']]
    )

    # 設置地圖格式
    fig.update_geos(showcoastlines=True, coastlinecolor="Black", projection_type="natural earth")
    fig.update_layout(
        title="世界各國匯率地圖",
        title_x=0.5,
        coloraxis_showscale=False  # 隱藏顏色條
    )

    # 將地圖保存為 HTML
    html_path = 'static/map_with_exchange_rates.html'
    fig.write_html(html_path)

    return html_path
