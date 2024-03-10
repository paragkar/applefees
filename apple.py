import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Set page layout to wide
st.set_page_config(layout="wide")

# Hide Streamlit default header and footer
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Function Today's Capabilities and terms
def f_r(r):
    return r * 0.3/12

# Function new capabilities and terms
# Adjusted to ensure it always returns an array
def f_r_d(r, d, third_party_store,rate):
    if third_party_store == 'Yes':
        return np.full_like(r, (d - 1) * 0.543/12)  # Return a constant array
    else:
        return ((d - 1) * 0.543 + r * rate)/12

# Safely compute the fee ratio to avoid division by zero
def safe_ratio(fee, revenue):
    return fee / revenue if revenue else 0

# Streamlit app initialization and configuration
st.title("Apple's Service Charge Analysis Tool")
st.write("This tool visualizes and compares Apple's current Monthly service charges against a proposed model under different download scenarios.")

# Sidebar: User inputs
d_value = st.sidebar.number_input('Enter the Monthly download value (in Millions):', min_value=0.0, value=2.0, step=0.5)
max_revenue = st.sidebar.number_input('Enter the Maximum Monthly Revenue (in Millions):', min_value=1.0, value=10.0, step=5.0)
app_store_small_business_program = st.sidebar.selectbox('App Store Small Business Program:', ['No', 'Yes'])
alternate_payment_processing = st.sidebar.selectbox('Alternate Payment Processing:', ['No', 'Yes'])
third_party_store = st.sidebar.selectbox('3rd Party Store:', ['No', 'Yes'])

st.sidebar.markdown("Equations used in the analysis:")
st.sidebar.markdown(r"$f(r) = 0.3 \times r$ (blue line)")

if app_store_small_business_program == 'Yes':
    rate = 0.15
else:
    rate = 0.2

if alternate_payment_processing == 'Yes':
    rate = rate - 0.03
else:
    pass

if third_party_store == 'Yes':
    st.sidebar.markdown(r"$f(r, d) = (d - 1) \times 0.543$ (red line, 3rd party store impact)")
else:
    st.sidebar.markdown(r"$f(r, d) = (d - 1) \times 0.543 + rate \times r$ (red line)")

# Set the range of Revenue values based on max revenue
r_values = np.linspace(0, max_revenue, 200)

# Initialize figure
fig = go.Figure()

# Calculate f(r) and f(r, d) values
f_r_values = f_r(r_values)
f_r_d_values = f_r_d(r_values, d_value, third_party_store, rate)

# Add f(r) trace in blue
fig.add_trace(go.Scatter(
    x=r_values, y=f_r_values, mode='lines+markers',
    name='Current Model (f(r))',
    line=dict(color='blue', dash='dot'),
    hoverinfo='text',
    text=[f"Revenue: ${r:.2f}M, Service Fee: ${f_r(r):.2f}M, Fee Ratio: {safe_ratio(f_r(r), r):.2%}" for r in r_values]
))

# Add f(r, d) trace considering 3rd party store impact in red
fig.add_trace(go.Scatter(
    x=r_values, y=f_r_d_values, mode='lines+markers',
    name=f'Proposed Model (f(r, d)) with downloads={d_value} Million/Month',
    line=dict(color='red'),
    hoverinfo='text',
    text=[f"Revenue: ${r:.2f}M, Service Fee: ${f_r_d(r, d_value, third_party_store, rate):.2f}M, Fee Ratio: {safe_ratio(f_r_d(r, d_value, third_party_store, rate), r):.2%}" for r in r_values]
))

# Check for intersection and update lines
for i in range(1, len(r_values)):
    if f_r_values[i-1] < f_r_d_values[i-1] and f_r_values[i] > f_r_d_values[i] or f_r_values[i-1] > f_r_d_values[i-1] and f_r_values[i] < f_r_d_values[i]:
        intersection_x = r_values[i]
        intersection_y = f_r(intersection_x)
        # Draw black lines from intersection to axes
        fig.add_shape(type="line", x0=intersection_x, y0=0, x1=intersection_x, y1=intersection_y, line=dict(color="Black", width=2))
        fig.add_shape(type="line", x0=0, y0=intersection_y, x1=intersection_x, y1=intersection_y, line=dict(color="Black", width=2))
        break

# Update layout with axis titles
fig.update_layout(
    height=700, 
    width=1200, 
    title_text="Apple's Current vs. Proposed Service Charges",
    xaxis_title="App Provider's Monthly Revenue ($ Million)",
    yaxis_title="Apple's Monthly Service Charges ($ Million)"
)

# Display the figure
st.plotly_chart(fig)
