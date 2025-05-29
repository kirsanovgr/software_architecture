workspace {
    name "Система управления задачами и целями"
    description "Микросервисная архитектура для управления пользователями, задачами и целями с использованием PostgreSQL"

    model {
        user = person "Пользователь" "Человек, использующий систему для управления задачами и целями"
        
        taskManagementSystem = softwareSystem "Система управления задачами" "Позволяет пользователям создавать и управлять задачами и целями" {
            // Контейнер сервиса пользователей
            userService = container "Сервис пользователей" "Управляет пользователями, аутентификацией и авторизацией" "Python, FastAPI" {
                userController = component "API контроллер" "Обрабатывает HTTP запросы" "FastAPI Router"
                userServiceComponent = component "Сервис пользователей" "Реализует бизнес-логику для управления пользователями" "Python"
                passwordService = component "Сервис паролей" "Управляет хешированием и проверки паролей" "Python"
                userRepository = component "Репозиторий пользователей" "Хранит и извлекает данные пользователей" "Python, SQLAlchemy"
                userPostgresDB = component "PostgreSQL база данных" "Хранит данные пользователей в PostgreSQL" "PostgreSQL 14"
            }
            
            // Контейнер сервиса задач и целей
            goalTaskService = container "Сервис задач и целей" "Управляет задачами и целями пользователей" "Python, FastAPI" {
                goalTaskController = component "API контроллер" "Обрабатывает HTTP запросы" "FastAPI Router"
                goalService = component "Сервис целей" "Реализует бизнес-логику для управления целями" "Python"
                taskService = component "Сервис задач" "Реализует бизнес-логику для управления задачами" "Python"
                goalRepository = component "Репозиторий целей" "Хранит и извлекает данные целей" "Python, SQLAlchemy"
                taskRepository = component "Репозиторий задач" "Хранит и извлекает данные задач" "Python, SQLAlchemy"
                goalTaskPostgresDB = component "PostgreSQL база данных" "Хранит данные задач и целей в PostgreSQL" "PostgreSQL 14"
                authClient = component "Клиент аутентификации" "Проверяет токены пользователей через сервис пользователей" "Python"
            }
        }
        
        // Отношения на уровне персон и систем
        user -> taskManagementSystem "Использует"
        
        // Отношения между компонентами сервиса пользователей
        userController -> userServiceComponent "Вызывает"
        userServiceComponent -> passwordService "Использует для хеширования паролей"
        userServiceComponent -> userRepository "Использует для доступа к данным"
        userRepository -> userPostgresDB "Читает и записывает данные пользователей"
        
        // Отношения между компонентами сервиса задач и целей
        goalTaskController -> goalService "Вызывает для управления целями"
        goalTaskController -> taskService "Вызывает для управления задачами"
        goalService -> goalRepository "Использует для доступа к данным целей"
        taskService -> taskRepository "Использует для доступа к данным задач"
        goalRepository -> goalTaskPostgresDB "Читает и записывает данные целей"
        taskRepository -> goalTaskPostgresDB "Читает и записывает данные задач"
        goalTaskController -> authClient "Использует для проверки аутентификации"
        authClient -> userService "Запрашивает проверку токенов"
    }
}