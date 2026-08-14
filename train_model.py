import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================================================
# 1. LOAD DATA
# =========================================================

file = "EduPro Online Platform.xlsx"

users = pd.read_excel(file, sheet_name="Users")
teachers = pd.read_excel(file, sheet_name="Teachers")
courses = pd.read_excel(file, sheet_name="Courses")
transactions = pd.read_excel(file, sheet_name="Transactions")


# =========================================================
# 2. MERGE DATA
# =========================================================

df = transactions.merge(
    courses,
    on="CourseID",
    how="left"
)

df = df.merge(
    teachers,
    on="TeacherID",
    how="left"
)

df = df.merge(
    users,
    on="UserID",
    how="left"
)


# =========================================================
# 3. DATE FEATURES
# =========================================================

df["TransactionDate"] = pd.to_datetime(
    df["TransactionDate"]
)

df["Year"] = df["TransactionDate"].dt.year
df["Month"] = df["TransactionDate"].dt.month
df["Day"] = df["TransactionDate"].dt.day


# =========================================================
# 4. COURSE LEVEL DATA
# =========================================================

course_data = (
    df.groupby("CourseID")
    .agg(
        EnrollmentCount=("TransactionID", "count"),
        CourseRevenue=("Amount", "sum"),

        CourseCategory=("CourseCategory", "first"),
        CourseType=("CourseType", "first"),
        CourseLevel=("CourseLevel", "first"),
        CoursePrice=("CoursePrice", "first"),
        CourseDuration=("CourseDuration", "first"),
        CourseRating=("CourseRating", "first"),

        YearsOfExperience=("YearsOfExperience", "first"),
        TeacherRating=("TeacherRating", "first"),
        Expertise=("Expertise", "first")
    )
    .reset_index()
)


# =========================================================
# 5. FEATURE ENGINEERING
# =========================================================

course_data["PriceBand"] = pd.cut(
    course_data["CoursePrice"],
    bins=[-np.inf, 50, 150, np.inf],
    labels=["Low", "Medium", "High"]
)

course_data["DurationBucket"] = pd.cut(
    course_data["CourseDuration"],
    bins=[-np.inf, 20, 50, np.inf],
    labels=["Short", "Medium", "Long"]
)

course_data["RatingTier"] = pd.cut(
    course_data["CourseRating"],
    bins=[0, 3, 4, 5],
    labels=["Low", "Good", "Excellent"],
    include_lowest=True
)

course_data["ExperienceBucket"] = pd.cut(
    course_data["YearsOfExperience"],
    bins=[-np.inf, 2, 5, 10, np.inf],
    labels=[
        "Beginner",
        "Intermediate",
        "Experienced",
        "Expert"
    ]
)

course_data["RevenuePerEnrollment"] = (
    course_data["CourseRevenue"] /
    course_data["EnrollmentCount"]
)


# =========================================================
# 6. REMOVE MISSING VALUES
# =========================================================

course_data = (
    course_data
    .replace([np.inf, -np.inf], np.nan)
    .dropna()
    .reset_index(drop=True)
)


# =========================================================
# 7. FEATURES
# =========================================================

features = [
    "CourseCategory",
    "CourseType",
    "CourseLevel",
    "CoursePrice",
    "CourseDuration",
    "CourseRating",
    "YearsOfExperience",
    "TeacherRating",
    "Expertise",
    "PriceBand",
    "DurationBucket",
    "RatingTier",
    "ExperienceBucket"
]

X = course_data[features]


categorical_features = [
    "CourseCategory",
    "CourseType",
    "CourseLevel",
    "Expertise",
    "PriceBand",
    "DurationBucket",
    "RatingTier",
    "ExperienceBucket"
]

numerical_features = [
    "CoursePrice",
    "CourseDuration",
    "CourseRating",
    "YearsOfExperience",
    "TeacherRating"
]


# =========================================================
# 8. PREPROCESSOR
# =========================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_features
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        )
    ]
)


# =========================================================
# 9. MODELS
# =========================================================

models = {

    "Linear Regression":
        LinearRegression(),

    "Ridge":
        Ridge(alpha=1.0),

    "Lasso":
        Lasso(alpha=0.01),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=200,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingRegressor(
            n_estimators=200,
            random_state=42
        )
}


# =========================================================
# 10. TRAINING FUNCTION
# =========================================================

def train_models(target, file_name):

    print("\n===================================")
    print("TARGET:", target)
    print("===================================")

    y = course_data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    results = []

    best_model = None
    best_r2 = -np.inf
    best_name = None

    for name, model in models.items():

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model)
            ]
        )

        pipeline.fit(
            X_train,
            y_train
        )

        predictions = pipeline.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        results.append({
            "Model": name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        })

        print(
            f"{name}: "
            f"MAE={mae:.2f}, "
            f"RMSE={rmse:.2f}, "
            f"R2={r2:.4f}"
        )

        if r2 > best_r2:

            best_r2 = r2
            best_model = pipeline
            best_name = name

    results_df = pd.DataFrame(results)

    print("\nBest Model:", best_name)

    joblib.dump(
        best_model,
        file_name
    )

    return results_df, best_model


# =========================================================
# 11. ENROLLMENT MODEL
# =========================================================

enrollment_results, enrollment_model = train_models(
    "EnrollmentCount",
    "enrollment_model.pkl"
)


# =========================================================
# 12. COURSE REVENUE MODEL
# =========================================================

revenue_results, revenue_model = train_models(
    "CourseRevenue",
    "course_revenue_model.pkl"
)


# =========================================================
# 13. CATEGORY REVENUE MODEL
# =========================================================

category_data = (
    df.groupby("CourseCategory")
    .agg(
        CategoryRevenue=("Amount", "sum"),
        CategoryEnrollments=("TransactionID", "count"),
        AveragePrice=("CoursePrice", "mean"),
        AverageRating=("CourseRating", "mean"),
        AverageTeacherRating=("TeacherRating", "mean"),
        AverageExperience=("YearsOfExperience", "mean")
    )
    .reset_index()
)


category_features = [
    "CourseCategory",
    "CategoryEnrollments",
    "AveragePrice",
    "AverageRating",
    "AverageTeacherRating",
    "AverageExperience"
]

X_category = category_data[category_features]

y_category = category_data["CategoryRevenue"]


category_preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            [
                "CategoryEnrollments",
                "AveragePrice",
                "AverageRating",
                "AverageTeacherRating",
                "AverageExperience"
            ]
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            ["CourseCategory"]
        )
    ]
)


category_model = Pipeline(
    steps=[
        ("preprocessor", category_preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42
            )
        )
    ]
)


category_model.fit(
    X_category,
    y_category
)


category_predictions = category_model.predict(
    X_category
)


category_mae = mean_absolute_error(
    y_category,
    category_predictions
)

category_rmse = np.sqrt(
    mean_squared_error(
        y_category,
        category_predictions
    )
)

category_r2 = r2_score(
    y_category,
    category_predictions
)


joblib.dump(
    category_model,
    "category_revenue_model.pkl"
)


# =========================================================
# 14. FEATURE IMPORTANCE
# =========================================================

def save_feature_importance(model, file_name):

    preprocessor = model.named_steps["preprocessor"]
    trained_model = model.named_steps["model"]

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    if hasattr(
        trained_model,
        "feature_importances_"
    ):

        importance = (
            trained_model
            .feature_importances_
        )

    elif hasattr(
        trained_model,
        "coef_"
    ):

        importance = np.abs(
            trained_model.coef_
        )

    else:
        return

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importance
    })

    importance_df = (
        importance_df
        .sort_values(
            "Importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    joblib.dump(
        importance_df,
        file_name
    )

    importance_df.to_csv(
        file_name.replace(".pkl", ".csv"),
        index=False
    )


# Save feature importance

save_feature_importance(
    enrollment_model,
    "enrollment_feature_importance.pkl"
)

save_feature_importance(
    revenue_model,
    "revenue_feature_importance.pkl"
)


# =========================================================
# 15. SAVE MODEL RESULTS
# =========================================================

all_results = pd.concat(
    [
        enrollment_results.assign(
            Target="Enrollment Count"
        ),

        revenue_results.assign(
            Target="Course Revenue"
        ),

        pd.DataFrame({
            "Model": ["Random Forest"],
            "MAE": [category_mae],
            "RMSE": [category_rmse],
            "R2": [category_r2],
            "Target": ["Category Revenue"]
        })
    ],
    ignore_index=True
)


all_results.to_csv(
    "model_results.csv",
    index=False
)


# =========================================================
# 16. FINAL OUTPUT
# =========================================================

print("\n===================================")
print("ALL MODELS TRAINED SUCCESSFULLY")
print("===================================")

print("\nSaved files:")

print("✓ enrollment_model.pkl")
print("✓ course_revenue_model.pkl")
print("✓ category_revenue_model.pkl")
print("✓ enrollment_feature_importance.pkl")
print("✓ revenue_feature_importance.pkl")
print("✓ model_results.csv")