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
    measured_r = st.number_input("Measured Resistance (Ω)", min_value=0.000, value=15.500, step=0.010, format="%.3f")
    measured_temp = st.number_input("Coil Temperature (°C)", min_value=-50.0, max_value=200.0, value=25.0, step=0.5)

with col2:
    st.subheader("Design Specs")
    nominal_r = st.number_input("Nominal R20 (Ω)", min_value=0.000, value=15.000, step=0.010, format="%.3f")
    tolerance = st.number_input("Tolerance Limit (±%)", min_value=0.0, value=5.0, step=0.5)

# --- Calculation & Output Section ---
if st.button("Calculate R20", type="primary"):
    r20, deviation = calculate_copper_r20(measured_r, measured_temp, nominal_r)
    
    st.divider()
    st.subheader("Test Results")
    
    # Display results using Streamlit metrics
    res_col, dev_col = st.columns(2)
    
    res_col.metric(label="Calculated R20", value=f"{r20:.4f} Ω")
    
    # Configure delta display (red if out of tolerance, green if close to 0)
    if abs(deviation) <= tolerance:
        dev_col.metric(label="Deviation", value=f"{deviation:.2f} %", delta="Pass", delta_color="normal")
        st.success(f"✅ **PASS**: The coil deviation ({deviation:.2f}%) is within the ±{tolerance}% limit.")
    else:
        dev_col.metric(label="Deviation", value=f"{deviation:.2f} %", delta="Fail", delta_color="inverse")
        st.error(f"❌ **FAIL**: The coil deviation ({deviation:.2f}%) exceeds the ±{tolerance}% limit.")

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
