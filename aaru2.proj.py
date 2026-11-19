    print("Lowest order value:", df["Sales"].min())
    print("Total quantity sold:", df["Quantity"].sum())

    if "Date" in df.columns and df["Date"].notna().any():
        monthly_sales = (
            df.dropna(subset=["Date"])
            .assign(Month=lambda x: x["Date"].dt.to_period("M").astype(str))
            .groupby("Month", as_index=False)["Sales"].sum()
        )
        print("\nMonthly sales:\n", monthly_sales)
    else:
        monthly_sales = pd.DataFrame(columns=["Month", "Sales"])

    correlation = df[["Quantity", "Unit_Price", "Sales"]].corr()
    print("\nCorrelation matrix:\n", correlation)

    return monthly_sales, correlation


# ------------------------------------------------------------------
# EXERCISE 6: Visualize the data
# ------------------------------------------------------------------

def create_visualizations(df, product_summary, region_summary, monthly_sales):
    print("\n" + "=" * 60)
    print("EXERCISE 6: DATA VISUALIZATION")
    print("=" * 60)

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(9, 5))
    sns.barplot(data=product_summary, x="Product", y="Total_Sales")
    plt.title("Total Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "sales_by_product.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(data=region_summary, x="Region", y="Sales")
    plt.title("Total Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "sales_by_region.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="Sales", bins=8, kde=True)
    plt.title("Distribution of Order Sales")
    plt.xlabel("Sales")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "sales_distribution.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="Quantity", y="Sales", hue="Category", s=90)
    plt.title("Quantity vs Sales")
    plt.xlabel("Quantity")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "quantity_vs_sales.png", dpi=150)
    plt.close()

    if not monthly_sales.empty:
        plt.figure(figsize=(8, 5))
        sns.lineplot(data=monthly_sales, x="Month", y="Sales", marker="o")
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.tight_layout()
        plt.savefig(PLOT_DIR / "monthly_sales_trend.png", dpi=150)
        plt.close()

    plt.figure(figsize=(7, 5))
    sns.heatmap(
        df[["Quantity", "Unit_Price", "Sales"]].corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )
    plt.title("Sales Data Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "correlation_heatmap.png", dpi=150)
    plt.close()

    print(f"Charts saved to: {PLOT_DIR}")


# ------------------------------------------------------------------
# EXERCISE 7: Export results
# ------------------------------------------------------------------

def export_results(df, product_summary, region_summary, monthly_sales):
    df.to_csv(OUTPUT_DIR / "cleaned_sales_data.csv", index=False)
    product_summary.to_csv(OUTPUT_DIR / "product_sales_summary.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "region_sales_summary.csv", index=False)
    monthly_sales.to_csv(OUTPUT_DIR / "monthly_sales_summary.csv", index=False)
    print("\nOutput CSV files saved in:", OUTPUT_DIR)


def main():
    print("=" * 60)
    print("HANDS-ON DATA LAB IMPLEMENTATION")
    print("=" * 60)

    data = load_data()
    inspect_data(data)

    cleaned = clean_data(data)
    product_summary, region_summary = manipulate_data(cleaned)
    monthly_sales, _ = analyze_data(cleaned)

    create_visualizations(
        cleaned, product_summary, region_summary, monthly_sales
    )
    export_results(cleaned, product_summary, region_summary, monthly_sales)

    print("\nDATA LAB COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
