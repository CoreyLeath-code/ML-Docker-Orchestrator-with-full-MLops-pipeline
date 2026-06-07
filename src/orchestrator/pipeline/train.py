import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split

from orchestrator.config import settings


def main():
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment("orchestrator-training")

    # Simple synthetic dataset placeholder (swap for real dataset later)
    rng = np.random.default_rng(42)
    X = rng.normal(size=(500, 3))
    y = 2.0 * X[:, 0] - 1.0 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(scale=0.3, size=500)

    df = pd.DataFrame(X, columns=["f1", "f2", "f3"])
    df["y"] = y

    X_train, X_test, y_train, y_test = train_test_split(
        df[["f1", "f2", "f3"]], df["y"], test_size=0.2, random_state=42
    )

    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        rmse = root_mean_squared_error(y_test, preds)

        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(model, "model")

        # Register model (optional—requires MLflow registry configured)
        mlflow.register_model(
            f"runs:/{mlflow.active_run().info.run_id}/model",
            settings.model_name,
        )

    print(f"Training complete. RMSE={rmse:.4f}")


if __name__ == "__main__":
    main()
