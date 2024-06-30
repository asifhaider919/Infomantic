import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET

# Function to parse XML data
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    data = []
    
    for mo in root.findall('.//{raml20.xsd}managedObject'):  # Assuming namespace is raml20.xsd
        mo_class = mo.get('class')
        dist_name = mo.get('distName')
        id = mo.get('id')
        
        name = mo.find(".//{raml20.xsd}p[@name='name']").text
        old_dn = mo.find(".//{raml20.xsd}p[@name='oldDN']").text
        bts_name = mo.find(".//{raml20.xsd}p[@name='btsName']").text
        
        data.append({
            'Class': mo_class,
            'DistName': dist_name,
            'ID': id,
            'Name': name,
            'OldDN': old_dn,
            'BTSName': bts_name
        })
    
    return data

# Streamlit UI
def main():
    st.title("XML to Excel Converter")
    
    # File upload
    uploaded_file = st.file_uploader("Upload XML File", type=['xml'])
    
    if uploaded_file is not None:
        st.write("Parsing XML...")
        data = parse_xml(uploaded_file)
        
        # Display parsed data
        st.write("Parsed Data:")
        st.write(pd.DataFrame(data))
        
        # Save to Excel
        st.write("Saving to Excel...")
        df = pd.DataFrame(data)
        excel_file_path = "parsed_data.xlsx"
        df.to_excel(excel_file_path, index=False)
        
        st.write(f"Excel file saved: [Download Excel file](/{excel_file_path})")
    
if __name__ == "__main__":
    main()
