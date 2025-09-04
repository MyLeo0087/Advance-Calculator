import streamlit as st
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Initialize session state for page
if "page" not in st.session_state:
    st.session_state.page = "home"   # default page = home

# Sidebar buttons
st.sidebar.title("Choose Option : ")

if st.sidebar.button(f"🏠 Home Screen"):
    st.session_state.page = "home"

if st.sidebar.button(" 📱Numerical Calculator"):
    st.session_state.page = "calc"

if st.sidebar.button("♎ Unit Convertor"):
    st.session_state.page = "unit"

if st.sidebar.button("💰 Currency Convertor"):
    st.session_state.page = "curr"

if st.sidebar.button("🧾 Data Analysis"):
    st.session_state.page = "data"

if st.session_state.page == "home":
    st.title("Welcome To Advance Calculator 📱")
    st.subheader("Program by Darshan")

    st.markdown("""
    ### 🚀 Features Available:
    1. **🧮 Numerical Calculator** – Basic math operations  
    2. **📐 Unit Converter** – Convert Length, Weight, Temperature 
    4. **💱 Currency Converter** – Convert money between currencies  
    3. **📊 Data Analysis** – Upload & analyze CSV file s  
    """)


elif st.session_state.page == "calc":
    operator = st.selectbox(
        "What is your operation?",
        ["None", "Addition", "Substraction", "Multiplication", "Divided"]
    )

    if operator != "None":
        num_1 = st.number_input("Enter your first number :", value=10)  
        num_2 = st.number_input("Enter your second number :", value=0)   #

        if operator == "Addition":
            st.success(f"The sum is **{num_1 + num_2}**")
        elif operator == "Substraction":
            st.success(f"The subtraction is **{num_1 - num_2}**")
        elif operator == "Multiplication":
            st.success(f"The multiplication is **{num_1 * num_2}**")
        elif operator == "Divided":
            if num_2 != 0:
                st.success(f"The division is **{num_1 / num_2}**")
            else:
                st.error("Division by zero not allowed ❌")

elif st.session_state.page == "unit" :
    st.title("Unit Converter ⚙️")


    unit_categories = {
        "Length": ["Meter", "Kilometer", "Centimeter", "Inch", "Foot"],
        "Weight": ["Kilogram", "Gram", "Pound", "Ounce"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
    }


    category = st.selectbox("Select conversion type:", list(unit_categories.keys()))

    col1,col2,col3 = st.columns(3)

    with col1:
        from_unit = st.selectbox("From unit:", unit_categories[category])

    with col3:
        to_unit = st.selectbox("To unit:", unit_categories[category])


    with col2:
        value = st.number_input("Enter value:", value=1.0)

    if st.button("Convert"):
        result = None

        if category == "Length":
            factor = {"Meter":1, "Kilometer":1000, "Centimeter":0.01, "Inch":0.0254, "Foot":0.3048}
            result = value * factor[from_unit] / factor[to_unit]

        elif category == "Weight":
            factor = {"Kilogram":1, "Gram":0.001, "Pound":0.453592, "Ounce":0.0283495}
            result = value * factor[from_unit] / factor[to_unit]

        elif category == "Temperature":
      
            if from_unit == "Celsius":
                temp_c = value
            elif from_unit == "Fahrenheit":
                temp_c = (value - 32) * 5/9
            elif from_unit == "Kelvin":
                temp_c = value - 273.15

    
            if to_unit == "Celsius":
                result = temp_c
            elif to_unit == "Fahrenheit":
                result = temp_c * 9/5 + 32
            elif to_unit == "Kelvin":
                result = temp_c + 273.15

        st.success(f"{value} {from_unit} = {result} {to_unit}")

elif  st.session_state.page == "curr":
    # Hardcoded exchange rates relative to USD
    exchange_rates = {
        "USD": 1,
        "EUR": 0.91,
        "GBP": 0.78,
        "INR": 83.5,
        "JPY": 148.0,
        "AUD": 1.57,
        "CAD": 1.34,
        "CHF": 0.91,
        "CNY": 6.91
    }

    st.title("Currency Converter ")

    # User input
    amount = st.number_input("Enter amount", min_value=0.0, value=1.0)
    from_currency = st.selectbox("From Currency", list(exchange_rates.keys()))
    to_currency = st.selectbox("To Currency", list(exchange_rates.keys()))

    # Conversion
    if st.button("Convert"):
        # Convert amount to USD first, then to target currency
        usd_amount = amount / exchange_rates[from_currency]
        converted_amount = usd_amount * exchange_rates[to_currency]
        st.success(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

    
##Data analysis

elif st.session_state.page == "data" :

    st.title("Data Analysis")

    # File uploader
    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file:
        df = pd.read_csv(file)
        
        with st.expander("Preview"):
            st.subheader("Data Preview")
            st.dataframe(df)
        
        with st.expander("Summary"):
            st.subheader("Data Summary")
            st.write(df.describe())
        
    
        with st.expander("Filter"):
            st.subheader("Filter Data")
            fun = st.selectbox("Operation", ["Unique value", "Specific Column", "Show Column"])
            
            if fun == "Unique value":
                col = st.selectbox("Select Column", df.columns)
                if col:
                    unique_values = df[col].unique()
                    st.write(f"Unique values in **{col}**:")
                    st.write(unique_values)
            
            elif fun == "Specific Column":
                cols = st.multiselect("Select columns to show", df.columns)
                if cols:
                    st.dataframe(df[cols])
            
            elif fun == "Show Column":
                st.write("All columns in the dataset:")
                st.write(list(df.columns))

        with st.expander("Graph Plot"):
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns

            st.subheader("Graph Plotting")

            # Select plot type
            plot_type = st.selectbox("Select Plot Type", ["Histogram", "Boxplot", "Line Plot", "Bar Plot", "Pie Chart"])

            # Plot based on type
            if plot_type in ["Histogram", "Boxplot", "Line Plot"]:
                if len(numeric_cols) == 0:
                    st.warning("No numeric columns available for this plot type!")
                else:
                    col = st.selectbox("Select numeric column", numeric_cols)

                    fig, ax = plt.subplots()
                    if plot_type == "Histogram":
                        sns.histplot(data=df, x=col, kde=True, ax=ax)
                    elif plot_type == "Boxplot":
                        sns.boxplot(data=df, x=col, ax=ax)
                    elif plot_type == "Line Plot":
                        sns.lineplot(data=df, y=col, ax=ax)
                    ax.set_title(f"{plot_type} of {col}")
                    st.pyplot(fig)

            elif plot_type == "Bar Plot":
                if len(categorical_cols) == 0:
                    st.warning("No categorical columns available for bar plot!")
                else:
                    col = st.selectbox("Select categorical column", categorical_cols)
                    counts = df[col].value_counts()
                    fig, ax = plt.subplots()
                    sns.barplot(x=counts.index, y=counts.values, ax=ax)
                    ax.set_title(f"Bar Plot of {col}")
                    ax.set_ylabel("Count")
                    st.pyplot(fig)

            elif plot_type == "Pie Chart":
                if len(categorical_cols) == 0:
                    st.warning("No categorical columns available for pie chart!")
                else:
                    col = st.selectbox("Select categorical column", categorical_cols)
                    counts = df[col].value_counts()
                    fig, ax = plt.subplots()
                    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
                    ax.set_title(f"Pie Chart of {col}")
                    ax.axis("equal")  # Equal aspect ratio ensures pie is circular
                    st.pyplot(fig)

            
