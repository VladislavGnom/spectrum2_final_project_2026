import os
import sys
import subprocess

def main():
    """Автоматический запуск Django-проекта на Replit."""
    # 1. Применяем миграции при каждом старте
    print("⚙️  Применяю миграции...")
    try:
        subprocess.run([sys.executable, "manage.py", "migrate", "--run-syncdb"], check=True)
        print("✅ Миграции применены.")
    except subprocess.CalledProcessError:
        print("❌ Ошибка миграций. Проверьте базу данных.")
        sys.exit(1)

    # 2. Определяем хост и порт из переменных окружения Replit
    host = '0.0.0.0'  # Обязательно для Replit
    port = int(os.environ.get('PORT', 8000))
    
    print(f"🚀 Запускаю сервер на http://{host}:{port}")
    
    # 3. Запускаем Django-сервер
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robot_zabota.settings')  # ← Замени на имя своего проекта!
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедись, что он установлен и "
            "находится в PYTHONPATH. Активируй виртуальное окружение?"
        ) from exc
        
    execute_from_command_line([sys.argv[0], "runserver", f"{host}:{port}"])

if __name__ == '__main__':
    main()