import pandas as pd

# Работа с БД
# !!! Товарная группа и название полностью определяют поставщика и цену !!!
GOODS1 = pd.DataFrame({"назв": ['яблоки', 'бананы', 'сыр'],
                       "тг": ['фрукты', 'фрукты', 'молочные продукты'],
                       "код_пост": ['10', '20', '10'], "цена": [100, 50, 500]})
GOODS1 = GOODS1.astype({"назв": str, "тг": str, "код_пост": str, "цена": float})
GOODS2 = pd.DataFrame({"назв": ['виноград', 'кефир', 'ананасы'],
                       "тг": ['фрукты', 'молочные продукты', 'фрукты'],
                       "код_пост": ['10', '10', '20'], "цена": [200, 70, 150]})
GOODS2 = GOODS2.astype({"назв": str, "тг": str, "код_пост": str, "цена": float})

GOODSadd = pd.Series(['арбузы', 'фрукты', '20', 65],
                     index=['назв', 'тг', 'код_пост', 'цена'])

SUPL = pd.DataFrame({"код_пост": ['10', '20'],
                     "пост_назв": ['Рога и Копыта', 'Парнас'],
                     "область": ['Тверская', 'Воронежская'],
                     "наценка": [15, 10]})

MANAG1 = pd.DataFrame({"имя": ['Петя', 'Вася', 'Петя', 'Коля'],
                       "офис": ['1', '2', '2', '1']})
MANAG2 = pd.DataFrame({"имя": ['Петя', 'Вася', 'Петя'],
                       "офис": ['1', '2', '2']})

# Объединение баз товаров

# Добавить - append, удалить - drop(значение индекса)
GOODS1w = pd.concat([GOODS1, GOODSadd], ignore_index=True)
gd1w = GOODS1w.drop('тг', axis=1)

GOODS1w = GOODS1w.astype({"назв": str, "тг": str, "код_пост": str, "цена": float})
# Горизонтальное
# join=inner - пересечение, outer - объединение
GOODS1ext = pd.concat([GOODS1w, MANAG1], axis=1, join="outer")
GOODS2ext = pd.concat([GOODS2, MANAG2], axis=1)
# Вертикальное 
# join=inner - пересечение, outer - объединение
GOODS = pd.concat([GOODS1ext, GOODS2ext], axis=0, ignore_index=True)
# Слияние двух справочников
GOODSfull = pd.merge(GOODS, SUPL, on="код_пост")

supl1 = SUPL.rename({'код_пост': 'ID'}, axis=1)
GOODSfull0 = pd.merge(GOODS, supl1, left_on='код_пост', right_on='ID')
GOODSfull0.drop('ID', axis=1, inplace=True)

# *************** Отчеты **********************
# Текстовый: Фрукты из Тверской области - название и цена
# Название отчета вводится или выбирается в интерфейсе
SEL = (GOODSfull["тг"] == "фрукты") & (GOODSfull["область"] == "Тверская")
W1 = GOODSfull.loc[SEL, ["назв", "цена"]]
W1.loc[2, "цена"] = 250
PTH1 = "./output/фрукты_тверь.xlsx"
W1.to_excel(PTH1, index=False)


def selection(dataframe, params):
    def find_col(dataframe, param):
        for column in dataframe.columns:
            if param in dataframe[column].value_counts().keys().astype(str):
                return column

    used_col = {}
    SELECT = pd.Series()
    for column in dataframe.columns:
        used_col[column] = False
    for param in params:
        logic_siqn = ''
        parsed_param = param.split('==')
        if parsed_param[0][0] == '+':
            logic_siqn = parsed_param[0][0]
            param_name = parsed_param[0][1:]
        else:
            param_name = parsed_param[0]
        param_value = parsed_param[1]
        if len(parsed_param) == 2:
            col = find_col(dataframe, param_value)
            if SELECT.empty:
                SELECT = dataframe[param_name].astype(str) == param_value
                print("Done")
            elif used_col[col] or logic_siqn == '+':
                SELECT += dataframe[param_name].astype(str) == param_value
            else:
                SELECT *= dataframe[param_name].astype(str) == param_value
                used_col[col] = True
        print(SELECT)
    PTH = "./output/report.xlsx"
    dataframe.loc[SELECT, ["назв", "цена"]].to_excel(PTH, index=False)
    return dataframe.loc[SELECT, ["назв", "цена"]]


print(selection(GOODSfull, ['цена==100.0', '+назв==ананасы']))
