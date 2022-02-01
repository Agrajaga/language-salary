# Programming vacancies compare

This is a simple script for comparing the average salaries of developers in various programming languages.  
The following programming languages participate in the sample: `Python, JavaScript, Java, Ruby, PHP, C++, C#, Go, Scala, Swift, 1С`.   
Salary amounts are taken from vacancies on websites [hh.ru](https://hh.ru) and [superjob.ru](https://www.superjob.ru).

### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
To use the API SuperJob.ru, you need to [register the application](https://api.superjob.ru/register) and get the Secret key.
_When registering the application, you will be required to specify the site. Enter any, they don't check._
Create a file `.env` and put your `Secret key` in it.
```
SJ_API_TOKEN=<your_secret_key>
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).