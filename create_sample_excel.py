import pandas as pd

# Create sample data
data = {
    'Name': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Wilson', 'Emily Brown'],
    'Phone': ['+1234567890', '+1987654321', '+1555123456', '+1444555666', '+1777888999']
}

df = pd.DataFrame(data)
df.to_excel('contacts_template.xlsx', index=False)
print("Sample Excel file 'contacts_template.xlsx' created successfully!")
print("The file contains the following structure:")
print(df.to_string(index=False))