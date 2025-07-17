def calculate_detailed_costs(optimal_sol, demand, production_cost, setup_cost, holding_cost):
    """Calculate detailed cost breakdown for the optimal solution"""
    results_data = []
    running_inventory = 0
    total_cost = 0
    
    for i, sol in enumerate(optimal_sol):
        month = i + 1
        order_qty = sol[1]
        demand_qty = demand[i]
        
        # Calculate inventory after ordering and before demand
        inventory_after_order = running_inventory + order_qty
        # Calculate inventory after demand
        inventory_after_demand = inventory_after_order - demand_qty
        
        # Calculate costs
        production_cost_month = production_cost * order_qty if order_qty > 0 else 0
        setup_cost_month = setup_cost if order_qty > 0 else 0
        holding_cost_month = holding_cost * inventory_after_demand if inventory_after_demand > 0 else 0
        month_total_cost = production_cost_month + setup_cost_month + holding_cost_month
        
        total_cost += month_total_cost
        
        results_data.append({
            'Month': month,
            'Demand': demand_qty,
            'Order Quantity': order_qty,
            'Inventory (Before Order)': running_inventory,
            'Inventory (After Order)': inventory_after_order,
            'Inventory (After Demand)': inventory_after_demand,
            'Monthly Cost': month_total_cost
        })
        
        running_inventory = inventory_after_demand
    
    return results_data, total_cost

def calculate_cost_breakdown(optimal_sol, demand, production_cost, setup_cost, holding_cost):
    """Calculate total cost breakdown"""
    total_production_cost = sum(production_cost * sol[1] for sol in optimal_sol)
    total_setup_cost = sum(setup_cost if sol[1] > 0 else 0 for sol in optimal_sol)
    
    # Calculate holding costs
    total_holding_cost = 0
    running_inventory = 0
    for i, sol in enumerate(optimal_sol):
        running_inventory = running_inventory + sol[1] - demand[i]
        if running_inventory > 0:
            total_holding_cost += holding_cost * running_inventory
    
    return {
        'production': total_production_cost,
        'setup': total_setup_cost,
        'holding': total_holding_cost,
        'total': total_production_cost + total_setup_cost + total_holding_cost
    }

def get_inventory_levels(optimal_sol, demand):
    """Calculate inventory levels over time"""
    inventory_levels = []
    running_inv = 0
    for i, sol in enumerate(optimal_sol):
        running_inv = running_inv + sol[1] - demand[i]
        inventory_levels.append(max(0, running_inv))
    return inventory_levels

def validate_inputs(n, demand, max_order, max_storage, production_cost, setup_cost, holding_cost):
    """Validate user inputs"""
    errors = []
    
    if n <= 0:
        errors.append("Number of months must be greater than 0")
    
    if not all(d > 0 for d in demand):
        errors.append("All demand values must be greater than 0")
    
    if max_order <= 0:
        errors.append("Maximum order capacity must be greater than 0")
    
    if max_storage <= 0:
        errors.append("Maximum storage capacity must be greater than 0")
    
    if production_cost <= 0:
        errors.append("Production cost must be greater than 0")
    
    if setup_cost <= 0:
        errors.append("Setup cost must be greater than 0")
    
    if holding_cost <= 0:
        errors.append("Holding cost must be greater than 0")
    
    return errors