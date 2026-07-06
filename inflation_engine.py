import pandas as pd

def calculate_basket_weights(transaction_data):
    """
    Takes a list of transaction dictionaries, processes them into a Pandas DataFrame,
    and calculates vectorized category spending weights.
    """
    # 1. Load data into a Pandas DataFrame
    df = pd.DataFrame(transaction_data)

    print("\n--- [RAW TRANSACTION FATAFRAME] ---")
    print(df)
    print("------------------------------------\n")

    # 2. Aggragate spend by category
    category_group = df.groupby('category')['amount'].sum().reset_index()
    category_group.rename(columns= {'amount': 'category_spend'}, inplace=True)

    # 3. Calculate Total Oversll Spend
    total_spend = category_group['category_spend'].sum()
    print(f"Total Overall Budget Spend: ${total_spend:,.2f}\n")

    # 4. VECTORIZED OPERATION: Calculate Category weight %
    # This runs the math on the entire column at once without using slow for-loops!
    category_group['category_weight'] = (category_group['category_spend'] / total_spend) * 100

    # Clean up formating for display
    category_group['category_weight'] = category_group['category_weight'].round(2)

    return category_group

if __name__ == '__main__':
    # Mock data mimicking what our AI categorizer and plaid would output
    mock_transactions = [
        {"merchant": "Landlord Corp", "category": "Housing", "amount": 1500.00},
        {"merchant": "Safeway", "category": "Groceries", "amount": 150.50},
        {"merchant": "Whole Foods", "category": "Groceries", "amount": 84.20},
        {"merchant": "Shell Oil", "category": "Transport", "amount": 45.00},
        {"merchant": "Uber Rides", "category": "Transport", "amount": 25.50},
        {"merchant": "McDonalds", "category": "Fast Food/Dining", "amount": 14.80},
        {"merchant": "Chipotle", "category": "Fast Food/Dining", "amount": 18.50}
    ]

    # Run the weighting calculation
    weighted_basket = calculate_basket_weights(mock_transactions)

    print("--- [FIANL BASKET WEIGHTING RESULTS] ---")
    print(weighted_basket.to_string(index=False))
    print("----------------------------------------")