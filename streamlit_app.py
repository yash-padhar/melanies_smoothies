# Import python packages
import streamlit as st

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

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'Choose upto 5 ingridents:'
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert=st.button('Submit Order')

    if time_to_insert:

        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
