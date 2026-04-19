import streamlit as st
import os
import folium
from streamlit_folium import st_folium
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
#Set up tên dashboard
st.set_page_config(page_title= "Kiểm tra tiến độ giao hàng", layout="wide")
st.title("🚚 Hệ thống Giám sát Vận tải")
#Giả lập dữ liệu 
data = pd.DataFrame({
    'Xe': ["Xe 1", "Xe 2", "Xe 3"],
    "Tên tài xế":["Hoàng", "Dương", "Khang"],
    "Trạng thái":["Đang giao", "Trễ chuyến", "Đang nghỉ"],
    "Tải trọng": [85,40,0],
    'lat': [10.776, 10.772, 10.780],
    'lon': [106.667, 106.658, 106.675]})
st.sidebar.header("Bộ lọc điều hành")
status_filter  = st.sidebar.multiselect(
    "Chọn trạng thái xe:",
    options=data['Trạng thái'].unique(),
    default=data['Trạng thái'].unique()
)
filtered_data= data[data["Trạng thái"].isin(status_filter)]
#Hiển thị chỉ số KPI
col1, col2, col3= st.columns(3)
col1.metric("Tổng số xe", len(data))
col2.metric("Xe đang hoạt động", len(data[data["Trạng thái"]!= "Đang nghỉ"]))
col3.metric("Tỷ lệ đúng giờ", "92%", "-2% so với hôm qua")
#Khởi tạo bản đồ
left_col, right_col = st.columns([2,1])
with left_col:
    st.header("Vị trí xe")
    m=folium.Map(location=[10.8231,106.6297], zoom_start=14)
    for _, row in filtered_data.iterrows():
        color="green" if row["Trạng thái"]=='Đang giao' else "red" if row["Trạng thái"]=="Trễ chuyển" else "yellow"
        folium.Marker([row['lat'], row['lon']],popup=f"{row['Xe']} - {row['Tên tài xế']}", icon=folium.Icon(color=color, icon="truck")).add_to(m)
st_folium(m, width=700, height=500)

with right_col:
    st.subheader("Chi tiết")
    st.dataframe(filtered_data[["Xe", "Tên tài xế", "Trạng thái", "Tải trọng"]])


