def calculate_kpis(df):

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    total_orders = df["Order ID"].nunique()

    avg_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value
    }