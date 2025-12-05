import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# 1️⃣ LOAD EXCEL
df = pd.read_excel("sales_data.xlsx")

# 2️⃣ ANALYSIS
total_sales = df["Sales"].sum()
grouped = df.groupby("Product")["Sales"].sum()

best_product = grouped.idxmax()
best_value = grouped.max()

worst_product = grouped.idxmin()
worst_value = grouped.min()

# 3️⃣ CHART
plt.figure()
grouped.plot(kind="bar")
plt.title("Product Sales Performance")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.close()

# 4️⃣ PDF
pdf_file = "final_sales_report.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4

c.setFont("Helvetica-Bold", 16)
c.drawString(100, height - 100, "FINAL SALES INTELLIGENCE REPORT")

c.setFont("Helvetica", 12)
c.drawString(100, height - 160, f"Total Sales: ₹{total_sales}")
c.drawString(100, height - 200, f"Best Product: {best_product} → ₹{best_value}")
c.drawString(100, height - 240, f"Worst Product: {worst_product} → ₹{worst_value}")

c.drawImage("sales_chart.png", 100, height - 500, width=350, height=220)

c.setFont("Helvetica-Oblique", 10)
c.drawString(100, 50, "Automatically generated using Python")

c.save()

print("\n✅ FULL AUTOMATION COMPLETE")
print("✅ CHART CREATED: sales_chart.png")
print("✅ PDF CREATED: final_sales_report.pdf")
