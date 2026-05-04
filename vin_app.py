import streamlit as st
import requests

def get_vin_data(vin):
    # NHTSA Public API for technical vehicle data
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['Results'][0]
            return data
        else:
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return None

# --- UI Setup ---
st.set_page_config(page_title="Vehicle Intelligence Tool", page_icon="🚗")
st.title("🚗 Vehicle Information Lookup")
st.markdown("Enter a 17-character VIN to retrieve technical specifications.")

vin_input = st.text_input("Enter VIN Number:", placeholder="e.g. 1G1YY26U...").upper()

if st.button("Decode Vehicle Information"):
    if len(vin_input) != 17:
        st.warning("Please enter a valid 17-character VIN.")
    else:
        with st.spinner('Fetching data...'):
            vehicle_info = get_vin_data(vin_input)
            
            if vehicle_info:
                # Basic Check: If the API returns an empty make, the VIN is likely invalid
                if not vehicle_info.get('Make'):
                    st.error("Could not find data for this VIN. Please check the number and try again.")
                else:
                    st.success("Vehicle Found!")
                    
                    # Displaying Technical Data
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Make", vehicle_info.get('Make'))
                        st.metric("Model", vehicle_info.get('Model'))
                        st.write(f"**Year:** {vehicle_info.get('ModelYear')}")
                        st.write(f"**Body Class:** {vehicle_info.get('BodyClass')}")

                    with col2:
                        st.write(f"**Engine:** {vehicle_info.get('DisplacementL')}L {vehicle_info.get('EngineConfiguration')}")
                        st.write(f"**Fuel Type:** {vehicle_info.get('FuelTypePrimary')}")
                        st.write(f"**Drive Type:** {vehicle_info.get('DriveType')}")
                        st.write(f"**Plant Country:** {vehicle_info.get('PlantCountry')}")

                    # --- Owner Information Section ---
                    st.divider()
                    st.subheader("👤 Ownership & Registration Details")
                    st.info("""
                        **Note on Privacy:** Owner information is not publicly accessible via open APIs due to data protection acts (POPIA/GDPR). 
                        To access registered owner names, this app would require integration with a restricted 
                        Government/Insurance database API.
                    """)
            else:
                st.error("Unable to retrieve data.")

