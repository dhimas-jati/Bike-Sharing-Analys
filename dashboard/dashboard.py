import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_count_daily_df(days_df):
    count_daily= days_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-30"'))
    return count_daily

def create_total_registered_df(days_df):
   regis_df =  days_df.groupby(by="dteday").agg({"registered": "sum"})
   regis_df = regis_df.reset_index()
   regis_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return regis_df

def create_total_casual_df(days_df):
   casual_df =  days_df.groupby(by="dteday").agg({"casual": ["sum"]})
   casual_df = casual_df.reset_index()
   casual_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return casual_df

def create_count_day_df(days_df):
    oneweek_df = days_df.groupby("nameday").agg({"casual": "sum", "registered": "sum"})
    oneweek_df.reset_index(inplace=True)
    return oneweek_df

def create_count_hours_df(hours_df):
    oneday_df = hours_df.groupby("hr").agg({"casual": "sum", "registered": "sum"})
    oneday_df.reset_index(inplace=True)
    return oneday_df


days_df = pd.read_csv("dashboard/days.csv")
hours_df = pd.read_csv("dashboard/hours.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("dashboard/photo.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]
main_df_hours = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                       (hours_df["dteday"] <= str(end_date))]

count_daily = create_count_daily_df(main_df_days)
regis_df = create_total_registered_df(main_df_days)
casual_df = create_total_casual_df(main_df_days)
oneweek_df = create_count_day_df(main_df_days)
oneday_df = create_count_hours_df(main_df_hours)

st.header('Dashboard Bike Sharing :sparkles:')

st.subheader('Daily Bike Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = count_daily.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = regis_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = casual_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Persentase penyewa Registered dengan casual dari jumlah total Bike Sharing")

casual = sum(days_df['casual'])
registered = sum(days_df['registered'])

data = [casual, registered]
labels = 'casual', 'registered'

fig, ax1 = plt.subplots()
ax1.pie(x=data, labels=labels, autopct='%1.1f%%',colors=["#90CAF9", "#E67F0D"],)

st.pyplot(fig)

st.subheader("distribusi penyebaran Bike Sharing")
st.subheader("distribusi penyebaran Bike Sharing bedasarkan Day")

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(
        oneweek_df["nameday"],
        oneweek_df["casual"],
        left=oneweek_df["registered"],
        label="Casual",
    )
ax.barh(oneweek_df["nameday"], oneweek_df["registered"], label="Registered")

ax.set_title("Distribusi jenis dan jumlah Penyewa Berdasarkan Day", pad=30, fontsize=16)
ax.set_ylabel("day")
ax.set_xlabel("Count")

ax.legend(bbox_to_anchor=(1, 1.1), ncol=2)
st.pyplot(fig)

st.subheader("distribusi penyebaran Bike Sharing berasarkan hours")

fig, ax = plt.subplots(figsize=(15, 10))

ax.bar(
        oneday_df["hr"],
        oneday_df["casual"],
        bottom=oneday_df["registered"],
        label="Casual",
    )
ax.bar(oneday_df["hr"], oneday_df["registered"], label="Registered")

ax.set_title("Distribusi jenis dan jumlah Penyewa Berdasarkan Jam", fontsize=16, pad=30)
ax.set_ylabel("count")
ax.set_xlabel("Hour")
ax.set_xticks(oneday_df["hr"], [f"{time}:00" for time in oneday_df["hr"]])
ax.legend()
st.pyplot(fig)

st.caption("Copyright © Dj Submission 2024 ")
