import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def train_eval_save(df, model_path):

    target = "availability_365"

    features = [
        "accommodates",
        "bedrooms",
        "beds",
        "minimum_nights",
        "number_of_reviews",
        "reviews_per_month",
    ]

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    # sklearn 구버전 호환
    rmse = np.sqrt(mean_squared_error(y_test, preds))

    joblib.dump(model, model_path)

    return {
        "rmse": float(rmse),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test))
    }