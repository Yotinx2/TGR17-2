import pymongo
import math
import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
#import numpy as np
#import plotly.figure_factory as ff

st.set_page_config(page_title="Artemis",
                    page_icon=":water:",
                    layout="wide")
st.title("ระบบแสดงผลน้ำในเขื่อนหัวนา")
st.header("By TGR17")
# # Add histogram data
# #x1 = np.random.randn(200) - 2
# #x2 = np.random.randn(200)
# #x3 = np.random.randn(200) + 2

# # Group data together
# #hist_data = [x1, x2, x3]

# #group_labels = ['Group 1', 'Group 2', 'Group 3']

# # Create distplot with custom bin_size
# #fig = ff.create_distplot(
# #        hist_data, group_labels, bin_size=[.1, .25, .5])

# # Plot!
# #st.plotly_chart(fig, use_container_width=True)


Df = pd.read_csv('mockupdata.waterdata.csv')
# #st.dataframe(df)

# st.sidebar.header("Please Filter Here:")

# city = st.sidebar.selectbox("Select the City:",
#                             options=df["City"].unique(),
#                             index=0
# )

# areaLocality = st.sidebar.multiselect("Select Area Locality:",
#                 options=df.query("City == @city")["Area_Locality"].unique(),
#                 default=df.query("City == @city")["Area_Locality"].unique()[0],
# )

# areaType = st.sidebar.selectbox("Select the Area Type:",
#                 options=df["Area_Type"].unique(),
#                 index=0
# )

# furnishing = st.sidebar.selectbox("Select the Furnishing Status:",
#                 options=df["Furnishing_Status"].unique(),
#                 index=0
# )
# df_selection = df.query("Area_Locality == @areaLocality & Area_Type == @areaType & Furnishing_Status == @furnishing"
# )
# #st.dataframe(df_selection)

# # ---- MAINPAGE ----
# st.title(":bar_chart: House Rent Dashboard")
# st.markdown("##")
# average_rent = round(df_selection["Rent"].mean(),1)
# average_size = round(df_selection["Size"].mean(), 2)
# left_column, right_column = st.columns(2)
# with left_column:
#         st.subheader("Average Rentalt:")
#         st.subheader(f"US $ {average_rent:,}")
# with right_column:
#         st.subheader("Average Size Room:")
#         st.subheader(f"M {average_size}")
# st.markdown("""---""")

# # BAR CHART Average rental
# average_rental_line = df_selection.groupby(by=["Furnishing_Status"])["Rent"].mean()
# #st.dataframe(average_rental_line)
# fig_average_rental = px.bar(
#         average_rental_line,
#         x="Rent",
#         y=average_rental_line.index,
#         orientation="h",
#         title="<b>Average Rental Line</b>",
#         color_discrete_sequence=["#0083B8"] * len(average_rental_line),
#         template="plotly_white",
# )
# fig_average_rental.update_layout(
#         plot_bgcolor="rgba(0,0,0,0)",
#         xaxis=(dict(showgrid=False))
# )

# # BAR CHART
# average_size_line = df_selection.groupby(by=["Furnishing_Status"])["Size"].mean()
# fig_average_size = px.bar(
#         average_size_line,
#         x="Size",
#         y=average_size_line.index,
#         title="<b>Average Size</b>",
#         color_discrete_sequence=["#0083B8"] * len(average_size_line),
#         template="plotly_white",
# )
# fig_average_size.update_layout(
#         plot_bgcolor="rgba(0,0,0,0)",
#         yaxis=(dict(showgrid=False)),
# )

# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig_average_rental, use_container_width=True)
# right_column.plotly_chart(fig_average_size, use_container_width=True)
# st.markdown("""---""")


# # Initialize connection.
# # Uses st.cache_resource to only run once.

# # MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"
# # @st.cache_resource
# # def init_connection():
# #     return pymongo.MongoClient(MONGO_DETAILS)

# # client = init_connection()

# # # Pull data from the collection.
# # # Uses st.cache_data to only rerun when the query changes or after 10 min.
# # @st.cache_data(ttl=600)
# # def get_data():
# #     db = client.streamlit
# #     items = db.Mypet.find()
# #     print(items)
# #     items = list(items)  # make hashable for st.cache_data
# #     return items

# # items = get_data()
# # print(items)
# # Print results.
# # for item in items:
# #     st.write(f"{item['name']} has a :{item['pet']}:")
# # Connect to MongoDB
client = pymongo.MongoClient("mongodb://tesarally:contestor@mongoDB:27017")
database = client["mockupdata"]
collection = database["waterdata"]


cursor = collection.find({})
data_list = list(cursor)

# Check if any data is found
if len(data_list) > 0:
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    # Drop the '_id' column
    df = df.drop('_id', axis=1)
    df.drop(df.index[-1], inplace=True)

    # Create two columns layout
    col1, col2 = st.columns(2)

    # Column 1: Display DataFrame
    with col1:
        st.write("ข้อมูลปริมาณน้ำในเขื่อน")
        st.write(df)

        # Display metrics
        st.write("Metrics:")
        
        # Metric 1: Average of WaterDataFront
        avg_water_data_front = df['WaterDataFront'].mean()
        st.metric("Average WaterDataFront", avg_water_data_front, delta_color="inverse")

        # Metric 2: Sum of WaterDataBack
        sum_water_data_back = df['WaterDataBack'].sum()
        st.metric("Total WaterDataBack", sum_water_data_back, delta_color="inverse")

    # Column 2: Display Line Chart and Bar Chart
    with col2:
        # Plot a line chart
        st.write("กราฟแสดงจำนวนน้ำที่ปล่อย:")
        line_chart = alt.Chart(df).mark_line().encode(
            x='Year:T',
            y='WaterDataFront:Q',
            color='Name:N',
            tooltip=['Year:T', 'WaterDataFront:Q', 'Name:N']
        ).properties(
            width=400,
            height=300
        ).interactive()
        st.altair_chart(line_chart, use_container_width=True)

        # Plot a bar chart
        st.write("กราฟแสดงข้อมูลน้ำในเขื่อน:")
        bar_chart = alt.Chart(df).mark_bar().encode(
            x='Year:T',
            y='WaterDataBack:Q',
            color='Name:N',
            tooltip=['Year:T', 'WaterDataBack:Q', 'Name:N']
        ).properties(
            width=400,
            height=300
        ).interactive()
        st.altair_chart(bar_chart, use_container_width=True)

else:
    st.write("No data found in the database.")