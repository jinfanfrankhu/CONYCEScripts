import pandas as pd
import textgrid
import os

# Load the TextGrid file
def textgrid_to_df(file_path):
    '''
    Convert a TextGrid file to a pandas DataFrame.
    '''
    textgrid_file = file_path + ".TextGrid"
    tg = textgrid.TextGrid.fromFile(textgrid_file)

    # Extract data into a list of dictionaries
    data = []
    for tier in tg.tiers:
        tier_name = tier.name
        for interval in tier.intervals:
            data.append({
                'tier': tier_name,
                'xmin': interval.minTime,
                'xmax': interval.maxTime,
                'text': interval.mark
            })

    # Convert to pandas dataframe
    df = pd.DataFrame(data)

    return df

def remove_empty_entries(df):
    '''
    Remove entries where text is empty or only spaces.
    '''
    return df[~df['text'].isin(["", " "])].reset_index(drop=True)


def reassign_interviewer(df):
    '''
    Change tier name to 'Interviewer' if text ends with '?'
    '''
    df.loc[df['text'].str.strip().str.endswith("?"), 'tier'] = 'Interviewer'
    return df

import textgrid

def df_to_textgrid(df, output_path):
    '''
    Convert a pandas DataFrame back to a TextGrid file.
    The DataFrame must contain: tier, xmin, xmax, text columns.
    '''
    tg = textgrid.TextGrid()
    
    # Get all unique tiers
    tiers = df['tier'].unique()
    
    # Determine total time bounds
    min_time = df['xmin'].min()
    max_time = df['xmax'].max()
    tg.minTime = min_time
    tg.maxTime = max_time

    for tier_name in tiers:
        tier_df = df[df['tier'] == tier_name].sort_values(by='xmin')
        tier = textgrid.IntervalTier(name=tier_name, minTime=min_time, maxTime=max_time)
        for _, row in tier_df.iterrows():
            tier.add(row['xmin'], row['xmax'], row['text'])
        tg.append(tier)

    tg.write(output_path)
    return True


if __name__ == "__main__":
    file_path = r"C:\Users\jinfa\Desktop\CONYCE\SP19\conyce_bh_sp19_AaravDengla_all_interview_mod_050825"

    df = textgrid_to_df(file_path)
    df = remove_empty_entries(df)
    df = reassign_interviewer(df)
    output_path = file_path + "_processed.TextGrid"
    df_to_textgrid(df, output_path)
    
    
