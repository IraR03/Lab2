import requests
from bs4 import BeautifulSoup



# Процедура получения цены
def get_number(product):
#    price_tag = product.find('p', class_='price')
    price_text = product.get_text(strip=True).split('a')
    if len(price_text) > 2:
        return price_text[1]
    else:
        return price_text[0].replace('\xa0','')



if __name__ == '__main__':
    # Получить 5 товаров из рекомендуемых и 5 из хитов продаж и вывести в один файл
    # отделяя друг от друга. Должно быть название, текущая цена и ссылка на товар
    link = 'https://www.proficosmetics.ru'

    # Отправляем GET-запрос на сайт
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup:
        # Получаем Рекомендуемые товары
        recommended_products = soup.find_all('div', class_='products_slider')[0]

        # Получаем Хиты продаж
        bestsellers = soup.find_all('div', class_='products_slider')[1]
        # Открываем файл для записи
        with open('output.txt', 'w', encoding='utf-8') as file:
            count_cards = 0
            file.write('Рекомендуемые товары:\n')
            for product in recommended_products.find_all('div', class_='tumb'):
                if product and count_cards < 5:
                    count_cards += 1
                    n = product.find('h5', class_='kr_brand_name')
                    name = n.find('a').text.strip()
                    llink = link + n.find('a')['href']
                    pr = product.find('p', class_='price')
                    price = get_number(pr)
                    file.write(f'Название: {name}\n')
                    file.write(f'Цена: {price} руб.\n')
                    file.write(f'Ссылка: {llink}\n\n')

        with open('output.txt', 'a', encoding='utf-8') as file:
            count_cards = 0
            file.write('Хиты продаж:\n')
            hit_sale = bestsellers.find_all('div', class_='tumb')
            for product in hit_sale:
                if product and count_cards < 5:
                    count_cards += 1
                    n = product.find('h5', class_='kr_brand_name')
                    name = n.find('a').text.strip()
                    llink = link + n.find('a')['href']
                    pr = product.find('p', class_='price')
                    price = get_number(pr)
                    file.write(f'Название: {name}\n')
                    file.write(f'Цена: {price} руб.\n')
                    file.write(f'Ссылка: {llink}\n\n')


        f = open('output.txt', 'r', encoding='utf-8')
        print(*f)
