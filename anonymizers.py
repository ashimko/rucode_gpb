import pandas as pd
import numpy as np


def replace_names(original_names: pd.DataFrame, fake_names: pd.DataFrame, name_col: str) -> pd.Series:
    # я решил ориентироваться на поле sex в исходных данных при генерации имени определенного рода
    # так как сами имена очень грязные, часто по роду не совпадают имя, отчество и фамилия
    original_names = original_names.copy()
    assert ('sex' in original_names) and ('sex' in fake_names)
    assert set(original_names['sex']) >= set(fake_names['sex'])

    for sex in original_names['sex'].unique():
        orig_mask = original_names['sex'] == sex
        fake_mask = fake_names['sex'] == sex

        sample_fake_names = fake_names.loc[fake_mask, name_col].sample(sum(orig_mask), replace=True).values
        mapping = {orig_name: np.random.choice(sample_fake_names) for orig_name in
                   original_names.loc[orig_mask, name_col].unique()}

        original_names.loc[orig_mask, name_col] = original_names.loc[orig_mask, name_col].map(mapping)

    null_mask = original_names[name_col].isnull()
    if sum(null_mask) > 0:
        original_names[name_col] = original_names[name_col].fillna(fake_names[name_col].sample(sum(null_mask)).values)

    return original_names[name_col]


def replace_geodata(original: pd.Series, fake: pd.Series) -> pd.Series:
    # я решил использовать города и название регионов "как есть".
    # Так как в реальной жизни обычно данные с городом обычно приведены к нормальному виду
    # и нормализация и очистка данных не задача данного контеста

    sample_fake_names = fake.sample(len(original), replace=True).values
    mapping = {orig_name: np.random.choice(sample_fake_names) for orig_name in original.unique()}

    original = original.map(mapping)
    return original


def replace_date(original_dates: pd.Series, date_format='%Y-%m-%d') -> pd.Series:
    # тут необходимо пояснение какие свойства в целом должны оставаться
    # у измененных данных. Я принял решение добавить случайно +- 90 дней к оригинальной дате рождения
    # чтобы сохранить и некоторые общие свойства распределениея дат и в то же время анонимизировать данные

    if not np.issubdtype(original_dates.dtype, np.datetime64):
        original_dates = pd.to_datetime(original_dates, format=date_format)
    return original_dates.apply(lambda x: x + pd.Timedelta(days=np.random.randint(1, 90)))


def snils_generator() -> str:
    def _generate_snils_number() -> np.array:
        return np.random.randint(0, 9, size=9)

    def _get_control_number(sum_: int) -> str:
        if sum_ < 100:
            control_number = str(sum_)
        elif 100 <= sum_ <= 101:
            control_number = '00'
        else:
            raise ValueError('sum_ should be <= 101')
        return control_number

    def _check_snils_number(snils_number: np.array) -> bool:
        first_triple = int(''.join(map(str, snils_number[:3])))
        second_triple = int(''.join(map(str, snils_number[3:6])))
        third_triple = int(''.join(map(str, snils_number[6:9])))
        if first_triple > 1:
            return True
        elif second_triple > 1:
            return True
        elif third_triple > 998:
            return True
        else:
            return False

    snils_number = _generate_snils_number()
    while not _check_snils_number(snils_number):
        snils_number = _generate_snils_number()
    s = sum([i * n for i, n in zip(list(range(1, 10))[::-1], snils_number)])

    while s > 101:
        s = s % 101
    control_number = _get_control_number(s)
    return ''.join(map(str, snils_number)) + control_number


def inn_generator(length=12):
    """
    Генерация ИНН (10 или 12 значный)
    На входе указывается длина номера - 10 или 12.
    Если ничего не указано, будет выбрана случайная длина.
    """
    def _inn_ctrl_summ(nums, type):
        """
        Подсчет контрольной суммы
        """
        inn_ctrl_type = {
            'n2_12': [7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
            'n1_12': [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
            'n1_10': [2, 4, 10, 3, 5, 9, 4, 6, 8],
        }
        n = 0
        l = inn_ctrl_type[type]
        for i in range(0, len(l)):
            n += nums[i] * l[i]
        return n % 11 % 10

    def _rnd(low: int, high: int) -> int:
        return np.random.randint(low, high)

    if not length:
        length = list((10, 12))[_rnd(0, 1)]
    if length not in (10, 12):
        return None
    nums = [
        _rnd(1, 9) if x == 0
        else _rnd(0, 9)
        for x in range(0, 9 if length == 10 else 10)
    ]
    if length == 12:
        n2 = _inn_ctrl_summ(nums, 'n2_12')
        nums.append(n2)
        n1 = _inn_ctrl_summ(nums, 'n1_12')
        nums.append(n1)
    elif length == 10:
        n1 = _inn_ctrl_summ(nums, 'n1_10')
        nums.append(n1)
    return ''.join([str(x) for x in nums])


def number_generator(size=16):
    # так как в условиях задания не описано каким именно образом
    # должны быть сгенерированы номера карт (только упомянут некий внутренний алгоритм)
    # я принял решение сгенерировать номера карт случаным образом
    return ''.join(map(str, np.random.randint(1, 9, size=16)))


def phone_generator():
    return '+79' + ''.join(map(str, np.random.randint(0, 9, size=16)))
