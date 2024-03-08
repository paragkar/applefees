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

# Function definitions
def f_r(r):
    return r * 0.3

def f_r_d(r, d):
    return (d - 1) * 0.543 + r * 0.2

# Safely compute the fee ratio to avoid division by zero
def safe_ratio(fee, revenue):
    return fee / revenue if revenue else 0

# Streamlit app initialization and configuration
st.title("Apple's Service Charge Analysis Tool")
st.write("This tool visualizes and compares Apple's current yearly service charges against a proposed model under different download scenarios. The tooltips provide dynamic insights into the service fee ratio at each revenue point.")

# Sidebar: User input for d value and display equations
d_value = st.sidebar.number_input('Enter the yearly download value (in millions):', min_value=0.0, value=100.0, step=1.0)
st.sidebar.write("Equations used in the analysis:")
st.sidebar.latex(r"f(r) = 0.3 \times r")
st.sidebar.latex(r"f(r, d) = (d - 1) \times 0.543 + 0.2 \times r")

# Set the range of Revenue values
r_values = np.linspace(0, 1000, 1000)

# Initialize figure
fig = go.Figure()

# Calculate and add traces for f(r) and f(r, d) with custom hover information
f_r_values = f_r(r_values)
f_r_d_values = f_r_d(r_values, d_value)

# Add f(r) trace
fig.add_trace(go.Scatter(
    x=r_values, y=f_r_values, mode='lines+markers',
    name='Current Model (f(r))',
    line=dict(dash='dot'),
    hoverinfo='text',
    text=[f"Revenue: ${r:.2f}M, Service Fee: ${f_r(r):.2f}M, Fee Ratio: {safe_ratio(f_r(r), r):.2%}" for r in r_values]
))

# Add f(r, d) trace
fig.add_trace(go.Scatter(
    x=r_values, y=f_r_d_values, mode='lines+markers',
    name=f'Proposed Model (f(r, d)) with downloads={d_value} Million/Year',
    hoverinfo='text',
    text=[f"Revenue: ${r:.2f}M, Service Fee: ${f_r_d(r, d_value):.2f}M, Fee Ratio: {safe_ratio(f_r_d(r, d_value), r):.2%}" for r in r_values]
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
    title_text="Apple's Current vs. Proposed Yearly Service Charges",
    xaxis_title="App Provider's Yearly Revenue ($ Million)",
    yaxis_title="Apple's Yearly Service Charges ($ Million)"
)

# Display the figure
st.plotly_chart(fig)
