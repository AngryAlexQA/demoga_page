[![Python UI Tests](https://github.com/AngryAlexQA/demoga_page/actions/workflows/python-app.yml/badge.svg)](https://github.com/AngryAlexQA/demoga_page/actions/workflows/python-app.yml)
[![pages-build-deployment](https://github.com/AngryAlexQA/demoga_page/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/AngryAlexQA/demoga_page/actions/workflows/pages/pages-build-deployment)
# DemoQA Home Project_7_hw

Проект для автоматизации тестирования демо-сайта demoqa.com.

### Запуск всех тестов
```
pytest tests/test_check_text.py -v --alluredir=allure-results
```

### Запуск конкретного теста
```
pytest tests/test_check_text.py::test_check_footer_text -v --alluredir=allure-results
pytest tests/test_check_text.py::test_check_center_text_after_navigation -v --alluredir=allure-results
```

### Запуск с повторными попытками для упавших тестов
```
pytest tests/test_check_text.py -v --alluredir=allure-results --reruns 2 --reruns-delay 1
```

### Просмотр отчета
```
allure serve allure-results
```

