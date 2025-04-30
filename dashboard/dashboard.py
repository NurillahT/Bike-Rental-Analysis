import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#  Membuat fungsi
def create_linechart(selected_day):
    fig, ax = plt.subplots(figsize=(10,6))

    ax = sns.lineplot(data=selected_day, x='month', y='count', hue='year', errorbar=None, marker='o')

    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Penyewa')
    ax.legend(title='Year')
    ax.grid(True, axis="x", linestyle="--")
    for spine in ax.spines.values():
        spine.set_visible(False)

    for line in ax.lines:
        for x, y in zip(line.get_xdata(), line.get_ydata()):
            ax.annotate(f"{int(y)}", xy=(x, y), xycoords='data',xytext=(0, 6),
                        textcoords='offset pixels', ha='center', va='bottom')
    
    st.pyplot(fig)

def create_barchart(selected_day, x, y, hue, palette, order, xlabel):
    fig = plt.figure(figsize=(5,3))
    ax = sns.barplot(data=selected_day, x=x, y=y, hue=hue,
                    palette=palette, order=order, errorbar=None)
                    
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xlabel(f"{xlabel}")
    ax.set_ylabel(None)

    for bar in ax.containers:
        ax.bar_label(bar, fmt= '%0.1f', label_type='edge' )

    st.pyplot(fig)

def create_scatterplot(selected_day, x, y, hue, palette, xlabel, ylabel):
    fig = plt.figure(figsize=(10, 6))
    ax = sns.scatterplot(data=selected_day, x=x, y=y, hue=hue, palette=palette, )
    
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xlabel(f'{xlabel}')
    ax.set_ylabel(f'{ylabel}')
    ax.legend(title='Musim')
    ax.grid(True, linestyle=":")
    st.pyplot(fig)

def create_sunburst(bike_day):
    monthly_season = bike_day.groupby(by=["season", "month"], observed=False)["date"].count().reset_index()
    fig = px.sunburst(monthly_season, path=['season', 'month'], values='date',  color='season',
                   color_discrete_map=dict(spring='#328E6E', summer='#ffd500', fall= '#cc3300', winter='#99ddff'),)
    st.plotly_chart(fig)

def season_rental_color(season):
    palette=dict(spring='lightgrey', summer='lightgrey', fall= 'lightgrey', winter='lightgrey')
    if season == 'spring':
        palette['spring']='#328E6E'
    elif season == 'summer':
        palette['summer']='#ffff66'
    elif season == 'fall':
        palette['fall']= '#FE7743'
    elif season == 'winter':
        palette['winter']='#99ddff'
    else:
        palette=dict(spring='#328E6E', summer='#ffff66', fall= '#FE7743', winter='#99ddff')
    return palette
    
def season_atemp_color(season):
    palette=dict(spring='lightgrey', summer='lightgrey', fall= 'lightgrey', winter='lightgrey')
    if season == 'spring':
        palette['spring']='#215e49'
    elif season == 'summer':
        palette['summer']='#e6b800'
    elif season == 'fall':
        palette['fall']= '#7f2401'
    elif season == 'winter':
        palette['winter']='#004080'
    else:
        palette=dict(spring='#215e49', summer='#e6b800', fall= '#7f2401', winter='#004080')
    return palette

# Memuat Data
bike_day = pd.read_csv('dashboard/final_day.csv')

with st.container(border=True):
    st.markdown("<h1 style='text-align: center;'>Bike Rental Dashboard</h1>", unsafe_allow_html=True)

    st.divider()    

    col0, col1, col2 = st.columns(3)
    with col0: 
        sum_11 = bike_day[bike_day["year"] ==  2011]["count"].sum()
        st.metric("2011 :", value=sum_11)
    with col1:
        sum_12 = bike_day[bike_day["year"] ==  2012]["count"].sum()
        st.metric("2012 :", value=sum_12, delta=int(sum_12-sum_11))
    with col2:
        # with st.container(border=True, height=110):
        sum_all = bike_day["count"].sum()
        st.metric("Total Rental:", value=sum_all)

    years = bike_day['year'].unique()
    years = np.append(years, "All")
    select_year = st.selectbox("Select Year", options=(years))

    if select_year == "All":
        selected_day = bike_day
        st.subheader("Monthly Rental Comparison")
    else:
        selected_day = bike_day[bike_day['year'] == int(select_year)]
        st.subheader(f"Monthly Rental: Year {select_year}")

    create_linechart(selected_day)

    st.markdown('######', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<h5>Average Rental by Weather</h5>", unsafe_allow_html=True)
        create_barchart(selected_day, x='weather', y='count', hue='weather', palette='mako', order=bike_day.sort_values('count', ascending=False).weather, xlabel='Cuaca')
        
    with col4:
        st.markdown("<h5>Average Rental by ATemprature</h5>", help="Apparent Temprature", unsafe_allow_html=True)
        create_barchart(selected_day, x='atemp_category', y='count', hue='atemp_category',
                        palette='coolwarm', order=None, xlabel='Tingkat Suhu')

    st.divider()

    create_sunburst(bike_day)

    cols1,cols2 = st.columns([.2,.7])
    with cols2:
        seasons=['Spring', 'Summer', 'Fall', 'Winter', 'All']
        select_season = st.segmented_control("Select Season", options=seasons, default='All', label_visibility='collapsed').lower()

        if select_season == "all":
            selected_season = selected_day
        else: 
            selected_season = selected_day[selected_day['season'] ==  select_season]

    st.markdown("<h2 style='text-align: center;'>Seasonal Rental</h2>", unsafe_allow_html=True)
    
    create_scatterplot(selected_season, x='atemp', y='count', hue='season', palette=dict(spring='#2BA02D', summer='#ffaa08', fall='#AA2222', winter='#0D47A1'), xlabel='Suhu', ylabel='Jumlah Peyewa')

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("<h5>Average Rental</h5>", unsafe_allow_html=True)

        create_barchart(selected_day, x='season', y='count', hue='season', palette=season_rental_color(select_season), order=None, xlabel='Musim')
        
    with col6:
        st.markdown("<h5>Average ATemprature</h5>", help="Apparent Temprature", unsafe_allow_html=True)

        create_barchart(selected_day, x='season', y='atemp', hue='season',
                        palette=season_atemp_color(select_season), order=None, xlabel='Musim')

        with st.popover("ATemp"):
            info_atemp = bike_day.iloc[:,-2:].drop_duplicates('atemp_range')
            st.dataframe(info_atemp, hide_index=True)

st.markdown('<p style="color:grey; text-align:center;">Copyright © 2025 | Nurillah Tsany W</p>', unsafe_allow_html=True)
