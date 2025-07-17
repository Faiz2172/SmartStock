import streamlit as st
import pandas as pd

def render_sidebar_inputs():
    """Render sidebar input components"""
    st.sidebar.title("📝 Input Parameters")
    
    # Number of months
    n = st.sidebar.number_input("Number of Months", min_value=1, max_value=12, value=6)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Monthly Demand")
    
    # Demand inputs
    demand = []
    for i in range(n):
        demand_val = st.sidebar.number_input(f"Month {i+1} Demand", min_value=0, value=100, key=f"demand_{i}")
        demand.append(demand_val)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏭 Production Parameters")
    
    # Cost inputs
    production_cost = st.sidebar.number_input("Production Cost per Item", min_value=0.0, value=10.0, step=0.1)
    setup_cost = st.sidebar.number_input("Setup Cost", min_value=0.0, value=50.0, step=0.1)
    holding_cost = st.sidebar.number_input("Holding Cost per Item", min_value=0.0, value=2.0, step=0.1)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Constraints")
    
    # Constraint inputs
    max_order = st.sidebar.number_input("Maximum Order Capacity", min_value=1, value=500)
    max_storage = st.sidebar.number_input("Maximum Storage Capacity", min_value=1, value=300)
    
    return n, demand, production_cost, setup_cost, holding_cost, max_order, max_storage

def render_sidebar_summary(n, demand):
    """Render sidebar summary"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Current Settings")
    st.sidebar.write(f"**Months:** {n}")
    st.sidebar.write(f"**Total Demand:** {sum(demand)}")
    st.sidebar.write(f"**Avg Monthly Demand:** {sum(demand)/n:.1f}")

def render_header():
    """Render main header"""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">📦 Inventory Control System</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Dynamic Programming Optimization Solution</p>', unsafe_allow_html=True)

def render_results_table(results_df):
    """Render results table with formatting"""
    st.subheader("🎯 Optimal Ordering Schedule")
    st.dataframe(results_df, use_container_width=True)

def render_summary_metrics(total_cost, optimal_sol):
    """Render summary metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost", f"${total_cost:.2f}")
    with col2:
        st.metric("Total Orders", sum(1 for sol in optimal_sol if sol[1] > 0))
    with col3:
        st.metric("Total Quantity Ordered", sum(sol[1] for sol in optimal_sol))
    with col4:
        avg_order = sum(sol[1] for sol in optimal_sol) / max(1, sum(1 for sol in optimal_sol if sol[1] > 0))
        st.metric("Average Order Size", f"{avg_order:.1f}")

def render_cost_analysis_table(cost_breakdown):
    """Render cost analysis table"""
    cost_data = {
        'Cost Type': ['Production Cost', 'Setup Cost', 'Holding Cost', 'Total Cost'],
        'Amount': [
            cost_breakdown['production'],
            cost_breakdown['setup'],
            cost_breakdown['holding'],
            cost_breakdown['total']
        ],
        'Percentage': [
            (cost_breakdown['production'] / cost_breakdown['total']) * 100,
            (cost_breakdown['setup'] / cost_breakdown['total']) * 100,
            (cost_breakdown['holding'] / cost_breakdown['total']) * 100,
            100
        ]
    }
    cost_df = pd.DataFrame(cost_data)
    st.dataframe(cost_df, use_container_width=True)

def render_eoq_info(eoq, demand, production_cost, holding_cost):
    """Render EOQ information"""
    st.markdown("### EOQ Calculation")
    st.metric("EOQ Value", f"{eoq:.2f} units")
    
    st.markdown("### EOQ Formula Components:")
    st.write(f"**Total Demand:** {sum(demand)} units")
    st.write(f"**Production Cost:** ${production_cost}")
    st.write(f"**Holding Cost:** ${holding_cost}")
    
    st.markdown("### EOQ Formula:")
    st.latex(r"EOQ = \sqrt{\frac{2 \times D \times S}{H}}")
    st.write("Where:")
    st.write("- D = Total Demand")
    st.write("- S = Production Cost per unit")
    st.write("- H = Holding Cost per unit")

def render_eoq_comparison(eoq, optimal_sol):
    """Render EOQ comparison analysis"""
    actual_orders = [sol[1] for sol in optimal_sol if sol[1] > 0]
    if actual_orders:
        avg_order_size = sum(actual_orders) / len(actual_orders)
        
        comparison_data = {
            'Metric': ['EOQ', 'Average Actual Order', 'Difference'],
            'Value': [eoq, avg_order_size, abs(eoq - avg_order_size)],
            'Status': [
                'Theoretical Optimal',
                'Constraint-Adjusted',
                'Deviation'
            ]
        }
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        if abs(eoq - avg_order_size) / eoq > 0.2:
            st.warning("⚠️ Actual orders deviate significantly from EOQ due to constraints")
        else:
            st.success("✅ Actual orders are close to EOQ optimal")