
import pandas as pd
import matplotlib.pyplot as plt
import calendar

# 1. Load dataset
df = pd.read_csv("sales.csv")


# 2. Initial data inspection
print(df.head())
df.info()
print(df.describe())

print(df.isna().sum())
print(df.duplicated().sum())


# 3. Convert date columns to datetime
print("--Convert date columns to datetime--")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
print(df["Ship Date"].dtypes)

df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
print(df["Order Date"].dtypes)

df["month"] = df["Order Date"].dt.month
df["year"] = df["Order Date"].dt.year

# 4. Check missing values in date columns
print("--Check missing values in date columns--")
print(df["Order Date"].isnull().sum())
print(df["Ship Date"].isnull().sum())


# 5. Check invalid sales values
print("-- Sales Check --")
invalid = (df["Sales"] <= 0).sum()
print(f"Sales: {invalid} values zero or negative")



# 6.Check extra spaces in text columns

for col in ["Product Name", "City"]:
    extra_spaces = (df[col] != df[col].str.strip()).sum()
    print(f"{col}:{extra_spaces} values with extra spaces")

# how many unique city
print(df["City"].nunique())
# print(df["City"].unique())

# how many unique product
print(df["Product Name"].nunique())
# print(df["Product Name"].unique())

# what category
print(df["Category"].unique())


print(df["Category"].value_counts())


result= df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head()
print(result)

result2= df.groupby("City")["Sales"].sum().sort_values(ascending=False).head()
print(result2)



print(df[df["City"] == "New York City"]["Order ID"].nunique())
print(df.groupby("Order ID")["Sales"].sum().mean())
print(df[df["City"] == "New York City"].groupby("Order ID")["Sales"].sum().mean())


result3 = df.groupby(["year", "month"])["Sales"].sum().sort_values(ascending=False)
print(result3)

result4 =  df.groupby("month")["Sales"].sum().sort_values(ascending=False).sort_index()


pivot = pd.pivot_table(
    df,
    index="year",
    columns="month",
    values="Sales",
    aggfunc="sum",
    fill_value=0
)

pivot["total sales"] = pivot.sum(axis=1)
pivot = pivot.sort_values(by="total sales", ascending=False)
print(pivot)

print(pivot.drop(columns="total sales").idxmax(axis=1))
print(pivot.drop(columns="total sales").max(axis=1))




plt.figure(figsize=(10, 6))

plt.barh(result.index , result.values, color="brown")
plt.xticks(rotation=50, ha="right", fontsize=8)

plt.title("Top 5 Products by Sales")

plt.xlabel("Sales")
plt.ylabel("Product")


plt.tight_layout()
plt.savefig("top5_product_by_sales.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 6))

plt.bar(result2.index , result2.values, color="brown")
plt.xticks(rotation=50, ha="right", fontsize=8)

plt.title("Top 5 Cities by Sales")

plt.xlabel("City")
plt.ylabel("Sales")


plt.tight_layout()
plt.savefig("top5_cities_by_sales.png", dpi=300, bbox_inches="tight")
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(result4.index , result4.values, color="brown" , marker="o")

plt.xticks(
    ticks=range(1, 13),
    labels=[calendar.month_name[i] for i in range(1, 13)],
    rotation=45
)

plt.title("Total Sales by Month")

plt.xlabel("Month")
plt.ylabel("Sales")


plt.tight_layout()
plt.savefig("total_Sales_by_Month.png", dpi=300, bbox_inches="tight")
plt.show()
