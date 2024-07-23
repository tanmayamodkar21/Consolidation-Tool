import streamlit as st
import pandas as pd
import io

st.title('Excel File Consolidator')

uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        df = pd.read_excel(uploaded_file)
        dfs.append(df)
    
    if dfs:
        consolidated_df = pd.concat(dfs, ignore_index=True)
        st.write("Consolidated Data")
        st.write(consolidated_df)
        
        # Convert the DataFrame to a binary Excel object
        @st.cache_data
        def convert_df_to_excel(df):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return buffer.getvalue()
        
        excel_data = convert_df_to_excel(consolidated_df)
        
        st.download_button(
            label="Download Excel file",
            data=excel_data,
            file_name='consolidated_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
