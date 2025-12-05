import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# ✅ Load CSV without headers, assign correct names manually
df = pd.read_csv(
    "price_alert_log.csv",
    header=None,
    names=["Product", "Current Price", "Target Price", "Status", "Checked At"]
)

# ✅ Convert index to numerical time step
df["TimeIndex"] = np.arange(len(df))

# ✅ Features (X) and Target (y)
X = df[["TimeIndex"]]
y = df["Current Price"]

# ✅ Train ML Model
model = LinearRegression()
model.fit(X, y)

# ✅ Predict next 5 future prices
future_index = np.arange(len(df), len(df) + 5).reshape(-1, 1)
future_prices = model.predict(future_index)

# ✅ Save Predictions
future_df = pd.DataFrame({
    "Future Time Index": future_index.flatten(),
    "Predicted Price": future_prices
})

future_df.to_csv("price_predictions.csv", index=False)

# ✅ Plot predictions
plt.figure()
plt.plot(df["TimeIndex"], y, label="Past Prices")
plt.plot(future_index, future_prices, label="Predicted Prices", linestyle="dashed")
plt.xlabel("Time Index")
plt.ylabel("Price")
plt.title("ML Price Prediction")
plt.legend()
plt.grid(True)
plt.savefig("price_prediction_chart.png")
plt.close()

print("\n✅ ML MODEL TRAINED SUCCESSFULLY")
print("✅ Predictions saved to price_predictions.csv")
print("✅ Chart created: price_prediction_chart.png")
