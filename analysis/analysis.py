import pandas as pd

# Путь к файлу
file_path = "user_behavior_analysis.xlsx"

# Чтение данных из Excel
df = pd.read_excel(file_path, sheet_name='Sheet1')


# Убираем пустые строки и значения NaN
df.dropna(how='all', inplace=True)

# Анализ действий пользователей
action_counts = df['Action After Response'].value_counts()
manual_copy_data = df[df['Action After Response'] == 'Manual Copy']

# Подсчет количества Manual Copy на пользователя
manual_copy_per_user = manual_copy_data.groupby('User ID').size()

# Средняя длина ответа при Manual Copy
avg_response_length_manual_copy = manual_copy_data['Response Length'].mean()

# Результаты анализа
print("=== АНАЛИЗ ПОЛЬЗОВАТЕЛЬСКИХ ДЕЙСТВИЙ ===\n")

print("Частота действий после ответа:")
for action, count in action_counts.items():
    print(f"- {action}: {count} раз")

print("\nКоличество действий 'Manual Copy' на пользователя:")
for user, count in manual_copy_per_user.items():
    print(f"- {user}: {count} раз(а)")

print(f"\nСредняя длина ответа при выборе 'Manual Copy': {avg_response_length_manual_copy:.2f} символов")

# Вывод рекомендации
if 'Manual Copy' in action_counts and action_counts['Manual Copy'] > 0:
    print("\nРЕКОМЕНДАЦИЯ:")
    print("Добавление кнопки 'Копировать в буфер обмена' оправдано, так как пользователи часто используют ручное копирование.")
else:
    print("\nРЕКОМЕНДАЦИЯ:")
    print("Добавление кнопки 'Копировать в буфер обмена' пока не оправдано — действия 'Manual Copy' слишком мало.")