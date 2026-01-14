# test_import.py
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent))

# Пробуем импортировать auth
try:
    from app.api.v1.auth import router
    print("✅ auth.py импортирован успешно")
    print(" Роутер:", router)
except Exception as e:
    print("❌ Ошибка при импорте auth.py:")
    print(e)
    import traceback
    traceback.print_exc()