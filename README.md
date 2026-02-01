# Swag Labs — Автоматизация тестирования авторизации

## Описание
Автоматизированы проверки функционала авторизации на сайте [https://www.saucedemo.com/](https://www.saucedemo.com/) с использованием Python и Selenium.

Реализовано **7 тест-кейсов**:
- **5 обязательных из ТЗ**:
  - Успешный вход (`standard_user`)
  - Вход с неверным паролем
  - Вход заблокированным пользователем (`locked_out_user`)
  - Вход с пустыми полями
  - Вход пользователя с задержками (`performance_glitch_user`)
- **2 дополнительных**:
  - Проверка наличия UI-элементов на странице логина  
  - Вход с несуществующим именем пользователя  

Дополнительные тесты добавлены для повышения надёжности: первый подтверждает корректную загрузку интерфейса перед выполнением сценариев, второй обеспечивает полноту валидации обработки ошибок при работе с несуществующими учётными записями.

## Технологии
- **Python 3.10** — язык реализации  
- **pytest** — фреймворк для запуска тестов  
- **Selenium WebDriver** — управление браузером  
- **webdriver-manager** — автоматическая загрузка драйверов  
- **Page Object Model** — архитектура тестов  
- **Allure Framework** — генерация отчётов  
- **Docker** — контейнеризация запуска  

## Структура проекта
```
swaglabs_tests/
├── Dockerfile
├── requirements.txt
└── src/
    ├── pages/          # Page Objects
    └── tests/          # Тестовые сценарии
```

## Запуск через Docker

1. **Сборка образа**  
   ```powershell
   docker build -t swaglabs-tests .
   ```

2. **Запуск тестов**  
   ```powershell
   Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue
   docker run --rm -v ${PWD}:/app swaglabs-tests
   ```

3. **Генерация отчёта**  
   ```powershell
   Remove-Item -Recurse -Force allure-report -ErrorAction SilentlyContinue
   docker run --rm -v ${PWD}/allure-results:/app/allure-results -v ${PWD}:/output frankescobar/allure-docker-service allure generate /app/allure-results -o /output/allure-report --clean
   ```

4. **Просмотр отчёта**  
   ```powershell
   docker run -d -p 5050:80 -v ${PWD}/allure-report:/usr/share/nginx/html --name allure-report nginx
   Start-Process "http://localhost:5050"
   ```

5. **Очистка**  
   ```powershell
   docker stop allure-report
   docker rm allure-report
   Remove-Item -Recurse -Force allure-results, allure-report
   ```

## Особенности реализации

- **Page Object Model**: логика взаимодействия с UI вынесена в отдельные классы (`LoginPage`, `InventoryPage`), что упрощает поддержку.
- **Скриншоты до и после**: для каждого критичного действия (ввод данных, нажатие кнопки) добавлены скриншоты в Allure-отчёт, что позволяет визуально подтвердить состояние приложения.
- **Точная валидация**: проверяются как корректность URL, так и наличие ключевых элементов на странице.
- **Замер времени**: для `performance_glitch_user` фиксируется время выполнения операции, что помогает отслеживать производительность.
- **Изоляция через Docker**: проект полностью упакован в контейнер, что гарантирует воспроизводимость запуска на любой машине.

## Зависимости
Указаны в `requirements.txt`:
- selenium==4.15.2
- pytest==7.4.3
- allure-pytest==2.13.2
- webdriver-manager==4.0.2
- python-dotenv==1.0.0
