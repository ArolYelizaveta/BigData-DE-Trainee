import pandas as pd

columns = [
    'age', 'workclass', 'fnlwgt', 'education', 'education-num',
    'marital-status', 'occupation', 'relationship', 'race', 'sex',
    'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'salary'
]

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data'
data = pd.read_csv(url, header=None, names=columns, sep=',\s*', na_values='?', engine='python')

print("--- Первые 5 строк датасета ---")
print(data.head())
print("\n" + "="*50 + "\n")


# --- Задача 1: Посчитать, сколько мужчин и женщин ---
print("--- 1. Количество мужчин и женщин ---")
print(data['sex'].value_counts())
print("\n" + "="*50 + "\n")


# --- Задача 2: Средний возраст мужчин ---
print("--- 2. Средний возраст мужчин ---")
avg_male_age = data[data['sex'] == 'Male']['age'].mean()
print(f"Средний возраст мужчин: {avg_male_age:.2f} лет")
print("\n" + "="*50 + "\n")


# --- Задача 3: Доля граждан США ---
print("--- 3. Доля граждан Соединенных Штатов ---")
us_citizens_share = (data['native-country'] == 'United-States').sum() / len(data) * 100
print(f"Доля граждан США: {us_citizens_share:.2f}%")
print("\n" + "="*50 + "\n")


# --- Задачи 4-5: Среднее и ст. отклонение возраста по зарплате ---
print("--- 4-5. Статистика возраста для зарабатывающих >50K и <=50K ---")
age_stats_by_salary = data.groupby('salary')['age'].agg(['mean', 'std'])
print(age_stats_by_salary)
print("\n" + "="*50 + "\n")


# --- Задача 6: Проверка уровня образования у высокооплачиваемых ---
print("--- 6. Правда ли, что люди, которые получают >50k, имеют высшее образование? ---")
higher_education = ['Bachelors', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', 'Masters', 'Doctorate']
high_earners_education = data[data['salary'] == '>50K']['education']
is_all_higher_edu = high_earners_education.isin(higher_education).all()
print(f"Утверждение, что все с доходом >50K имеют высшее образование, является: {is_all_higher_edu}")
if not is_all_higher_edu:
    print("\nПримеры уровней образования, не относящихся к высшему, среди людей с доходом >50K:")
    print(high_earners_education[~high_earners_education.isin(higher_education)].unique())
print("\n" + "="*50 + "\n")


# --- Задача 7: Статистика возраста по расе и полу ---
print("--- 7. Статистика возраста для каждой расы и пола ---")
age_stats_by_race_sex = data.groupby(['race', 'sex'])['age'].describe()
print(age_stats_by_race_sex)
max_age_asian_male = age_stats_by_race_sex.loc[('Asian-Pac-Islander', 'Male'), 'max']
print(f"\nМаксимальный возраст мужчин расы Asian-Pac-Islander: {int(max_age_asian_male)} лет")
print("\n" + "="*50 + "\n")


# --- Задача 8: Доля зарабатывающих >50K среди женатых и холостых мужчин ---
print("--- 8. Доля зарабатывающих >50K: женатые vs холостые мужчины ---")
men_data = data[data['sex'] == 'Male'].copy()
men_data['marital_category'] = men_data['marital-status'].apply(
    lambda x: 'Married' if x.startswith('Married') else 'Single'
)
salary_dist = pd.crosstab(men_data['marital_category'], men_data['salary'], normalize='index')
print(salary_dist)
print("\nВывод: Доля зарабатывающих много (>50K) значительно выше среди женатых мужчин.")
print("\n" + "="*50 + "\n")


# --- Задача 9: Максимальное количество рабочих часов в неделю ---
print("--- 9. Анализ максимального количества рабочих часов ---")
max_hours = data['hours-per-week'].max()
people_with_max_hours = data[data['hours-per-week'] == max_hours].shape[0]
rich_percentage_max_hours = (data[data['hours-per-week'] == max_hours]['salary'] == '>50K').sum() / people_with_max_hours * 100
print(f"Максимальное количество часов в неделю: {max_hours} часов")
print(f"Количество людей, работающих столько: {people_with_max_hours} человек")
print(f"Процент зарабатывающих >50K среди них: {rich_percentage_max_hours:.2f}%")
print("\n" + "="*50 + "\n")


# --- Задача 10: Среднее время работы по странам и зарплате ---
print("--- 10. Среднее время работы (hours-per-week) по странам и зарплате ---")
avg_hours_by_country_salary = data.groupby(['native-country', 'salary'])['hours-per-week'].mean().unstack()
print(avg_hours_by_country_salary.head(10)) # Выводим первые 10 стран для примера
print("\n" + "="*50 + "\n")


# --- Задача 11: Группировка по возрасту ---
print("--- 11. Создание возрастных групп ---")
bins = [15, 35, 70, 100]
labels = ['young', 'adult', 'retiree']
data['AgeGroup'] = pd.cut(data['age'], bins=bins, labels=labels, right=True)
print("Первые 5 строк с новой колонкой 'AgeGroup':")
print(data[['age', 'AgeGroup']].head())
print("\n" + "="*50 + "\n")


# --- Задачи 12-13: Анализ дохода по возрастным группам ---
print("--- 12-13. Количество зарабатывающих >50K по возрастным группам ---")
high_earners_by_age = data[data['salary'] == '>50K']['AgeGroup'].value_counts()
print("Количество зарабатывающих >50K в каждой группе:")
print(high_earners_by_age)
leader_group = high_earners_by_age.idxmax()
print(f"\nВозрастная группа, где больше всего людей с доходом >50K: '{leader_group}'")
print("\n" + "="*50 + "\n")


# --- Задача 14: Фильтрация групп по типу занятости ---
print("--- 14. Фильтрация групп по типу занятости ---")
print("Количество людей в каждой группе занятости (до фильтрации):")
print(data['occupation'].value_counts())

def filter_func(group):
    return group['age'].mean() <= 40 and group['hours-per-week'].min() > 5

filtered_groups = data.groupby('occupation').filter(filter_func)
print("\nКоличество людей в отфильтрованных группах по занятости:")
print(filtered_groups['occupation'].value_counts())
print("\n" + "="*50 + "\n")