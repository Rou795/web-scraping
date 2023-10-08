import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from parsers import request_parse, selenium_parse

data = {}
all_data = []
all_vacans = []
vac_list = []
schema = 'https://hh.ru/'

url = 'https://hh.ru/search/vacancy'
params = {
    'area': ['1', '2'],
    'text': 'Python, Django, Flask',
    'items_on_page': '20',
    'page': '0'
}
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml',
    'Connection': 'keep-alive'
}

# функция для создания файла с результатами парсинга

def file_maker(all_data, file_name):
    with open(file_name, 'w', encoding='cp1251') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    print(f'{file_name} готов.')

if __name__ == '__main__':
    response = requests.get(url, headers=headers, params=params, timeout=500)
    url_sel = response.url

    # определение кол-ва страниц, которые нужно обойти

    soup = BeautifulSoup(response.text, 'lxml')
    vacancion_nums = int(soup.select_one('h1.bloko-header-section-3').text.split()[0])
    pages = (vacancion_nums // 20)
    if vacancion_nums % 20 != 0:
        pages += 1

# проверка на возможность использования библиотеки requests.
# Суть заключается в том, что мы проверяем кол-во блоков с вакансиями, котоыре может вытянуть requests
# с тем, которое мы ищем (вытягиваем со страницы кол-во результатовпо параметрам поиска)

    for i in tqdm(range(0, pages)):
        params['page'] = str(i)
        response = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        vacans = soup.select('.vacancy-serp-item-body')
        all_vacans.extend(vacans.copy())
#    print(len(all_vacans))
#    print(vacancion_nums)
    if len(all_vacans) < vacancion_nums:
        print('Рекомендуем использовать Selenium. Requests пропустит вакансии')

# Запуск цикла парсинга с помощью Selenium, но он очень долгий(
# Все комментарии написал, пока он работал)

        for i in tqdm(range(0, pages)):
            if i == 0:
                vac_list.extend(selenium_parse(url_sel))
            else:
                url_sel = url_sel.replace(f'&page={i - 1}', f'&page={i}')
                vac_list.extend(selenium_parse(url_sel))
        file_maker(vac_list, 'result_sel.json')
    else:

# париснг с помощью библиотеки requests. Здесь поставил парсинг только на вакансии с USD

        all_data = request_parse(all_vacans)
        file_maker(all_data, 'result_req.json')
