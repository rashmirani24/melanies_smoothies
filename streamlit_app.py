# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)



from snowflake.snowpark.functions import col

#session = get_active_session()


connection_parameters = {
    "account": "PKSMRXO-VGB03693",
    "user": "RASHMIRANI24",
    "password": "Omnamahshivay140823*",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}



session = Session.builder.configs(connection_parameters).create()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_list = st.multiselect('Choose upto 5 ingredients: ',my_dataframe,max_selections=5)
if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
