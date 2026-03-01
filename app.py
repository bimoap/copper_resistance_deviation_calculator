import streamlit as st

def calculate_copper_r20(measured_r, measured_temp, nominal_r):
    """Calculates R20 and deviation for standard copper (constant = 234.5)."""
    copper_constant = 234.5
    r_20 = measured_r * ((copper_constant + 20.0) / (copper_constant + measured_temp))
    
    if nominal_r > 0:
        deviation = ((r_20 - nominal_r) / nominal_r) * 100.0
    else:
        deviation = 0.0
        
    return r_20, deviation

# --- UI Configuration ---
st.set_page_config(page_title="Coil QA Calculator", layout="centered")

st.title("Copper Coil R20 Calculator")
st.markdown("Calculate temperature-corrected resistance and tolerance deviations for copper conductors.")

# --- Conductor Selection ---
conductor_type = st.selectbox(
    "Select Conductor Type",
    ("Hollow or strip copper conductor", "Copper wire conductor")
)

# Set the default lower and upper tolerances based on the selection
if conductor_type == "Hollow or strip copper conductor":
    default_lower = -3.5
    default_upper = 3.5
else:
    default_lower = -3.0
    default_upper = 3.5

st.divider()

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Test Measurements")
    measured_r = st.number_input("Measured Resistance (Ω)", min_value=0.0000000, value=0.0012345, step=0.0000100, format="%.7f")
    measured_temp = st.number_input("Coil Temperature (°C)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)

with col2:
    st.subheader("Design Specs")
    nominal_r = st.number_input("Nominal R20 (Ω)", min_value=0.0000000, value=0.0012356, step=0.0000100, format="%.7f")
    
    # Split tolerance into lower and upper limits to handle asymmetrical ranges
    lower_tolerance = st.number_input("Lower Limit (%)", value=default_lower, step=0.1)
    upper_tolerance = st.number_input("Upper Limit (%)", value=default_upper, step=0.1)

# --- Calculation & Output Section ---
if st.button("Calculate R20", type="primary"):
    r20, deviation = calculate_copper_r20(measured_r, measured_temp, nominal_r)
    
    st.divider()
    st.subheader("Test Results")
    
    # Display results using Streamlit metrics
    res_col, dev_col = st.columns(2)
    
    res_col.metric(label="Calculated R20", value=f"{r20:.7f} Ω")
    
    # Configure delta display and check against the specific lower and upper limits
    if lower_tolerance <= deviation <= upper_tolerance:
        dev_col.metric(label="Deviation", value=f"{deviation:.5f} %", delta="Pass", delta_color="normal")
        st.success(f"✅ **PASS**: The coil deviation ({deviation:.5f}%) is within the {lower_tolerance}% to +{upper_tolerance}% limit for a {conductor_type.lower()}.")
    else:
        dev_col.metric(label="Deviation", value=f"{deviation:.5f} %", delta="Fail", delta_color="inverse")
        st.error(f"❌ **FAIL**: The coil deviation ({deviation:.5f}%) is outside the {lower_tolerance}% to +{upper_tolerance}% limit for a {conductor_type.lower()}.")

# --- Signature Section ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: right; color: gray; font-size: 0.9em; line-height: 1.4;'>
        <i>App developed & maintained by:</i><br>
        <b>Bimo Adhi Prastya</b><br>
        Coil Shop Technician
    </div>
    """, 
    unsafe_allow_html=True
)
