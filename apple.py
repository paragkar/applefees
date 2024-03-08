import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Function definitions
def f_r(r):
    return r * 0.3

def f_r_d(r, d):
    return (d - 1) * 0.543 + r * 0.2

# Find the intersection point
def find_intersection(d_value):
    r_values = np.linspace(0, 1000, 10000)  # Increase resolution to find a more accurate intersection
    for r in r_values:
        if np.isclose(f_r(r), f_r_d(r, d_value), atol=0.01):  # Adjust atol for precision
            return r, f_r(r)
    return None, None

# Streamlit app
st.title("Apple's Service Charge Analysis Tool")
st.write("This tool visualizes and compares Apple's current yearly service charges against a proposed model under different download scenarios. Lines from the intersection point to the axes are included.")

# User input for d value
d_value = st.number_input('Enter the yearly download value (in millions):', min_value=1.0, value=100.0, step=1.0)

# Initialize figure
fig = go.Figure()

# Calculate intersection and add traces
intersection_r, intersection_fee = find_intersection(d_value)

# Add trace for f(r) with custom hover information
fig.add_trace(go.Scatter(x=[0, 1000], y=f_r(np.array([0, 1000])), mode='lines',
                         name='Current Model (f(r))', line=dict(dash='dot')))

# Add traces for f(r, d) with custom hover information
fig.add_trace(go.Scatter(x=[0, 1000], y=f_r_d(np.array([0, 1000]), d_value), mode='lines',
                         name=f'Proposed Model (f(r, d)) with downloads={d_value} Million/Year'))

if intersection_r is not None and intersection_fee is not None:
    # Mark the intersection point
    fig.add_trace(go.Scatter(x=[intersection_r], y=[intersection_fee], mode='markers', name='Intersection Point'))
    
    # Draw lines to the axes from the intersection point
    fig.add_shape(type="line", x0=intersection_r, y0=0, x1=intersection_r, y1=intersection_fee,
                  line=dict(color="RoyalBlue", width=2, dash="dot"))
    fig.add_shape(type="line", x0=0, y0=intersection_fee, x1=intersection_r, y1=intersection_fee,
                  line=dict(color="RoyalBlue", width=2, dash="dot"))

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
