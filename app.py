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
st.markdown("Calculate temperature-corrected resistance and tolerance deviations for copper winding wire.")

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Test Measurements")
    # Updated value and expanded format to 7 decimal places to accommodate 0.0012345
    measured_r = st.number_input("Measured Resistance (Ω)", min_value=0.0000000, value=0.0012345, step=0.0000100, format="%.7f")
    
    # Updated temperature constraints, default value, and step
    measured_temp = st.number_input("Coil Temperature (°C)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)

with col2:
    st.subheader("Design Specs")
    # Updated to 7 decimal places to match the measurement precision
    nominal_r = st.number_input("Nominal R20 (Ω)", min_value=0.0000000, value=15.0000000, step=0.0000100, format="%.7f")
    tolerance = st.number_input("Tolerance Limit (±%)", min_value=0.0, value=3.5, step=0.1)

# --- Calculation & Output Section ---
if st.button("Calculate R20", type="primary"):
    r20, deviation = calculate_copper_r20(measured_r, measured_temp, nominal_r)
    
    st.divider()
    st.subheader("Test Results")
    
    # Display results using Streamlit metrics
    res_col, dev_col = st.columns(2)
    
    # Output adjusted to 7 decimal places for the resistance
    res_col.metric(label="Calculated R20", value=f"{r20:.7f} Ω")
    
    # Configure delta display (red if out of tolerance, green if close to 0)
    if abs(deviation) <= tolerance:
        dev_col.metric(label="Deviation", value=f"{deviation:.5f} %", delta="Pass", delta_color="normal")
        st.success(f"✅ **PASS**: The coil deviation ({deviation:.5f}%) is within the ±{tolerance}% limit.")
    else:
        dev_col.metric(label="Deviation", value=f"{deviation:.5f} %", delta="Fail", delta_color="inverse")
        st.error(f"❌ **FAIL**: The coil deviation ({deviation:.5f}%) exceeds the ±{tolerance}% limit.")

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
