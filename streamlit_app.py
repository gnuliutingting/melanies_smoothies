

      # Import necessary libraries
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want for your custom Smoothie!")



name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be", name_on_order)



# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get the list of fruits from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()

# Extract fruit names into a list
fruit_names = [row['FRUIT_NAME'] for row in my_dataframe]

# Multiselect widget for choosing up to 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    options=fruit_names,
    max_selections=5
)

# Only process if ingredients are selected
if ingredients_list:
    ingredients_string =''
      
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        st.subheader(fruit_chosen + 'Nutriention Information') 
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data= smoothiefroot_response.json(), use_container_width = True)

          # Show selected ingredients
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

st.write(my_insert_stmt)
      
# Insert the ingredients into Snowflake when the submit button is pressed
time_to_insert = st.button('Submit Order')
      
if time_to_insert:
              
 # Execute the SQL statement
session.sql(my_insert_stmt).collect()
      
 # Show success message
st.success(f"Your Smoothie is ordered,{name_on_order}!", icon="✅")




        
