# Supabase DAO


> Скрипт реализации Data Access Object для базы данных под управлением supabase-py



## Как использовать

- распаковать локально
- создать venv или подключить существующий
- `pip install -r requirements.txt`
- для инфы по cli `python main.py -h`


## Примеры использования скрипта

### Получение таблиц
Требования: 
- флаг `-t (--table_name)`: вводим имя таблицы, откуда хотим запросить данные, пример - `some_table`
- флаг `-f (--fetch)`: при указании, соберет данные из таблицы. Скрипт вернет Data Transfer Object (DTO) - `Table` 
- опицональный флаг `-csv (--make_csv)`: при указании создаст в корне `some_table.csv`

`python main.py  -t some_table -f` - показать в консоли данные из таблицы `some_table`
`python main.py  -t some_table -f -csv` - показать в консоли данные из таблицы `some_table`, создать файл `some_table.csv` локально

### Загрузка таблиц
Требования:
- флаг `-t (--table_name)`: вводим имя таблицы, куда хотим отправить данные, пример - `some_table`
- флаг `-i (--insert)`: путь до таблицы, которую требуется загрузить

`python main.py  -t some_table -i test_table.csv` - загрузить таблицу `test_table.csv`, лежащую локально в таблицу Supabase `some_table`

### Загрузка картинок

Требования:
- флаг `-u (--upload)`: путь до директории с processed картинками. Скрипт разделяет preview и non-preview, при их равенстве и отсутствии дубликатов в бакете Supabase загружает их в бакет.


 `python main.py -u /home/meatmarshall/work/output/_processed/` - загрузить кейсы из директории в бакет jpg
