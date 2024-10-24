import pandas as pd
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_population_data(input_file, output_file):
    try:
        # Load the dataset
        logging.info("Loading dataset...")
        df = pd.read_csv(input_file)
        logging.info(f"Dataset loaded successfully with shape {df.shape}")

        # Display non-null counts and unique values before cleaning
        logging.info("Displaying non-null counts and unique values before cleaning:")
        for column in df.columns:
            non_null_count = df[column].notnull().sum()
            unique_count = df[column].nunique()
            logging.info(f"{column}: Non-null count = {non_null_count}, Unique count = {unique_count}")

    except FileNotFoundError:
        logging.error(f"Error: File {input_file} not found.")
        return
    except Exception as e:
        logging.error(f"An error occurred while loading the file: {e}")
        return

    try:
        # Remove duplicate data
        logging.info("Removing duplicate rows...")
        initial_shape = df.shape
        df = df.drop_duplicates()
        logging.info(f"Removed {initial_shape[0] - df.shape[0]} duplicate rows")

        # Impute missing values using median for numerical columns and mode for categorical columns or Other for gender
        logging.info("Handling missing values...")
        df['population'] = df['population'].fillna(df['population'].median())
        df['age'] = df['age'].fillna(df['age'].median())
        df['gender'] = df['gender'].fillna(3)  # Fill missing genders with 'Other'
        df['income_groups'] = df['income_groups'].fillna(df['income_groups'].mode()[0])
        logging.info("Missing values handled")

        # Standardize gender representation
        logging.info("Standardizing gender values...")
        gender_mapping = {1: 'Male', 2: 'Female', 3: 'Other'}
        df['gender'] = df['gender'].map(gender_mapping)

        # Correct income group names
        logging.info("Correcting inconsistent income group names...")
        income_group_corrections = {
            'low_income_typo': 'low_income',
            'lower_middle_income_typo': 'lower_middle_income',
            'high_income_typo': 'high_income',
            'upper_middle_income_typo': 'upper_middle_income'
        }
        df['income_groups'] = df['income_groups'].replace(income_group_corrections)

        # Trim whitespace from categorical columns
        logging.info("Trimming whitespace from categorical columns...")
        df['income_groups'] = df['income_groups'].str.strip()

        # Calculate and handle outliers in population and age
        logging.info("Handling population and age outliers...")
        population_99th = df['population'].quantile(0.99)
        df['population'] = np.where(df['population'] > population_99th, population_99th, df['population'])

        df['age'] = np.where(df['age'] > 100, 100, df['age'])  # Capping age at 100

        # Convert population to integers to remove .0
        df['population'] = df['population'].astype(int)

        # Convert year column to integer type
        logging.info("Converting year to integer and filling missing values with mode...")
        df['year'] = df['year'].fillna(df['year'].mode()[0])
        df['year'] = df['year'].astype(int)

        # Validate data ranges
        logging.info("Validating data ranges for population and age...")
        df['population'] = df['population'].apply(lambda x: x if x >= 0 else np.nan)
        df = df.dropna(subset=['population'])  # Remove any remaining invalid population values

        # Check for any remaining missing values
        missing_after_cleaning = df.isnull().sum()
        logging.info(f"Remaining missing values after cleaning:\n{missing_after_cleaning}")

        # Convert population and age columns to integers where applicable
        logging.info("Converting 'population' and 'age' to integers where applicable...")
        df['age'] = df['age'].apply(lambda x: int(x) if x.is_integer() else x)

        # Display non-null counts and unique values after cleaning
        logging.info("Displaying non-null counts and unique values after cleaning:")
        for column in df.columns:
            non_null_count = df[column].notnull().sum()
            unique_count = df[column].nunique()
            logging.info(f"{column}: Non-null count = {non_null_count}, Unique count = {unique_count}")

        # Save the cleaned dataset
        logging.info(f"Saving cleaned data to {output_file}...")
        df.to_csv(output_file, index=False)
        logging.info("Cleaned dataset saved successfully")

    except Exception as e:
        logging.error(f"An error occurred during the cleaning process: {e}")
        return

if __name__ == "__main__":
    try:
        # Load and clean dataset and save to same directory
        clean_population_data("/Users/hteshome/Desktop/Training/Pytools_Class/06-data-munging-haile-teshome/messy_population_data.csv", "/Users/hteshome/Desktop/Training/Pytools_Class/06-data-munging-haile-teshome/cleaned_population_data.csv")
    except Exception as e:
        logging.error(f"An error occurred in the main block: {e}")
