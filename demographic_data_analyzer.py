import pandas as pd

def race_count(df):
    race_df = df['race'].value_counts().reset_index(name='total')
    return race_df

def average_age_men(df):
    return (df[df['sex']=='Male']['age'].sum()/df[df['sex']=='Male']['age'].count()).round(decimals=1)

def percentile_education(df):
    degree_df = df['education'].value_counts().reset_index(name='sum').rename(columns={'index': 'education'})
    Bachelors = degree_df[degree_df['education'] == 'Bachelors']['sum'].values[0]
    total = degree_df['sum'].sum()
    percet = (Bachelors*100)/total
    return percet.round(decimals=1)

def salary(df):
    # With advanced education
    rich = df[((df['education']=='Bachelors')|(df['education']=='Masters')|(df['education']=='Doctorate')) & (df['salary']== '>50K')].count()['salary']
    poor = df[((df['education']=='Bachelors')|(df['education']=='Masters')|(df['education']=='Doctorate')) & (df['salary']== '<=50K')].count()['salary']
    higher_education_rich = (rich*100)/(rich+poor)

    # Without advanced education
    rich = df[((df['education']!='Bachelors')&(df['education']!='Masters')&(df['education']!='Doctorate')) & (df['salary']== '>50K')].count()['salary']
    poor = df[((df['education']!='Bachelors')&(df['education']!='Masters')&(df['education']!='Doctorate')) & (df['salary']== '<=50K')].count()['salary']
    lower_education_rich = (rich*100)/(rich+poor)

    return round(higher_education_rich, 1), round(lower_education_rich, 1)

def work_hours(df):
    min_hours = df['hours-per-week'].min()
    rich = df[(df['hours-per-week']==min_hours) & (df['salary']=='>50K')]
    poor = df[(df['hours-per-week']==min_hours) & (df['salary']=='<=50K')]
    rich_percentage = (rich.count()['salary']*100)/(rich.count()['salary']+poor.count()['salary'])
    return min_hours, round(rich_percentage, 1)

def occupation(df):
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    return india_rich['occupation'].value_counts().idxmax()

def calculate_demographic_data(print_data=True):
    df = pd.read_csv('adult.data.csv')

    race_ct = race_count(df)
    avg_age_men = average_age_men(df)
    pct_bachelors = percentile_education(df)
    higher_ed_rich, lower_ed_rich = salary(df)
    min_work, rich_pct = work_hours(df)

    # Country with highest percentage of people earning >50K
    rich = df.groupby(['native-country', 'salary']).size().unstack(fill_value=0)
    rich['>50K_pct'] = (rich['>50K'] / (rich['>50K'] + rich['<=50K'])) * 100
    top_country_pct = rich['>50K_pct'].max()
    top_country = rich['>50K_pct'].idxmax()

    top_job_india = occupation(df)

    if print_data:
        print("Number of each race:\n", race_ct)
        print("Average age of men:", avg_age_men)
        print(f"Percentage with Bachelors degrees: {pct_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_ed_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_ed_rich}%")
        print(f"Min work time: {min_work} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_pct}%")
        print("Country with highest percentage of rich:", top_country)
        print(f"Highest percentage of rich people in country: {top_country_pct}%")
        print("Top occupations in India:", top_job_india)

    return {
        'race_count': race_ct,
        'average_age_men': avg_age_men,
        'percentage_bachelors': pct_bachelors,
        'higher_education_rich': higher_ed_rich,
        'lower_education_rich': lower_ed_rich,
        'min_work_hours': min_work,
        'rich_percentage': rich_pct,
        'highest_earning_country': top_country,
        'highest_earning_country_percentage': round(top_country_pct, 1),
        'top_IN_occupation': top_job_india
    }

