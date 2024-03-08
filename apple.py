import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Function definitions
def f_r(r):
    return r * 0.3

def f_r_d(r, d):
    return (d - 1) * 0.543 + r * 0.2

# Set the range of Revenue values
r_values = np.linspace(0, 1000, 100)

# Streamlit app
st.title("Apple's Service Charge Analysis Tool")
st.write("This tool allows you to compare Apple's current yearly service charges against a proposed model under different download scenarios.")

# User input for d value
d_value = st.number_input('Enter the yearly download value (in millions):', min_value=1.0, value=100.0, step=1.0)

# Initialize figure
fig = go.Figure()

# Add trace for f(r) with a dotted line
fig.add_trace(go.Scatter(x=r_values, y=f_r(r_values), mode='lines', name='Current Model (f(r))', line=dict(dash='dot')))

# Add traces for f(r, d) using the user-provided d value
fig.add_trace(go.Scatter(x=r_values, y=f_r_d(r_values, d_value), mode='lines', name=f'Proposed Model (f(r, d)) with downloads={d_value} Million/Year'))

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