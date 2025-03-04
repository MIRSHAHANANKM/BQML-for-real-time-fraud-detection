import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Strip spaces in column names
    df.columns = df.columns.str.strip()

    # Check actual column names
    print("Columns in dataset:", df.columns.tolist())

    # Drop unnecessary columns
    df = df.drop(columns=["user_id", "device_id", "ip_address"], errors="ignore")

    # Convert datetime columns to numerical values
    df["signup_time"] = pd.to_datetime(df["signup_time"])
    df["purchase_time"] = pd.to_datetime(df["purchase_time"])
    df["time_diff"] = (df["purchase_time"] - df["signup_time"]).dt.total_seconds()

    # Drop original datetime columns
    df = df.drop(columns=["signup_time", "purchase_time"], errors="ignore")

    # Encode categorical columns (one-hot encoding)
    df = pd.get_dummies(df, columns=["source", "browser", "sex"], drop_first=True)

    # Select features and labels
    X = df.drop(columns=["class"])
    y = df["class"]

    # Standardize numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, scaler

# Example usage
file_path = "meta_learning/fraud_data.csv"  # Ensure the correct path
X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(file_path)

print("Preprocessing complete. Shapes:", X_train.shape, X_test.shape)


