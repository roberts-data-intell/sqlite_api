from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('Sales_Project.db')
        
        # Create cursor
        cursor = conn.cursor()
        
        #data1 Top 10 Query 10 top ten products and their marketing budget and the profit
        cursor.execute("""SELECT State, MAX(Profit) as MaxProfit
                          FROM (
                          SELECT State, Market, SUM(Profit) as Profit
                          FROM Business_Data
                          GROUP BY State, Market
                          )
                          GROUP BY State;""")
        
        # Fetch data
        data = cursor.fetchall()
        
        #data2 Top 9 Query 9 Market - total profit and marketing expenses
        cursor.execute("""SELECT Market, SUM(Profit) as TotalProfit, SUM(Marketing) as TotalMarketing
                          FROM Business_Data
                          GROUP BY Market;""")
        data2 = cursor.fetchall()
        
        #data3 top 8 Query 8 Correlation Between Total Expenses and Profit in Each Market Size
        cursor.execute("""SELECT 
                          `Market Size`,
                          (
                          COUNT(*) * SUM(Profit * `Total Expenses`) - SUM(Profit) * SUM(`Total Expenses`)
                          ) / (
                          SQRT(COUNT(*) * SUM(Profit * Profit) - SUM(Profit) * SUM(Profit)) *
                          SQRT(COUNT(*) * SUM(`Total Expenses` * `Total Expenses`) - SUM(`Total Expenses`) * SUM(`Total Expenses`))
                          ) AS Correlation
                          FROM Business_Data
                          GROUP BY `Market Size`HAVING 
                          COUNT(*) * SUM(Profit * Profit) - SUM(Profit) * SUM(Profit) > 0 AND 
                          COUNT(*) * SUM(`Total Expenses` * `Total Expenses`) - SUM(`Total Expenses`) * SUM(`Total Expenses`) > 0;""")
        data3 = cursor.fetchall()
        
        #data4 top 7 Query 7 Product Types That Have Seen Sales Growth Over Time and how much
        cursor.execute("""SELECT [Product Type], (MAX(Sales) - MIN(Sales)) AS SalesGrowth
                          FROM (
                          SELECT [Product Type], Date, SUM(Sales) as Sales
                          FROM Business_Data
                          GROUP BY [Product Type], Date
                          ) as SubQuery7
                          GROUP BY [Product Type]
                          HAVING COUNT(Sales) > 1 AND MAX(Sales) > MIN(Sales);""")
        data4 = cursor.fetchall()
        
        #data5 top 6 SQL Query 6 States Where Actual COGS Are Different From 
        # Budget COGS and show by how much is the difference
        cursor.execute("""SELECT State, ABS(ActualCOGS - BudgetCOGS) AS Difference
                          FROM (
                          SELECT State, SUM(COGS) as ActualCOGS, SUM(`Budget COGS`) as BudgetCOGS
                          FROM Business_Data
                          GROUP BY State
                          ) as SubQuery6
                          WHERE ActualCOGS != BudgetCOGS;""")
        data5 = cursor.fetchall()
        
        #data6 Note Query 5 Average Inventory for Each Product Type in Each State
        cursor.execute("""SELECT State, [Product Type], ROUND(AVG(Inventory), 2) as AvgInventory
                          FROM Business_Data
                          GROUP BY State, [Product Type];""")
        data6 = cursor.fetchall()
        
        #data7 Note Query 3 Top 5 States with Highest Sales
        cursor.execute("""SELECT State, MAX(Sales) as MaxSales
                          FROM (
                          SELECT State, Market, SUM(Sales) as Sales
                          FROM Business_Data
                          GROUP BY State, Market
                          ) as SubQuery3
                          GROUP BY State
                          ORDER BY MaxSales DESC
                          LIMIT 5;""")
        data7 = cursor.fetchall()
        
        #data8 Note Query 2  Highest selling product in each market and what is the profit and Total Expenses
        cursor.execute("""SELECT 
                          Market,
                          Product,
                          MAX(Sales) as HighestSales,
                          Profit,
                          `Total Expenses`
                          FROM (
                          SELECT 
                              Market,
                              Product,
                              SUM(Sales) as Sales,
                              SUM(Profit) as Profit,
                              SUM(`Total Expenses`) as `Total Expenses`
                          FROM Business_Data
                          GROUP BY Market, Product
                          ) AS SubQuery
                          GROUP BY Market;""")
        data8 = cursor.fetchall()
        
        #data9 Note Query 1 Most Profitable Markets in Each State 
        cursor.execute("""SELECT State, MAX(Profit) as MaxProfit
                          FROM (
                          SELECT State, Market, SUM(Profit) as Profit
                          FROM Business_Data
                          GROUP BY State, Market
                          ) as SubQuery1
                          GROUP BY State;""")
        data9 = cursor.fetchall()
        
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        data = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        data6 = []
        data7 = []
        data8 = []
        data9 = []
        
    finally:
        # Close connection
        if conn:
            conn.close()
    
    return render_template("index.html", data=data, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, data8=data8, data9=data9)

if __name__ == "__main__":
    app.run(debug=True)
