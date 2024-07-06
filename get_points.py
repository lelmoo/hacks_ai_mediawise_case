import json
import pandas as pd


def rename_name(row):
    gender = ''
    age_from = row['ageFrom']
    age_to = row['ageTo']
    income = row['income'].upper()

    if row['gender'] == 'all':
        gender = 'All'
    else:
        gender = row['gender'][0].upper()

    if gender == 'All' and age_from == 18 and age_to == 100 and income == 'ABC':
        return f'All 18+'
    elif age_to == 100:
        return f'{gender} {age_from}+ {income}'
    else:
        return f'{gender} {age_from}-{age_to} {income}'
    

def get_points(json_path, data_path):
    with open(json_path, 'r') as file:
        json_data = json.load(file)

    df = pd.DataFrame([{**json_data['targetAudience'], 'sides': json_data['sides']}])
    df['name'] = df.apply(rename_name, axis=1)
    df.drop(['gender', 'ageFrom', 'ageTo', 'income'], axis=1, inplace=True)
    df = df.reset_index(drop=True)

    points = pd.read_csv(data_path)
    out = points[points['name'].isin(df['name'])].nlargest(df['sides'][0], 'value')
    return out.to_json(orient='records', force_ascii=False)


