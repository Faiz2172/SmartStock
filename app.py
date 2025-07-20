import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Import your backend classes (keep original logic intact)
from inventory_optimizer import InventoryOptimizer, EOQCalculator
from utils import *

def main():
    st.set_page_config(
        page_title="SmartStock",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for modern styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .cost-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .input-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📦 Inventory Control System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Dynamic Programming Optimization for Supply Chain Management</p>', unsafe_allow_html=True)
    
    # Input Section
    render_input_section()

def render_input_section():
    """Render the main input section"""
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 📊 Configure Your Inventory Parameters")
    
    # Basic Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Planning Period")
        n = st.number_input("Number of Months", min_value=1, max_value=12, value=6, help="Planning horizon in months")
    
    with col2:
        st.markdown("#### 🏭 Production Costs")
        production_cost = st.number_input("Production Cost per Item ($)", min_value=0.0, value=10.0, step=0.1)
        setup_cost = st.number_input("Setup Cost per Order ($)", min_value=0.0, value=50.0, step=0.1)
        holding_cost = st.number_input("Holding Cost per Item ($)", min_value=0.0, value=2.0, step=0.1)
    
    # Constraints
    st.markdown("#### ⚙️ Operational Constraints")
    col3, col4 = st.columns(2)
    
    with col3:
        max_order = st.number_input("Maximum Order Capacity", min_value=1, value=500, help="Maximum units that can be ordered at once")
    
    with col4:
        max_storage = st.number_input("Maximum Storage Capacity", min_value=1, value=300, help="Maximum units that can be stored")
    
    # Demand Input Section
    st.markdown("#### 📈 Monthly Demand Forecast")
    
    # Create demand input method selection
    input_method = st.radio("Choose input method:", ["Manual Entry", "Quick Patterns"], horizontal=True)
    
    if input_method == "Manual Entry":
        demand = render_manual_demand_input(n)
    else:
        demand = render_pattern_demand_input(n)
    
    # Display demand summary
    if demand:
        render_demand_summary(demand)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate button
    if st.button("🚀 Calculate Optimal Solution", type="primary"):
        if demand and all(d > 0 for d in demand):
            calculate_and_display_results(n, demand, max_order, max_storage, 
                                        production_cost, setup_cost, holding_cost)
        else:
            st.error("Please ensure all demand values are greater than 0")

def render_manual_demand_input(n):
    """Render manual demand input with improved layout"""
    demand = []
    
    # Create columns for demand inputs
    cols = st.columns(min(n, 4))  # Max 4 columns per row
    
    for i in range(n):
        col_idx = i % 4
        with cols[col_idx]:
            demand_val = st.number_input(f"Month {i+1}", min_value=0, value=100, key=f"demand_{i}")
            demand.append(demand_val)
    
    return demand

def render_pattern_demand_input(n):
    """Render pattern-based demand input"""
    pattern_type = st.selectbox("Select demand pattern:", 
                               ["Constant", "Increasing", "Decreasing", "Seasonal", "Random"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        base_demand = st.number_input("Base Demand", min_value=1, value=100)
    
    with col2:
        if pattern_type in ["Increasing", "Decreasing"]:
            variation = st.number_input("Monthly Change", min_value=0, value=10)
        elif pattern_type == "Seasonal":
            amplitude = st.number_input("Seasonal Amplitude", min_value=0, value=30)
        elif pattern_type == "Random":
            max_variation = st.number_input("Max Variation (%)", min_value=0, value=20)
    
    # Generate demand based on pattern
    demand = []
    for i in range(n):
        if pattern_type == "Constant":
            demand.append(base_demand)
        elif pattern_type == "Increasing":
            demand.append(base_demand + i * variation)
        elif pattern_type == "Decreasing":
            demand.append(max(1, base_demand - i * variation))
        elif pattern_type == "Seasonal":
            seasonal_factor = amplitude * np.sin(2 * np.pi * i / 12)
            demand.append(int(base_demand + seasonal_factor))
        elif pattern_type == "Random":
            variation_factor = np.random.uniform(-max_variation/100, max_variation/100)
            demand.append(int(base_demand * (1 + variation_factor)))
    
    return demand

def render_demand_summary(demand):
    """Render demand summary with visualization"""
    st.markdown("#### 📊 Demand Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Demand", f"{sum(demand)}")
    with col2:
        st.metric("Average", f"{np.mean(demand):.1f}")
    with col3:
        st.metric("Min Demand", f"{min(demand)}")
    with col4:
        st.metric("Max Demand", f"{max(demand)}")
    
    # Quick demand visualization
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f"Month {i+1}" for i in range(len(demand))],
        y=demand,
        marker_color='lightblue',
        text=demand,
        textposition='auto'
    ))
    fig.update_layout(
        title="Monthly Demand Forecast",
        xaxis_title="Month",
        yaxis_title="Demand",
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def calculate_and_display_results(n, demand, max_order, max_storage, production_cost, setup_cost, holding_cost):
    """Calculate and display results using your original backend logic"""
    
    # Validate inputs
    errors = validate_inputs(n, demand, max_order, max_storage, production_cost, setup_cost, holding_cost)
    
    if errors:
        for error in errors:
            st.error(error)
        return
    
    # Use your original backend logic
    inventory_optimizer = InventoryOptimizer()
    eoq_calculator = EOQCalculator(n, demand, production_cost, setup_cost, holding_cost)
    
    # Calculate optimal solution
    optimal_order = inventory_optimizer.calculate_min_cost(n, demand, max_order, max_storage, 
                                                         production_cost, setup_cost, holding_cost)
    optimal_sol = inventory_optimizer.calculate_optimal_sol(n, optimal_order, demand)
    eoq = eoq_calculator.calculate_eoq()
    
    # Display results
    display_enhanced_results(n, optimal_sol, demand, eoq, production_cost, setup_cost, holding_cost)

def display_enhanced_results(n, optimal_sol, demand, eoq, production_cost, setup_cost, holding_cost):
    """Enhanced results display with modern UI"""
    
    # Calculate data using your utility functions
    results_data, total_cost = calculate_detailed_costs(optimal_sol, demand, production_cost, setup_cost, holding_cost)
    cost_breakdown = calculate_cost_breakdown(optimal_sol, demand, production_cost, setup_cost, holding_cost)
    
    # Success message
    st.success("✅ Optimization Complete!")
    
    # Key Metrics Dashboard
    st.markdown("### 📊 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>${total_cost:.2f}</h3>
            <p>Total Cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_orders = sum(1 for sol in optimal_sol if sol[1] > 0)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_orders}</h3>
            <p>Total Orders</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_quantity = sum(sol[1] for sol in optimal_sol)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_quantity}</h3>
            <p>Total Quantity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_order = total_quantity / max(1, total_orders)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{avg_order:.1f}</h3>
            <p>Avg Order Size</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cost Breakdown Cards
    st.markdown("### 💰 Cost Breakdown")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="cost-card">
            <h3>${cost_breakdown['production']:.2f}</h3>
            <p>Production Cost ({(cost_breakdown['production']/total_cost*100):.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="cost-card">
            <h3>${cost_breakdown['setup']:.2f}</h3>
            <p>Setup Cost ({(cost_breakdown['setup']/total_cost*100):.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="cost-card">
            <h3>${cost_breakdown['holding']:.2f}</h3>
            <p>Holding Cost ({(cost_breakdown['holding']/total_cost*100):.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabbed Results
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Optimal Schedule", "📈 Analytics Dashboard", "🧮 Detailed Analysis", "📖 EOQ Comparison"])
    
    with tab1:
        render_optimal_schedule(results_data)
    
    with tab2:
        render_analytics_dashboard(n, optimal_sol, demand, cost_breakdown, total_cost)
    
    with tab3:
        render_detailed_analysis(results_data, cost_breakdown)
    
    with tab4:
        render_eoq_analysis(eoq, optimal_sol, demand, production_cost, holding_cost)

def render_optimal_schedule(results_data):
    """Render optimal scheduling results"""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Optimal Ordering Schedule")
    
    # Format the results dataframe
    results_df = pd.DataFrame(results_data)
    
    # Style the dataframe
    styled_df = results_df.style.format({
        'Monthly Cost': '${:.2f}',
        'Order Quantity': '{:.0f}',
        'Demand': '{:.0f}',
        'Inventory (Before Order)': '{:.0f}',
        'Inventory (After Order)': '{:.0f}',
        'Inventory (After Demand)': '{:.0f}'
    }).background_gradient(subset=['Monthly Cost'], cmap='RdYlBu_r')
    
    st.dataframe(styled_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics_dashboard(n, optimal_sol, demand, cost_breakdown, total_cost):
    """Render comprehensive analytics dashboard"""
    st.markdown("#### 📈 Analytics Dashboard")
    
    months = list(range(1, n + 1))
    order_quantities = [sol[1] for sol in optimal_sol]
    inventory_levels = get_inventory_levels(optimal_sol, demand)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Demand vs Orders', 'Inventory Levels', 'Monthly Costs', 'Cost Distribution'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "pie"}]]
    )
    
    # Demand vs Orders
    fig.add_trace(go.Bar(x=months, y=demand, name='Demand', marker_color='lightblue'), row=1, col=1)
    fig.add_trace(go.Bar(x=months, y=order_quantities, name='Orders', marker_color='darkblue'), row=1, col=1)
    
    # Inventory Levels
    fig.add_trace(go.Scatter(x=months, y=inventory_levels, mode='lines+markers', 
                            name='Inventory', line=dict(color='green', width=3)), row=1, col=2)
    
    # Monthly Costs
    production_costs = [10 * sol[1] if sol[1] > 0 else 0 for sol in optimal_sol]  # Using default for visualization
    setup_costs = [50 if sol[1] > 0 else 0 for sol in optimal_sol]
    
    fig.add_trace(go.Bar(x=months, y=production_costs, name='Production', marker_color='red'), row=2, col=1)
    fig.add_trace(go.Bar(x=months, y=setup_costs, name='Setup', marker_color='orange'), row=2, col=1)
    
    # Cost Distribution Pie
    fig.add_trace(go.Pie(labels=['Production', 'Setup', 'Holding'], 
                        values=[cost_breakdown['production'], cost_breakdown['setup'], cost_breakdown['holding']],
                        name="Cost Distribution"), row=2, col=2)
    
    fig.update_layout(height=800, showlegend=True, title_text="Comprehensive Analytics Dashboard")
    st.plotly_chart(fig, use_container_width=True)

def render_detailed_analysis(results_data, cost_breakdown):
    """Render detailed cost analysis"""
    st.markdown("#### 🧮 Detailed Cost Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Monthly Cost Details**")
        monthly_df = pd.DataFrame(results_data)[['Month', 'Monthly Cost']].copy()
        monthly_df['Cumulative Cost'] = monthly_df['Monthly Cost'].cumsum()
        st.dataframe(monthly_df.style.format({'Monthly Cost': '${:.2f}', 'Cumulative Cost': '${:.2f}'}))
    
    with col2:
        st.markdown("**Cost Category Analysis**")
        cost_analysis_df = pd.DataFrame({
            'Cost Type': ['Production', 'Setup', 'Holding', 'Total'],
            'Amount': [cost_breakdown['production'], cost_breakdown['setup'], 
                      cost_breakdown['holding'], cost_breakdown['total']],
            'Percentage': [
                f"{(cost_breakdown['production']/cost_breakdown['total']*100):.1f}%",
                f"{(cost_breakdown['setup']/cost_breakdown['total']*100):.1f}%",
                f"{(cost_breakdown['holding']/cost_breakdown['total']*100):.1f}%",
                "100.0%"
            ]
        })
        st.dataframe(cost_analysis_df.style.format({'Amount': '${:.2f}'}))

def render_eoq_analysis(eoq, optimal_sol, demand, production_cost, holding_cost):
    """Render EOQ analysis and comparison"""
    st.markdown("#### 📖 Economic Order Quantity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**EOQ Calculation**")
        st.metric("EOQ Value", f"{eoq:.2f} units")
        
        st.markdown("**Formula Components:**")
        st.write(f"• Total Demand: {sum(demand)} units")
        st.write(f"• Production Cost: ${production_cost}")
        st.write(f"• Holding Cost: ${holding_cost}")
        
        st.latex(r"EOQ = \sqrt{\frac{2 \times D \times S}{H}}")
    
    with col2:
        st.markdown("**EOQ vs Actual Comparison**")
        
        actual_orders = [sol[1] for sol in optimal_sol if sol[1] > 0]
        if actual_orders:
            avg_actual = sum(actual_orders) / len(actual_orders)
            
            comparison_data = {
                'Metric': ['EOQ (Theoretical)', 'Average Actual Order', 'Deviation'],
                'Value': [f"{eoq:.2f}", f"{avg_actual:.2f}", f"{abs(eoq-avg_actual):.2f}"],
                'Status': ['Optimal', 'Constraint-Adjusted', 'Difference']
            }
            
            st.dataframe(pd.DataFrame(comparison_data))
            
            # EOQ Comparison Chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['EOQ', 'Average Actual'],
                y=[eoq, avg_actual],
                marker_color=['blue', 'orange'],
                text=[f"{eoq:.1f}", f"{avg_actual:.1f}"],
                textposition='auto'
            ))
            fig.update_layout(title="EOQ vs Actual Orders", height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Analysis
            deviation_pct = abs(eoq - avg_actual) / eoq * 100
            if deviation_pct > 20:
                st.warning(f"⚠️ Actual orders deviate {deviation_pct:.1f}% from EOQ due to constraints")
            else:
                st.success(f"✅ Actual orders are within {deviation_pct:.1f}% of EOQ optimal")

if __name__ == "__main__":
    main()