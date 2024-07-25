import pandas as pd
import secrets
import string
import csv

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

def generate_user_credentials(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Create a list to store user credentials
    user_credentials = []
    
    for index, row in df.iterrows():
        student_id = row['ID']
        password = generate_random_password()
        user_credentials.append({'username': student_id, 'password': password})
    
    # Save the user credentials to a new CSV file
    output_file = 'user_credentials.csv'
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'password'])
        writer.writeheader()
        for user in user_credentials:
            writer.writerow(user)
    
    print(f"User credentials saved to {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate user credentials from CSV file.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing student information.')
    args = parser.parse_args()
    generate_user_credentials(args.csv_file)
