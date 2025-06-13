import pandas as pd
import json
import os

def extract_table_from_csv(filepath, start_marker, end_marker=None, columns=None, col_indices=None, delimiter=';'):
    """Extracts a table from a CSV file between start_marker and end_marker (if provided)."""
    data = []
    with open(filepath, encoding='utf-8-sig') as f:
        in_table = False
        for line in f:
            row = [c.strip() for c in line.strip().split(delimiter)]
            if not in_table and row[0] == start_marker:
                in_table = True
                if columns:
                    data.append(columns)
                continue
            if in_table:
                if end_marker and row[0] == end_marker:
                    break
                if col_indices:
                    row = [row[i] for i in col_indices]
                data.append(row)
    if data:
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    return pd.DataFrame()

def prepare_data():
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    print("Starting data preparation...")

    # --- Section 1: Household Expenditure Distribution by Main Consumption Categories (Table 2.5) ---
    try:
        file_25 = 'data/24 HIES - ADePT tables - Food Consumption.xlsx - Table 2.5.csv'
        df_expenditure = extract_table_from_csv(
            file_25,
            start_marker='Cereals and their products',
            end_marker='Food additives',
            columns=['Category', 'Energy', 'Protein', 'Carbohydrates', 'Fat'],
            col_indices=[0,1,2,3,4],
            delimiter=';'
        )
        # Add the last row (Food additives)
        with open(file_25, encoding='utf-8-sig') as f:
            for line in f:
                if line.startswith('Food additives'):
                    row = [c.strip() for c in line.strip().split(';')]
                    df_expenditure.loc[len(df_expenditure)] = row[:5]
        df_expenditure['Share'] = df_expenditure['Energy'].str.replace(',', '.').astype(float)
        df_expenditure = df_expenditure[['Category', 'Share']].dropna()
        df_expenditure.to_json(os.path.join(output_dir, 'food_expenditure_by_category.json'), orient='records', indent=4)
        print("Generated food_expenditure_by_category.json")
    except Exception as e:
        print(f"Error preparing food_expenditure_by_category.json: {e}")

    # --- Section 2: Household Food Security (Nutrient Intake Summary - Table 2.2) ---
    try:
        file_22 = 'data/24 HIES - ADePT tables - Food Consumption.xlsx - Table 2.2.csv'
        df_nutrient = extract_table_from_csv(
            file_22,
            start_marker='Cereals and their products',
            end_marker='Food additives',
            columns=['Nutrient', 'Quantity', 'Value', 'Energy', 'Protein', 'Carbohydrates', 'Fat'],
            col_indices=[0,1,2,3,4,5,6],
            delimiter=';'
        )
        with open(file_22, encoding='utf-8-sig') as f:
            for line in f:
                if line.startswith('Food additives'):
                    row = [c.strip() for c in line.strip().split(';')]
                    df_nutrient.loc[len(df_nutrient)] = row[:7]
        records = []
        for col, label in zip(['Energy', 'Protein', 'Fat'], ['Energy (kcal)', 'Protein (g)', 'Fat (g)']):
            val = pd.to_numeric(df_nutrient[col].str.replace(',', '.'), errors='coerce').sum()
            val = float(val) if not pd.isna(val) else None
            records.append({'Nutrient': label, 'AverageIntake': val})
        with open(os.path.join(output_dir, 'nutrient_intake_summary.json'), 'w') as f:
            json.dump(records, f, indent=4)
        print("Generated nutrient_intake_summary.json")
    except Exception as e:
        print(f"Error preparing nutrient_intake_summary.json: {e}")

    # --- Section 3: Food Consumption by Source (Table 1.2) ---
    try:
        file_12 = 'data/24 HIES - ADePT tables - Food Consumption.xlsx - Table 1.2.csv'
        with open(file_12, encoding='utf-8-sig') as f:
            for line in f:
                if line.startswith('Palau'):
                    row = [c.strip() for c in line.strip().split(';')]
                    shares = row[3:7]
                    sources = ['Purchased', 'Own Produced', 'Away from Home', 'Other Sources']
                    df_out = pd.DataFrame({'Source': sources, 'Share': [float(s.replace(',', '.')) for s in shares]})
                    df_out.to_json(os.path.join(output_dir, 'food_source_distribution.json'), orient='records', indent=4)
                    print("Generated food_source_distribution.json")
                    break
    except Exception as e:
        print(f"Error preparing food_source_distribution.json: {e}")

    # --- Section 4: Welfare Indicators by Region (Urban vs. Rural) (Table 1.1) ---
    try:
        file_11 = 'data/24 HIES - ADePT tables - Food Consumption.xlsx - Table 1.1.csv'
        regions = []
        with open(file_11, encoding='utf-8-sig') as f:
            for line in f:
                if line.startswith('Urban') or line.startswith('Rural'):
                    row = [c.strip() for c in line.strip().split(';')]
                    regions.append({'Region': row[0], 'AverageFoodConsumption': float(row[5].replace(',', '.'))})
        if regions:
            with open(os.path.join(output_dir, 'regional_food_consumption.json'), 'w') as f:
                json.dump(regions, f, indent=4)
            print("Generated regional_food_consumption.json")
    except Exception as e:
        print(f"Error preparing regional_food_consumption.json: {e}")

    print("Data preparation complete.")

if __name__ == '__main__':
    prepare_data()