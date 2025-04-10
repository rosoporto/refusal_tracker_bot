import matplotlib.pyplot as plt
import io
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models import RefusalHistory
import matplotlib.dates as mdates


def generate_analytics_plot(session: Session, user_id: int):
    history = (
        session.query(RefusalHistory.date, func.sum(RefusalHistory.refusals))
        .filter_by(user_id=user_id)
        .group_by(RefusalHistory.date)
        .all()
    )
    if not history:
        return None

    dates, refusals = zip(*history)

    # Создаем график
    plt.figure(figsize=(8, 6))  # Увеличиваем высоту графика
    plt.plot(dates, refusals, marker='o')
    plt.title("Прогресс отказов")
    plt.xlabel("Дата")
    plt.ylabel("Количество отказов")

    # Устанавливаем деления по вертикали с шагом 1
    plt.yticks(range(min(refusals), max(refusals) + 1))

    # Форматируем даты на оси X в формате DD.MM.YY
    date_format = mdates.DateFormatter('%d.%m.%y')
    plt.gca().xaxis.set_major_formatter(date_format)

    # Включаем сетку для лучшей читаемости
    plt.grid(True)

    # Ротация меток оси X для лучшего отображения
    plt.xticks(rotation=45)

    # Автоматическая настройка межметок
    plt.tight_layout()

    # Сохраняем график в буфер
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img