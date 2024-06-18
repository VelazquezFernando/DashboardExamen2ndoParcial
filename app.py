import pandas as pd  #pip install pandas openpyxl
import plotly.express as px  #pip install plotly-express
import streamlit as st #pip install streamlit

# para el emoji -> https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sale Dashboard", page_icon="bar_chart:",
                   layout="wide"
                   
                   )
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,

    )

# Add "hour " column to dataframe
    df["hour"] =pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df


df = get_data_from_excel()
# primera prueba   ->st.dataframe(df)



#-------------------- SIDEBAR    -----------------
#  filtro 
#  Seleccionador de ciudades
st.sidebar.header("Please filter here:")
city = st.sidebar.multiselect(
    "Select the city:",
    options=df["City"].unique(),
    default=df["City"].unique()

)
#  filtro 
#  Seleccionador de tipo de cliente
st.sidebar.header("Please filter here:")
customer_type = st.sidebar.multiselect(
    "Select the Customer type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()

)
#  filtro 
#  Seleccionador de genero
st.sidebar.header("Please filter here:")
gender = st.sidebar.multiselect(
    "Select the gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()

)

#aqui hacemos nuestra primera query que sera la seleccion
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender" 
)

st.dataframe(df_selection)



#----------------- MAIN PAGE ----------
#---- Aqui vienen nuestras principales KPI's

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")


# Sales by product line [BAR CHART]
# massive help with jupiterNoteBook


sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


#st.plotly_chart(fig_product_sales)

# Cuando lo vemos en jupiter notebook, vemos que Time esta como un objeto que es como un python string
# primero necesitamos convertirlo a datetime object   con to_datetime function

# Sales by hour [BARCHART]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title="<b>Sales by hour </b>",
    color_discrete_sequence=["#0083b8"] * len(sales_by_hour),
    template = "plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis= dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False)),
)

#st.plotly_chart(fig_hourly_sales)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width =True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)



#-------- HIDE STREAMLIT STYLE ------
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html = True)

