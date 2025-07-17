class EOQCalculator:
    def __init__(self, n, demand, production_cost, setup_cost, holding_cost):
        self.n = n
        self.demand = demand
        self.production_cost = production_cost
        self.setup_cost = setup_cost
        self.holding_cost = holding_cost
   
    def calculate_eoq(self):
        total_demand = sum(self.demand)
        return (2 * total_demand * self.production_cost / self.holding_cost) ** 0.5


class InventoryOptimizer:
    def calculate_min_cost(self, n, demand, max_order, max_storage, production_cost, setup_cost, holding_cost):
        min_cost = [[0] * (max_storage + 4) for _ in range(n + 1)]
        optimal_order = [[0] * (max_order + 4) for _ in range(n + 1)]
        a = [[[0] * (max_order + 4) for _ in range(max_storage + 4)] for _ in range(n + 1)]
       
        # Fix: Prevent IndexError by bounding i to max_storage + 4
        for i in range(min(demand[n - 1] + 1, max_storage + 4)):
            ordered = demand[n - 1] - i
            if ordered > 0:
                min_cost[n - 1][i] = production_cost * ordered + setup_cost
            else:
                min_cost[n - 1][i] = 0
            optimal_order[n-1][i] = ordered
       
        for t in range(n - 2, -1, -1):
            for i in range(max_storage + 1):
                ba = float('inf')
                for j in range(max_order + 1):
                    if t == 0 and i > 0:
                        break
                    if i + j < demand[t]:
                        temp = demand[t]
                    else:
                        temp = j

                    ordered = temp
                    total_holding = holding_cost * (i + ordered - demand[t])
                    if total_holding > max_storage:
                        break

                    if ordered > 0:
                        a[t][i][j] = production_cost * ordered + total_holding + setup_cost
                    else:
                        a[t][i][j] = total_holding

                    next_inventory = i + ordered - demand[t]
                    total_min = a[t][i][j] + min_cost[t + 1][next_inventory]
                    if total_min < ba:
                        ba = total_min
                        optimal_order[t][i] = temp
                min_cost[t][i] = ba
        return optimal_order
   
    def calculate_optimal_sol(self, n, optimal_order, demand):
        optimal_sol = []
        next_inventory1 = 0
        optimal_sol.append(["for month 1; order=", optimal_order[0][0]])
       
        for t in range(1, n):
            if optimal_order[t - 1][next_inventory1] > demand[t - 1]:
                l = optimal_order[t - 1][next_inventory1] - demand[t - 1]
            else:
                l = demand[t - 1] - optimal_order[t - 1][next_inventory1]

            optimal_sol.append(["for month {}; order=".format(t + 1), optimal_order[t][l]])
            if optimal_order[t][l] == 0:
                next_inventory1 = 0
            else:
                next_inventory1 = l
        return optimal_sol
