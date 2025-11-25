import pandas as pd
import numpy as np

df = pd.read_csv("thesis_final_data.csv")
print ("dataframe loaded")

df = df.replace(["", " ", "N/A", "na", "NaN"], np.nan)
print ('empty values replaced')


numeric_vars = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q9', 'Q10', 'Q11', 'Q14']

for col in numeric_vars:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        print(f"WARNING: Column '{col}' not found in dataframe!")

q12_cols = [f"Q12_{i}" for i in range(1, 10)]
q15_cols = [f"Q15_{i}" for i in range(1, 13)]

matrix_cols = q12_cols + q15_cols

for col in matrix_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        print(f"WARNING: {col} not found in dataset")

# safety score
df['safety_score'] = 0.8 * df['Q10'] + 0.2 * df['Q9']

numeric_safety = ['safety_score']
for col in numeric_safety:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        print(f"WARNING: Column '{col}' not found in dataframe!")

print(df['safety_score'].mean())

# gender
df["gender_recode"] = df["Q4"].apply(lambda x: 1 if x == 1 else 0)

print(df["gender_recode"].value_counts())

# variable labels

nationality_labels = {
    1: "Dutch",
    2: "EU",
    3: "Non-EU"
}

df["nationality_label"] = df["Q5"].map(nationality_labels)

duration_residence_labels = {
    1: "< 3 months",
    2: "3 - 6 months",
    3: "6 months - 2 years",
    4: "2 - 4 years",
    5: "> 4 years",
}

df["duration_residence_labels"] = df['Q6'].map(duration_residence_labels)

frequency_outside_labels = {
    1: "avoid it",
    2: "1-2/ week",
    3: "3-5/ week",
    4: "6-7/ week",
}

df["frequency_outside_labels"] = df['Q14'].map(frequency_outside_labels)

print("labels assigned")

df = df[(df["Q1"] == 1) & (df["Q3"] == 1)]

df = df.drop(columns=["Q8", "Q13", "Q16"], errors="ignore")

df.to_csv("cleaned_data.csv", index=False)

print("new CSV file saved")




