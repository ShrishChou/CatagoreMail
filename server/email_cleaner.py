from bs4 import BeautifulSoup
import pandas as pd
import json

def get_plain_text_from_html(html_body):
    soup = BeautifulSoup(html_body, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    # Split into lines and remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    # Join non-empty lines
    clean_text = '\n'.join(lines)
    return clean_text.strip()


# Specify the path to your file
file_path = 'read_emails_snippet.json'

# Initialize empty lists to store the data
subjects = []
senders = []
bodies = []

# Read the file and parse each line as JSON
with open(file_path, 'r') as file:
    for line in file:
        json_obj = json.loads(line.strip())
        subjects.append(str(json_obj.get('subject', '')))
        senders.append(str(json_obj.get('sender', '')))
        bodies.append(str(json_obj.get('body', '')))

# Create the DataFrame with explicitly defined dtypes
df = pd.DataFrame({
    'subject': pd.Series(subjects, dtype='string'),
    'sender': pd.Series(senders, dtype='string'),
    'body': pd.Series(bodies, dtype='string')
})

# Remove rows where 'body' is "No body content"
df = df[df['body'] != "No body content"]

# Apply get_plain_text_from_html to the entire 'body' column
df['body'] = df['body'].apply(get_plain_text_from_html)
df['read'] = 1

print(df['body'].dtype)
df['body'] = df['body'].astype(str)

# Specify the output CSV file path
output_csv_path = 'cleaned_read_emails.csv'

# Write the DataFrame to a CSV file with headers
df.to_csv(output_csv_path, index=False)

print(f"Cleaned data has been written to {output_csv_path}")


