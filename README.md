# SmartStock 📈: Inventory Optimization System

SmartStock is a **Multi-Period Inventory Optimization System** developed in Python. It leverages **Dynamic Programming (DP)** to help businesses minimize the total cost of inventory planning over several months. The system determines the optimal number of units to produce each month while strictly meeting demand and adhering to production and storage limits.

-----
https://github.com/user-attachments/assets/4bbac803-9184-4b83-857e-e2d4bf6649ff
----

## 📌 Problem Statement

In inventory management, balancing supply and demand efficiently is crucial. We address this by considering:

  * **Monthly demand forecast:** The expected quantity of items needed each month.
  * **Capacity Limits:**
      * **Monthly production capacity:** Maximum items that can be produced in a month.
      * **Maximum inventory storage:** Maximum items that can be held in storage at any given time.
  * **Cost Parameters:**
      * **Production cost:** Cost incurred per item produced.
      * **Setup cost:** A fixed cost incurred each time production occurs in a month (if any items are produced).
      * **Holding cost:** Cost for carrying one item in inventory to the next month.

**🎯 Objective:** Calculate the number of items to produce each month to **exactly meet demand with minimum total cost**, without exceeding production or storage constraints.

-----

## 💡 Key Features

  * **Multi-Month Optimization:** Efficiently optimizes production and inventory plans across multiple periods.
  * **Inventory Carry-Over Logic:** Accurately accounts for inventory carried forward from one month to the next.
  * **Cost Minimization:** Focuses on minimizing the combined total of **production, setup, and holding costs**.
  * **Dynamic Programming (DP):** Utilizes a robust bottom-up DP approach for optimal decision-making.
  * **Flexible Interface:** Usable via CLI (`app.py`), with a rich web-based GUI via Streamlit.

-----

## 📦 Folder Structure

```text
SmartStock/
├── app.py                  # Main Streamlit web application entry point
├── inventory_optimizer.py  # Core DP algorithm for inventory optimization
├── ui_components.py        # Reusable UI elements (potentially for Tkinter/other GUI)
├── utils.py                # Helper utility functions
├── visualizations.py       # Functions for generating charts and plots
├── requirements.txt        # Lists all Python dependencies
├── README.md               # Project documentation (this file)
└── assets/                 # Optional: Directory for images or other assets
```

-----

## 📊 Sample Example

Let's consider a scenario with 4 months:

```python
n = 4
demand = [20, 40, 30, 10]
max_order = 50
max_storage = 30
production_cost = 3
setup_cost = 50
holding_cost = 2
```

### ✅ Optimal Production Plan Output

Given the above parameters, SmartStock would derive an optimal plan similar to this:

```text
Optimal Solution:
for month 1; order= 20
for month 2; order= 50
for month 3; order= 30
for month 4; order= 0

EOQ (Economic Order Quantity): 39.6863
```

### 💰 Cost Breakdown

The detailed cost breakdown provides insights into the expenses for each month and the total:

| Month | Produced | Used | Stored | Setup Cost | Production Cost | Holding Cost | Total |
| :---- | :------- | :--- | :----- | :--------- | :-------------- | :----------- | :---- |
| 1     | 20       | 20   | 0      | 50         | 60              | 0            | 110   |
| 2     | 50       | 40   | 10     | 50         | 150             | 20           | 220   |
| 3     | 30       | 30   | 0      | 50         | 90              | 0            | 140   |
| 4     | 0        | 10   | 0      | 0          | 0               | 0            | 0     |
| **Total Cost** | | | | | | | **470** |

-----

## ⚙️ How It Works

The core of SmartStock lies in its **Dynamic Programming** algorithm. The DP state `min_cost[t][i]` represents the **minimum cost from month `t` to the end of the planning horizon, given that you start month `t` with `i` items in storage.**

**Logic Flow:**

1.  **Iterate over each month (`t`)** from the last month backwards to the first.
2.  **For each month, iterate over every possible initial inventory level (`i`)** that can be carried over from the previous month (within `max_storage`).
3.  **For every combination of (`t`, `i`), explore all feasible production amounts (`j`)** in month `t` (from 0 up to `max_order` and enough to meet demand).
4.  **For each `j`, calculate:**
      * **Production cost:** `j * production_cost`
      * **Setup cost:** `setup_cost` (only if `j > 0`, otherwise 0)
      * **Holding cost:** For inventory carried to month `t+1`. This is based on `(i + j - demand[t]) * holding_cost`.
      * **Add future costs:** Recursively fetch `min_cost[t+1][new_inventory]` from the DP table.
5.  **Choose the option** (`j`) that results in the **lowest total cost** for `min_cost[t][i]`.

This bottom-up approach ensures that when we calculate the minimum cost for a given state, the minimum costs for all subsequent states are already known.

-----

## 🖥️ How to Run

### Web Application (Recommended: Streamlit)

To run the interactive web application, ensure you have the required dependencies installed (from `requirements.txt`).

1.  **Navigate** to the root directory of the project:
    ```bash
    cd SmartStock
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    This will open the SmartStock dashboard in your web browser. Adjust parameters in the sidebar and view the optimal plans and visualizations instantly\!

### CLI (Console)

For a command-line interface, execute the `app.py` directly:

```bash
python app.py
```

Follow the on-screen prompts to enter the months, demand, capacities, and cost parameters.

-----

## 🚀 Future Enhancements

We're continuously looking to improve SmartStock\! Potential future additions include:

  * **Export Options:** Functionality to export the optimal production plan and cost breakdown to CSV or PDF.
  * **Variable Costs:** Support for month-specific production, setup, or holding costs.
  * **Advanced Visualizations:** More interactive charts and graphs (e.g., with Matplotlib or Plotly) to analyze inventory flow and cost drivers.
  * **Multi-Item Optimization:** Extend the model to handle planning for multiple product SKUs simultaneously.
  * **Safety Stock/Service Level:** Incorporate options for maintaining a safety stock or optimizing based on a desired service level.

-----

## 🤝 Contributing

Contributions are welcome\! If you have suggestions for improvements, new features, or bug fixes, please:

1.  **Fork** the repository.
2.  **Create a new branch** for your feature or fix.
3.  **Open an issue** to discuss major changes before submitting a pull request.
4.  **Submit a pull request** with your changes.
   
-----

## 👨‍💻 Author

**Faiz Shaikh**

  * 📧 **Email:** shkfaiz2004@gmail.com
  * 🔗 **GitHub:** [@Faiz2172](https://github.com/Faiz2172)
  * 🔗 **LinkedIn:** [Faiz Shaikh](https://www.linkedin.com/in/faiz-shaikh-1a9a85258)

-----
