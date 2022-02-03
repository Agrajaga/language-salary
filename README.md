# Programming vacancies compare

This is a simple script for comparing the average salaries of developers in various programming languages.  
The following programming languages participate in the sample: `Python, JavaScript, Java, Ruby, PHP, C++, C#, Go, Scala, Swift, 1С`.   
Salary amounts are taken from vacancies on websites [hh.ru](https://hh.ru) and [superjob.ru](https://www.superjob.ru).

### How to run

To run the script, type:
```
$ python salary.py
```
You will get the results in the form of tables
```
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 3683             | 657                 | 233220           |
| JavaScript            | 4803             | 1053                | 194072           |
| Java                  | 3904             | 556                 | 256920           |
| Ruby                  | 314              | 110                 | 248166           |
| PHP                   | 1973             | 973                 | 179818           |
| C++                   | 1886             | 585                 | 207057           |
| C#                    | 2029             | 603                 | 204516           |
| Go                    | 1145             | 276                 | 256088           |
| Scala                 | 277              | 58                  | 289728           |
| Swift                 | 709              | 221                 | 256527           |
| 1С                    | 3793             | 976                 | 155150           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 75               | 51                  | 144721           |
| JavaScript            | 98               | 79                  | 139733           |
| Java                  | 44               | 31                  | 196270           |
| Ruby                  | 6                | 6                   | 154833           |
| PHP                   | 63               | 49                  | 148805           |
| C++                   | 45               | 31                  | 165693           |
| C#                    | 40               | 27                  | 173629           |
| Go                    | 16               | 13                  | 218984           |
| Scala                 | 1                | 1                   | 240000           |
| Swift                 | 7                | 3                   | 221666           |
| 1С                    | 89               | 66                  | 154177           |
+-----------------------+------------------+---------------------+------------------+
```

### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
To use the API SuperJob.ru, you need to [register the application](https://api.superjob.ru/register) and get the `Secret key`.
_When registering the application, you will be required to specify the site. Enter any, they don't check._  
Create a file `.env` and put your `Secret key` in it:
```
SJ_API_TOKEN=<your_secret_key>
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).