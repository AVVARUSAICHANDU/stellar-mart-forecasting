import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Load daily sales
daily = pd.read_csv("data/daily_sales.csv")

# Feature engineering
daily["day_number"] = np.arange(len(daily))

# Train-test split
X = daily[["day_number"]]
y = daily["daily_sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Train linear model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
preds = model.predict(X_test)

# Save model
joblib.dump(model, "models/sales_model.pkl")

# Save test predictions
out = pd.DataFrame({
    "actual": y_test.values,
    "predicted": preds
})
out.to_csv("models/test_predictions.csv", index=False)

print("Model trained and saved as models/sales_model.pkl")
print("Test predictions saved to models/test_predictions.csv")