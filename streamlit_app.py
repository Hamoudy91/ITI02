import streamlit as st
import pandas as pd

# Load the CSV file
data_path = 'PartITIT2024 - Sheet1.csv'  # Update with your actual file path

try:
    parts_df = pd.read_csv(data_path, sep=',', encoding='utf-8')
    st.write("Part Finder")
except FileNotFoundError:
    st.error(f"File not found: {data_path}. Please ensure the file is uploaded.")
    st.stop()
except pd.errors.ParserError:
    st.error(f"Error parsing the file: {data_path}. Please check the file formatting.")
    st.stop()

# Display the column names to debug (if needed)
# st.write(parts_df.columns)

# Clean up the columns if necessary (e.g., removing extra spaces)
parts_df.columns = parts_df.columns.str.strip()

# User input for Model Number
model_input = st.text_input("Enter your model number")

# If model number is entered, filter the data
if model_input:
    filtered_df = parts_df[parts_df['Model'].str.contains(model_input, case=False, na=False)]
    if filtered_df.empty:
        st.write("No parts found for this model.")
    else:
        # Drop-down for Part Description (TCLNA)
        part_description = st.selectbox("Select Part Description (TCLNA)", filtered_df['Part Description (TCLNA)'].unique())

        # Display Part Number, Year Sold, and Type based on the selection
        selected_part = filtered_df[filtered_df['Part Description (TCLNA)'] == part_description]
        if not selected_part.empty:
            st.write(f"**Part Number**: {selected_part['Part No.'].values[0]}")
            st.write(f"**Year Sold**: {selected_part['Year Sold'].values[0]}")
            st.write(f"**Type**: {selected_part['Type'].values[0]}")
            
            # Ask if user wants to see the price
            if st.checkbox("Would you like to see the price?"):
                st.write(f"**Price**: ${selected_part['Price'].values[0]}")
        else:
            st.write("No details found for the selected part.")
