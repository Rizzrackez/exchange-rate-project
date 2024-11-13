import requests

from exchange_rate_project.settings import (
    EXCHANGERATE_API_URL,
)


def get_exchange_rate_data() -> dict:
    """Возвращает данные текущего курса
    доллара к рублю и дату последнего обновления."""

    exchange_rate = requests.get(EXCHANGERATE_API_URL)

    # вызываем HTTPError, если с внешним сервисом что-то не так
    exchange_rate.raise_for_status()

    exchange_rate = exchange_rate.json()
    current_usd_rate_data = {
        'time_last_update': exchange_rate['time_last_update_utc'],
        'conversion_rate': exchange_rate['conversion_rate'],
    }

    return current_usd_rate_data
