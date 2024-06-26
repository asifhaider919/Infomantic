import streamlit as st

# Set the title of the app
st.title("Simple Calculator")

# Create input fields for the two numbers
num1 = st.number_input("Enter the first number", value=0.0, step=1.0)
num2 = st.number_input("Enter the second number", value=0.0, step=1.0)

# Create a dropdown for the operations
operation = st.selectbox("Select operation", ("Add", "Subtract", "Multiply", "Divide"))

# Perform the calculation based on the selected operation
result = None
if operation == "Add":
    result = num1 + num2
elif operation == "Subtract":
    result = num1 - num2
elif operation == "Multiply":
    result = num1 * num2
elif operation == "Divide":
    if num2 != 0:
        result = num1 / num2
    else:
        st.error("Cannot divide by zero!")

# Display the result
if result is not None:
    st.write(f"The result of {operation.lower()}ing {num1} and {num2} is {result}")

# Add an optional footer
st.write("Powered by Streamlit")
