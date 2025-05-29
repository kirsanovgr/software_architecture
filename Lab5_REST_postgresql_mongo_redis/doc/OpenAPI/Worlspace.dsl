workspace {
    name "Система управления задачами и целями"
    description "Микросервисная архитектура для управления пользователями, задачами и целями с использованием PostgreSQL, MongoDB и Redis"

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
                redisCache = component "Redis кэш" "Обеспечивает сквозное чтение и сквозную запись данных пользователей" "Redis"
            }
            
            // Контейнер сервиса задач и целей
            goalTaskService = container "Сервис задач и целей" "Управляет задачами и целями пользователей" "Python, FastAPI" {
                goalTaskController = component "API контроллер" "Обрабатывает HTTP запросы" "FastAPI Router"
                goalService = component "Сервис целей" "Реализует бизнес-логику для управления целями" "Python"
                taskService = component "Сервис задач" "Реализует бизнес-логику для управления задачами" "Python"
                fileService = component "Сервис файлов" "Управляет загрузкой и хранением файлов" "Python"
                goalRepository = component "Репозиторий целей" "Хранит и извлекает данные целей" "Python, SQLAlchemy"
                taskRepository = component "Репозиторий задач" "Хранит и извлекает данные задач" "Python, SQLAlchemy"
                fileRepository = component "Репозиторий файлов" "Управляет хранением файлов в MongoDB" "Python, PyMongo"
                taskPostgresDB = component "PostgreSQL база данных" "Хранит метаданные задач и целей" "PostgreSQL 14"
                filesMongoDB = component "MongoDB база данных" "Хранит файлы задач (изображения, текстовые и офисные документы)" "MongoDB"
            }
            
            // Отношения между компонентами сервиса пользователей
            userController -> userServiceComponent "Использует"
            userServiceComponent -> passwordService "Использует для хеширования паролей"
            userServiceComponent -> userRepository "Использует для доступа к данным"
            userRepository -> userPostgresDB "Читает и записывает данные пользователей"
            userRepository -> redisCache "Использует для кэширования данных (сквозное чтение и запись)"
            
            // Отношения между компонентами сервиса задач и целей
            goalTaskController -> goalService "Использует для управления целями"
            goalTaskController -> taskService "Использует для управления задачами"
            goalService -> goalRepository "Использует для доступа к данным целей"
            taskService -> taskRepository "Использует для доступа к данным задач"
            taskService -> fileService "Использует для управления файлами задач"
            fileService -> fileRepository "Использует для доступа к файлам"
            goalRepository -> taskPostgresDB "Читает и записывает данные целей"
            taskRepository -> taskPostgresDB "Читает и записывает данные задач"
            fileRepository -> filesMongoDB "Читает и записывает файлы (изображения, текст, документы)"
            
            // Отношения между контейнерами
            goalTaskService -> userService "Проверяет аутентификацию пользователей"
        }
        
        // Отношения между пользователем и системой
        user -> taskManagementSystem "Использует для управления задачами и целями"
    }
    
    views {
        systemContext taskManagementSystem {
            include *
            autoLayout
        }
        
        container taskManagementSystem {
            include *
            autoLayout
        }
        
        component userService {
            include *
            autoLayout
        }
        
        component goalTaskService {
            include *
            autoLayout
        }
        
        theme default
    }
}