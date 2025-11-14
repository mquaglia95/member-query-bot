import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timezone
from collections import Counter
import os

# Create output directory for charts
os.makedirs("analysis_output", exist_ok=True)

# Load data
print("Loading data...")
with open("../messages.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Handle paginated API response structure
if isinstance(data, dict) and "items" in data:
    messages = data["items"]
else:
    messages = data

df = pd.DataFrame(messages)

# Start building the report
report = []

def add_section(title):
    report.append(f"\n{'='*80}")
    report.append(f"{title.center(80)}")
    report.append(f"{'='*80}\n")

def add_text(text):
    report.append(text)

# basic summary
add_section("DATA OVERVIEW")
add_text(f"Total number of messages: {len(df)}")
add_text(f"Number of columns: {len(df.columns)}")
add_text(f"Columns: {list(df.columns)}\n")

# display first ten rows of data
add_section("FIRST 10 ROWS OF DATA")
add_text(df.head(10).to_string())

# meta data and basic stats
add_section("DATA TYPES")
add_text(df.dtypes.to_string())
add_text("\n")

add_section("BASIC STATISTICS")
add_text(df.describe(include='all').to_string())

# null value analysis
add_section("NULL VALUE ANALYSIS")

null_counts = df.isnull().sum()  # <-- DEFINED HERE
null_percentages = (df.isnull().sum() / len(df) * 100).round(2)
null_df = pd.DataFrame({
    'Column': null_counts.index,
    'Null Count': null_counts.values,
    'Null Percentage': null_percentages.values
})
add_text(null_df.to_string())

# null value visualizations
if null_counts.sum() > 0:  # <-- USED HERE (should work)
    plt.figure(figsize=(10, 6))
    null_percentages.plot(kind='bar', color='salmon')
    plt.title('Percentage of Null Values by Column', fontsize=14, fontweight='bold')
    plt.xlabel('Column')
    plt.ylabel('Null Percentage (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('analysis_output/null_values.png', dpi=300)
    plt.close()
    add_text("\n📊 Chart saved: analysis_output/null_values.png\n")
else:
    add_text("\n✅ No null values present - no null percentage chart needed.\n")

# missing value stats
add_section("EMPTY OR WHITESPACE VALUES")

empty_stats = {}
for col in df.columns:
    if df[col].dtype == 'object':
        empty_count = df[col].str.strip().eq('').sum()
        empty_stats[col] = {
            'Empty Count': empty_count,
            'Empty Percentage': round(empty_count / len(df) * 100, 2)
        }

empty_df = pd.DataFrame(empty_stats).T
add_text(empty_df.to_string())

# analysis of message details
add_section("MESSAGE LENGTH DETAILS")

df['message_length'] = df['message'].fillna('').str.len()

length_stats = df['message_length'].describe()
add_text(length_stats.to_string())

# message length distribution
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
df['message_length'].hist(bins=50, color='skyblue', edgecolor='black')
plt.title('Message Length Distribution', fontweight='bold')
plt.xlabel('Message Length (characters)')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.3)

plt.subplot(1, 2, 2)
df['message_length'].plot(kind='box', color='lightgreen')
plt.title('Message Length Box Plot', fontweight='bold')
plt.ylabel('Message Length (characters)')
plt.tight_layout()
plt.savefig('analysis_output/message_length.png', dpi=300)
plt.close()
add_text("\n📊 Chart saved: analysis_output/message_length.png\n")

# user analysis
add_section("USER ANALYSIS")

unique_users = df['user_id'].nunique()
unique_names = df['user_name'].nunique()
add_text(f"Unique user IDs: {unique_users}")
add_text(f"Unique user names: {unique_names}")

# top 10 users by message count
top_users = df['user_name'].value_counts().head(10)
add_text("\nTop 10 Users by Message Count:")
add_text(top_users.to_string())

# user activity chart
plt.figure(figsize=(12, 6))
top_users.plot(kind='barh', color='coral')
plt.title('Top 10 Most Active Users', fontsize=14, fontweight='bold')
plt.xlabel('Number of Messages')
plt.ylabel('User Name')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('analysis_output/top_users.png', dpi=300)
plt.close()
add_text("\n📊 Chart saved: analysis_output/top_users.png\n")

# user id consistency check
add_section("USER ID CONSISTENCY ANALYSIS")

user_id_to_names = df.groupby('user_id')['user_name'].apply(lambda x: set(x.dropna())).to_dict()
inconsistent_users = {uid: names for uid, names in user_id_to_names.items() if len(names) > 1}

add_text(f"User IDs with multiple different names: {len(inconsistent_users)}")
if inconsistent_users:
    add_text("\nExamples of inconsistent user_id to user_name mappings:")
    for i, (uid, names) in enumerate(list(inconsistent_users.items())[:10]):
        add_text(f"  User ID: {uid}")
        add_text(f"    Names: {names}")
        if i >= 9:
            break

# timestamp analysis
add_section("TIMESTAMP ANALYSIS")

# convert timestamps
df['timestamp_parsed'] = pd.to_datetime(df['timestamp'], errors='coerce')

# check for invalid timestamps
now = datetime.now(timezone.utc)
future_count = (df['timestamp_parsed'] > now).sum()
add_text(f"Messages with future timestamps: {future_count}")

invalid_count = df['timestamp_parsed'].isnull().sum()
add_text(f"Messages with invalid timestamps: {invalid_count}")

# timestamp distribution
if not df['timestamp_parsed'].isnull().all():
    df['date'] = df['timestamp_parsed'].dt.date
    daily_counts = df.groupby('date').size()
    
    plt.figure(figsize=(14, 6))
    daily_counts.plot(kind='line', color='mediumpurple', linewidth=2)
    plt.title('Messages Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('analysis_output/messages_over_time.png', dpi=300)
    plt.close()
    add_text("\n📊 Chart saved: analysis_output/messages_over_time.png\n")

# null value correlations
add_section("NULL VALUE PATTERN ANALYSIS")

if null_counts.sum() > 0:
    # null indicator columns
    null_pattern = df.isnull().astype(int)
    null_pattern.columns = [f'{col}_null' for col in null_pattern.columns]

    # combine with original
    combined = pd.concat([df, null_pattern], axis=1)

    # analyze common null patterns
    add_text("Common null value combinations:")
    null_combinations = combined[[col for col in combined.columns if '_null' in col]].value_counts().head(10)
    add_text(null_combinations.to_string())

    # heatmap of null values
    plt.figure(figsize=(10, 8))
    null_corr = null_pattern.corr()
    sns.heatmap(null_corr, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Between Null Values in Different Columns', 
              fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('analysis_output/null_correlation.png', dpi=300)
    plt.close()
    add_text("\n📊 Chart saved: analysis_output/null_correlation.png\n")
else:
    add_text("✅ No null values present - no pattern analysis needed.\n")

# character encoding analysis
add_section("CHARACTER ENCODING ANALYSIS")

non_ascii_count = df['message'].fillna('').apply(lambda x: any(ord(c) > 127 for c in x)).sum()
add_text(f"Messages with non-ASCII characters: {non_ascii_count}")
add_text(f"Percentage: {round(non_ascii_count / len(df) * 100, 2)}%")

# data quality summary
add_section("DATA QUALITY SUMMARY")

quality_issues = []

if null_counts.sum() > 0:
    quality_issues.append(f"⚠️  Found {null_counts.sum()} total null values across columns")

if len(inconsistent_users) > 0:
    quality_issues.append(f"⚠️  {len(inconsistent_users)} user IDs map to multiple different names")

if future_count > 0:
    quality_issues.append(f"⚠️  {future_count} messages have future timestamps")

if invalid_count > 0:
    quality_issues.append(f"⚠️  {invalid_count} messages have invalid timestamp formats")

if non_ascii_count > 0:
    quality_issues.append(f"ℹ️  {non_ascii_count} messages contain non-ASCII characters")

if not quality_issues:
    add_text("✅ No significant data quality issues detected!")
else:
    add_text("Data Quality Issues Found:\n")
    for issue in quality_issues:
        add_text(issue)

# save report
report_text = '\n'.join(report)

with open('analysis_output/data_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)

print("\n" + "="*80)
print("DATA ANALYSIS COMPLETE".center(80))
print("="*80)
print(f"\n📄 Full report saved to: analysis_output/data_analysis_report.txt")
print(f"📊 Charts saved to: analysis_output/")
print("\nGenerated files:")
print("  - data_analysis_report.txt")
print("  - null_values.png")
print("  - message_length.png")
print("  - top_users.png")
print("  - messages_over_time.png")
print("  - null_correlation.png")