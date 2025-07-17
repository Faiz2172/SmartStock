import plotly.graph_objects as go
import plotly.express as px

def create_demand_vs_order_chart(months, demand, order_quantities):
    """Create demand vs order quantity bar chart"""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=demand, name='Demand', marker_color='lightblue'))
    fig.add_trace(go.Bar(x=months, y=order_quantities, name='Order Quantity', marker_color='darkblue'))
    fig.update_layout(
        title='Monthly Demand vs Order Quantity',
        xaxis_title='Month',
        yaxis_title='Quantity',
        barmode='group'
    )
    return fig

def create_inventory_levels_chart(months, inventory_levels):
    """Create inventory levels over time line chart"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, 
        y=inventory_levels, 
        mode='lines+markers',
        name='Inventory Level', 
        line=dict(color='green', width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title='Inventory Levels Over Time',
        xaxis_title='Month',
        yaxis_title='Inventory Units'
    )
    return fig

def create_cost_breakdown_chart(months, optimal_sol, production_cost, setup_cost):
    """Create monthly cost breakdown stacked bar chart"""
    production_costs = [production_cost * sol[1] if sol[1] > 0 else 0 for sol in optimal_sol]
    setup_costs = [setup_cost if sol[1] > 0 else 0 for sol in optimal_sol]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=production_costs, name='Production Cost', marker_color='red'))
    fig.add_trace(go.Bar(x=months, y=setup_costs, name='Setup Cost', marker_color='orange'))
    fig.update_layout(
        title='Monthly Cost Breakdown',
        xaxis_title='Month',
        yaxis_title='Cost ($)',
        barmode='stack'
    )
    return fig

def create_cost_distribution_pie(cost_breakdown):
    """Create cost distribution pie chart"""
    labels = ['Production Cost', 'Setup Cost', 'Holding Cost']
    values = [cost_breakdown['production'], cost_breakdown['setup'], cost_breakdown['holding']]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title='Cost Distribution')
    return fig

def create_eoq_comparison_chart(eoq, actual_orders):
    """Create EOQ vs actual orders comparison"""
    if actual_orders:
        avg_order_size = sum(actual_orders) / len(actual_orders)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['EOQ', 'Average Actual Order'],
            y=[eoq, avg_order_size],
            marker_color=['blue', 'orange']
        ))
        fig.update_layout(
            title='EOQ vs Actual Orders Comparison',
            yaxis_title='Order Quantity'
        )
        return fig
    return None