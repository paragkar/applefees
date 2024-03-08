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
st.write("This tool visualizes and compares Apple's current yearly service charges against a proposed model under different download scenarios. The tooltips provide dynamic insights into the service fee ratio at each revenue point. If an intersection exists, black lines from that point to the axes are drawn.")

# User input for d value
d_value = st.number_input('Enter the yearly download value (in millions):', min_value=1.0, value=100.0, step=1.0)

# Initialize figure
fig = go.Figure()

# Generate service fee data
f_r_values = f_r(r_values)
f_r_d_values = [f_r_d(r, d_value) for r in r_values]

# Add trace for f(r) with custom hover information
fig.add_trace(go.Scatter(x=r_values, y=f_r_values, mode='lines+markers',
                         name='Current Model (f(r))',
                         line=dict(dash='dot'),
                         hoverinfo='text',
                         text=[f"Revenue: ${r:.2f}M, Service Fee: ${fee:.2f}M, Fee Ratio: {fee/r:.2%}" for r, fee in zip(r_values, f_r_values)]))

# Add traces for f(r, d) using the user-provided d value with custom hover information
fig.add_trace(go.Scatter(x=r_values, y=f_r_d_values, mode='lines+markers',
                         name=f'Proposed Model (f(r, d)) with downloads={d_value} Million/Year',
                         hoverinfo='text',
                         text=[f"Revenue: ${r:.2f}M, Service Fee: ${fee:.2f}M, Fee Ratio: {fee/r:.2%}" for r, fee in zip(r_values, f_r_d_values)]))

# Check for intersection point - only draw lines if intersection exists
for r, fee_r, fee_r_d in zip(r_values, f_r_values, f_r_d_values):
    if np.isclose(fee_r, fee_r_d, atol=0.01):
        intersection_x = r
        intersection_y = fee_r
        # Draw black lines from the intersection
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
