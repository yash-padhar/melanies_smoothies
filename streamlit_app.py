# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session=cnx.session()

title = st.text_input("Name on Snoothie")
st.write("The Name on the smoothie will be:", title)

name_on_order=title

# Write directly to the app
st.title("🥤Customize Your Smoothie !🥤")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

pd_df=my_dataframe.to_pandas()

ingredients_list=st.multiselect(
    'Choose upto 5 ingridents:'
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0] 
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert=st.button('Submit Order')

    if time_to_insert:

        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
