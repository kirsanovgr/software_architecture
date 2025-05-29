workspace {
    name "Система управления задачами и целями"
    description "Микросервисная архитектура для управления пользователями, задачами и целями"

    model {
        user = person "Пользователь" "Человек, использующий систему для управления задачами и целями"
        
        taskManagementSystem = softwareSystem "Система управления задачами" "Позволяет пользователям создавать и управлять задачами и целями" {
            // Контейнер сервиса пользователей
            userService = container "Сервис пользователей" "Управляет пользователями, аутентификацией и авторизацией" "Python, FastAPI" {
                userController = component "API контроллер" "Обрабатывает HTTP запросы" "FastAPI Router"
                userServiceComponent = component "Сервис пользователей" "Реализует бизнес-логику для управления пользователями" "Python"
                passwordService = component "Сервис паролей" "Управляет хешированием и проверки паролей" "Python"
                userRepository = component "Репозиторий пользователей" "Хранит и извлекает данные пользователей" "Python"
                userMemoryDB = component "In-Memory хранилище" "Хранит данные пользователей в памяти" "Python List"
            }
            
            // Контейнер сервиса задач и целей
            goalTaskService = container "Сервис задач и целей" "Управляет задачами и целями пользователей" "Python, FastAPI" {
                goalTaskController = component "API контроллер" "Обрабатывает HTTP запросы" "FastAPI Router"
                goalService = component "Сервис целей" "Реализует бизнес-логику для управления целями" "Python"
                taskService = component "Сервис задач" "Реализует бизнес-логику для управления задачами" "Python"
                goalRepository = component "Репозиторий целей" "Хранит и извлекает данные целей" "Python"
                taskRepository = component "Репозиторий задач" "Хранит и извлекает данные задач" "Python"
                goalTaskMemoryDB = component "In-Memory хранилище" "Хранит данные задач и целей в памяти" "Python List"
                authClient = component "Клиент аутентификации" "Проверяет токены пользователей через сервис пользователей" "Python"
            }
        }
        
        // Отношения на уровне персон и систем
        user -> taskManagementSystem "Использует"
        
        // Отношения на уровне контейнеров
        user -> userService "Регистрируется, входит в систему и управляет профилем" "HTTP/JSON"
        user -> goalTaskService "Создает и управляет задачами и целями" "HTTP/JSON"
        goalTaskService -> userService "Проверяет аутентификацию пользователя" "HTTP/JSON"
        // Добавляем самоссылку для сервиса задач и целей
        goalTaskService -> goalTaskService "Внутренняя обработка" "Внутренний вызов"
        
        // Отношения на уровне компонентов в сервисе пользователей
        userController -> userServiceComponent "Использует"
        userServiceComponent -> passwordService "Использует для хеширования и проверки паролей"
        userServiceComponent -> userRepository "Использует для доступа к данным"
        userRepository -> userMemoryDB "Читает и записывает данные"
        
        // Отношения на уровне компонентов в сервисе задач и целей
        goalTaskController -> goalService "Использует для управления целями"
        goalTaskController -> taskService "Использует для управления задачами"
        goalService -> goalRepository "Использует для доступа к данным"
        taskService -> taskRepository "Использует для доступа к данным"
        goalRepository -> goalTaskMemoryDB "Читает и записывает данные"
        taskRepository -> goalTaskMemoryDB "Читает и записывает данные"
        goalTaskController -> authClient "Проверяет токены"
        authClient -> userService "Запрашивает проверку токена" "HTTP/JSON"
    }
    
    views {
        systemContext taskManagementSystem "SystemContext" {
            include *
            autoLayout
        }
        
        container taskManagementSystem "Containers" {
            include *
            autoLayout
        }
        
        component userService "UserServiceComponents" {
            include *
            autoLayout
        }
        
        component goalTaskService "GoalTaskServiceComponents" {
            include *
            autoLayout
        }
        
        dynamic taskManagementSystem "CreateTask" "Процесс создания новой задачи пользователем" {
            user -> userService "1. Аутентифицируется с логином и паролем"
            userService -> user "2. Возвращает токен доступа"
            user -> goalTaskService "3. Отправляет запрос на создание задачи с токеном"
            goalTaskService -> userService "4. Проверяет токен пользователя"
            userService -> goalTaskService "5. Подтверждает валидность токена"
            goalTaskService -> goalTaskService "6. Создает новую задачу"
            goalTaskService -> user "7. Возвращает созданную задачу"
            autoLayout
        }
        
        theme default
        
        styles {
            element "Person" {
                shape Person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Component" {
                background #85BBF0
                color #000000
            }
        }
    }
}