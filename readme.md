# Парсер яндекс карт

Приложение предназначено для сбора данных об организациях размещенных на сайте [https://yandex.ru/maps/](https://yandex.ru/maps/)


##Позволяет собрать данные:
* Ссылка с адресом организации на яндекс картах
* Номер телефона организации, указанный в карточке организации
* Адрес организации
* Сайт организации
* Средний чек
* Рейтинг на картах яндекс
* Количество оценок

Собранные данные сохраняются в xlsx документе в папке содержажей скрипт

 
## Для работы потребуеться 
Установка библиотек в свое виртуальное окружение.
1. Selenium
2. BeautifulSoup4
3. Pandas

```shell
pip install selenium pandas beautifulsoup4
```

 
###Важные опции

Приложение произволить поиск по запросу пользователя, который формируеться переменными
_query_ и _location_ . Так как https://yanex.ru/maps/ сайт с динамически подгружаемым контентом, приложение производит автоматический скролл страницы до тех пор пока не подгрузяться все элементы списка, ограничить количество элементов можно переменной ___count_of_units___, по умолчанию значение переменной 1000. После сбора всех элементов на странице приложение формирует список ссылок, которые дальше парсит на предмет полезных данных, формирует словарь данных и сохраняет его в xlsx формате
 

