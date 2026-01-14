import pandas as pd

# Read the CSV files
df_data = pd.read_csv('df_659_12_12.csv')
trials_summary = pd.read_csv('trials_summary.csv')

# Function to format time as "S.MS"
def format_time(s, ms):
    return f"{s}.{ms}"

# Process each trial
for idx, row in trials_summary.iterrows():
    trial_num = int(row['trial_number'])
    start_row = int(row['start_row'])
    end_row = int(row['end_row'])
    
    # Get the slice of data for this trial (adjusting for 0-based indexing)
    trial_data = df_data.iloc[start_row-1:end_row]
    
    # Find MagEntry timestamp (Entry state)
    mag_entry = trial_data[(trial_data['Cat'] == 'Entry') & (trial_data['State'] == 'MagEntry')]
    if not mag_entry.empty:
        mag_s = mag_entry.iloc[0]['S']
        mag_ms = mag_entry.iloc[0]['MS']
        trials_summary.at[idx, 'MagEntry'] = format_time(mag_s, mag_ms)
    
    # Find On1A1 timestamp (Input state)
    on1a1 = trial_data[(trial_data['Cat'] == 'Input') & (trial_data['State'] == 'On1A1')]
    if not on1a1.empty:
        on1a1_s = on1a1.iloc[0]['S']
        on1a1_ms = on1a1.iloc[0]['MS']
        trials_summary.at[idx, 'On1A1'] = format_time(on1a1_s, on1a1_ms)
    
    print(f"Processed trial {trial_num}: MagEntry={trials_summary.at[idx, 'MagEntry']}, On1A1={trials_summary.at[idx, 'On1A1']}")

# Save the updated trials_summary
trials_summary.to_csv('trials_summary.csv', index=False)
print("\nDone! Updated trials_summary.csv")
