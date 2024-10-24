
# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: (Dependent on the messy dataset provided)
- **Columns**: (Dependent on the messy dataset provided)

### Column Details
| Column Name    | Data Type | Non-Null Count | Unique Values           | Mean/Median (if applicable)                          |
|----------------|-----------|----------------|-------------------------|------------------------------------------------------|
| population     | float     | 119378         | 114925                  | Median used for missing values, converted to integer |
| age            | float     | 119495         | 101                     | Capped at 100, converted to integer                  |
| gender         | float     | 119811         | 3 (Male, Female, Other) | Mode used for missing values                         |
| income_groups  | string    | 119412         | 8                       | Mode used for missing values                         |
| year           | int       | 119516         | 169                     | Mode used for missing values, converted to integer   |

### Identified Issues

1. **Duplicate Rows**
   - Description: Duplicate entries in the dataset.
   - Affected Column(s): All columns.
   - Example: Multiple rows with identical values across all columns.
   - Potential Impact: Duplicates may skew analysis to overrepresent population.

2. **Missing Values**
   - Description: Missing values in multiple columns.
   - Affected Column(s): population, age, gender, income_groups.
   - Example: NaN values for gender in several rows.
   - Potential Impact: Missing data can result in biased results or skew analysis.

3. **Inconsistent Gender Representation**
   - Description: The `gender` column contains unexpected numerical representations.
   - Affected Column(s): gender.
   - Example: The value `3.0` used for missing or unknown gender.
   - Potential Impact: Misinterpretation of gender categories.

4. **Income Group Typos**
   - Description: Inconsistent naming in the `income_groups` column, such as 'low_income_typo'.
   - Affected Column(s): income_groups.
   - Example: Typos like `low_income_typo`.
   - Potential Impact: Incorrect grouping and analysis by income level.

5. **Outliers in `population` and `age`**
   - Description: Outliers detected in the `population` and `age` columns.
   - Affected Column(s): population, age.
   - Example: Population values exceeding the 99th percentile, age values exceeding 100.
   - Potential Impact: Extreme values may distort analysis.

---

## 2. Data Cleaning Process

### Issue 1: Duplicate Rows
- **Cleaning Method**: Used `drop_duplicates()` to remove all duplicate rows.
- **Implementation**:
  ```python
  df = df.drop_duplicates()
  ```
- **Justification**: Removing duplicates ensures the dataset accurately represents unique observations.
- **Impact**: Duplicate rows were successfully removed.

### Issue 2: Missing Values
- **Cleaning Method**: Filled missing values in `population` and `age` with the median, and in `gender` and `income_groups` with the mode.
- **Implementation**:
  ```python
  df['population'] = df['population'].fillna(df['population'].median())
  df['age'] = df['age'].fillna(df['age'].median())
  df['gender'] = df['gender'].fillna(3)  # Other
  df['income_groups'] = df['income_groups'].fillna(df['income_groups'].mode()[0])
  ```
- **Justification**: Imputing missing values with reasonable defaults ensures no missing data in columns.
- **Impact**: Missing values were successfully filled.

### Issue 3: Inconsistent Gender Representation
- **Cleaning Method**: Mapped `gender` values to strings for more meaningful values.
- **Implementation**:
  ```python
  gender_mapping = {1: 'Male', 2: 'Female', 3: 'Other'}
  df['gender'] = df['gender'].map(gender_mapping)
  ```
- **Justification**: Standardizing gender values makes analysis clearer and more easily understood.
- **Impact**: Gender was standardizes in a more interpretable way.

### Issue 4: Income Group Typos
- **Cleaning Method**: Replaced inconsistent income group names using `replace()`.
- **Implementation**:
  ```python
  income_group_corrections = {
      'low_income_typo': 'low_income',
      'lower_middle_income_typo': 'lower_middle_income',
      'high_income_typo': 'high_income',
      'upper_middle_income_typo': 'upper_middle_income'
  }
  df['income_groups'] = df['income_groups'].replace(income_group_corrections)
  ```
- **Justification**: Correcting these typos ensures consistency in categorical data.
- **Impact**: Income group names are now consistent.

### Issue 5: Outliers in population and age columns
- **Cleaning Method**: Capped population values at the 99th percentile and `age` at 100.
- **Implementation**:
  ```python
  population_99th = df['population'].quantile(0.99)
  df['population'] = np.where(df['population'] > population_99th, population_99th, df['population'])
  df['age'] = np.where(df['age'] > 100, 100, df['age'])  # Capping age at 100
  ```
- **Justification**: Capping outliers ensures that extreme values do not distort analysis.
- **Impact**: Outliers were removed.

### Issue 6: Unnecessary decimal places
- **Cleaning Method**: Removed training decimal for population and age columns
- **Implementation**:
  ```python
 # Convert population to integers to remove .0
        df['population'] = df['population'].astype(int)
  ```
- **Justification**: Removes confusion of decimal points value and converts to more appropriate data type.
- **Impact**: Population and age converted to integers


---

### Final Steps:
- **Data Validation**: Verified that all cleaned data falls within acceptable ranges, with no remaining missing values.
  ```python
  df['population'] = df['population'].apply(lambda x: x if x >= 0 else np.nan)
  df = df.dropna(subset=['population'])
  ```

---

## 3. Final State Analysis

### Dataset Overview
- **Name**: cleaned_population_data.csv
- **Rows**: 122768
- **Columns**: 5

### Column Details
| Column Name    | Data Type | Non-Null Count | Unique Values           | Mean/Median (if applicable)                         |
|----------------|-----------|----------------|-------------------------|-----------------------------------------------------|
| population     | int       | 122768         | 113698                  | Median after outlier handling, converted to integer |
| age            | int       | 122768         | 101                     | Median: (varies), capped at 100                     |
| gender         | object    | 122768         | 3 (Male, Female, Other) | Mode used for missing values                        |
| income_groups  | object    | 122768         | 4                       | Mode used for missing values                        |
| year           | int       | 122768         | 169                     | Mode used for missing values, converted to integer  |                             |

### Summary of Changes
- Removed duplicate rows.
- Interpolated missing values in population, age, gender, and income_groups.
- Corrected typos in the income_groups column.
- Standardized gender representation.
- Capped outliers in population and age.
- Converted `population`, `age`, and `year` columns to integers.
- Removed trailing decimals.