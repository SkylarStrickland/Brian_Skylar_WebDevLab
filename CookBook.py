import streamlit as st
import os

# Define the recipe pages with an optional serving size parameter and image
def recipe(name, serving_size=1):
    st.title(name + " Recipe") #1st New Stremalit Methods
    image_filename = os.path.join("CookBookImages/"+name.lower() + ".jpg") #Will Include 3 Images
    st.image(image_filename, use_column_width=True)
    st.header("Ingredients:")
    if name == "Pasta":
        pasta_quantity = 200 * serving_size
        tomato_sauce_quantity = 2 * serving_size
        st.write(f"- {pasta_quantity}g pasta")
        st.write(f"- {tomato_sauce_quantity} cups of tomato sauce")
    elif name == "Pizza":
        pizza_dough_quantity = serving_size
        st.write(f"- {pizza_dough_quantity} pizza dough")
        st.write("- Tomato sauce")
        st.write("- Mozzarella cheese")
    elif name == "Salad":
        lettuce_quantity = 2 * serving_size
        tomatoes_quantity = 4 * serving_size
        st.write(f"- {lettuce_quantity} cups of lettuce")
        st.write(f"- {tomatoes_quantity} tomatoes")
    st.header("Instructions:")
    if name == "Pasta":
        st.write("1. Boil the pasta in salted water until al dente.")
        st.write("2. Heat the tomato sauce in a pan.")
        st.write("3. Drain the pasta and mix it with the sauce.")
        st.write("4. Serve hot!")
    elif name == "Pizza":
        st.write("1. Preheat your oven to 475°F (245°C).")
        st.write("2. Roll out the pizza dough into your desired shape.")
        st.write("3. Spread tomato sauce on the dough.")
        st.write("4. Sprinkle mozzarella cheese on top.")
        st.write("5. Bake for 12-15 minutes or until the crust is golden and the cheese is bubbly.")
        st.write("6. Enjoy!")
    elif name == "Salad":
        st.write("1. Wash and chop the lettuce.")
        st.write("2. Dice the tomatoes.")
        st.write("3. Toss lettuce and tomatoes together.")
        st.write("4. Add your favorite salad dressing.")
        st.write("5. Serve and enjoy!")

# Create navigation sidebar
st.sidebar.title("Cookbook")
recipe_choice = st.sidebar.radio("Select a Recipe", ["Pasta", "Pizza", "Salad"])#2nd New Streamlit Method

# Add an input field for serving size
serving_size = st.sidebar.number_input("Serving Size", min_value=1, value=1)#3rd New Streamlit Method

# Display the selected recipe page with serving size and image
if recipe_choice == "Pasta":
    recipe("Pasta", serving_size)
elif recipe_choice == "Pizza":
    recipe("Pizza", serving_size)
elif recipe_choice == "Salad":
    recipe("Salad", serving_size)
