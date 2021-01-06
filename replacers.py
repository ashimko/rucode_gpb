from itertools import combinations_with_replacement
from string import ascii_uppercase
from typing import Union

from utils import load_from_pickle
from anonymizers import *


def replace_data(original: Union[pd.Series, pd.DataFrame], predicted_class: str) -> pd.Series:
    if predicted_class == 'regionname':
        fake = load_from_pickle('./data/catalogs/regions.pkl')
        replaced_data = replace_geodata(original=original, fake=fake)
        return replaced_data
    elif predicted_class == 'regioncode':
        fake = original.drop_duplicates().sample(frac=1.0)
        replaced_data = replace_geodata(original=original, fake=fake)
        return replaced_data
    elif predicted_class == 'countrycode':
        fake = pd.Series([''.join(combination) for combination in combinations_with_replacement(ascii_uppercase, 2)])
        replaced_data = replace_geodata(original=original, fake=fake)
        return replaced_data
    elif predicted_class == 'street':
        fake = pd.Series(data=load_from_pickle('./data/catalogs/streets.pkl'), name='street')
        replaced_data = replace_geodata(original=original, fake=fake)
        return replaced_data
    elif predicted_class == 'house':
        fake = load_from_pickle('./data/catalogs/houses.pkl')
        replaced_data = replace_geodata(original=original, fake=fake)
        return replaced_data
    elif predicted_class in ['opendate', 'appdatetime', 'signdate', 'birthdate', 'issuedate']:
        replaced_data = replace_date(original_dates=original)
        return replaced_data
    elif predicted_class == 'card_number':
        fake = [number_generator(16) for _ in range(len(original))]
        replaced_data = pd.Series(data=fake, name=original.name, index=original.index)
        return replaced_data
    elif predicted_class == 'client_snils':
        fake = [snils_generator() for _ in range(len(original))]
        replaced_data = pd.Series(data=fake, name=original.name, index=original.index)
        return replaced_data
    elif predicted_class == ['client_inn', 'inn']:
        fake = [inn_generator() for _ in range(len(original))]
        replaced_data = pd.Series(data=fake, name=original.name, index=original.index)
        return replaced_data
    elif predicted_class == 'lastname':
        fake = load_from_pickle('./data/catalogs/surnames.pkl')
        replaced_data = replace_names(original, fake, 'lastname')
        return replaced_data
    elif predicted_class == 'firstname':
        fake = load_from_pickle('./data/catalogs/names.pkl')
        replaced_data = replace_names(original, fake, 'firstname')
        return replaced_data
    elif predicted_class == 'middlename':
        fake = load_from_pickle('./data/catalogs/middlenames.pkl')
        replaced_data = replace_names(original, fake, 'middlename')
        return replaced_data
    elif predicted_class == 'birthplacetown':
        fake = load_from_pickle('./data/catalogs/cities.pkl')
        replaced_data = replace_geodata(original, fake)
        return replaced_data
    elif predicted_class == 'series':
        fake = [number_generator(4) for _ in range(len(original))]
        replaced_data = pd.Series(data=fake, name=original.name, index=original.index)
        return replaced_data
    elif predicted_class in ['number', 'issuercode']:
        fake = [number_generator(6) for _ in range(len(original))]
        replaced_data = pd.Series(data=fake, name=original.name, index=original.index)
        return replaced_data
    elif predicted_class == 'issuer':
        fake = original.drop_duplicates()
        replaced_data = pd.Series(data=fake, name=original.name, index=original.index)
        return replaced_data
    elif predicted_class == 'phone_number':
        fake = [phone_generator() for _ in range(len(original))]
        replaced_data = pd.Series(data=fake, name=original.name, index=original.index)
        return replaced_data
    elif predicted_class == 'title':
        fake = pd.Series([''.join(combination) for combination in combinations_with_replacement(ascii_uppercase, 2)])
        fake = 'ООО ' + fake
        replaced_data = pd.Series(data=fake, name=original.name, index=original.index)
        return replaced_data
    else:
        return original
