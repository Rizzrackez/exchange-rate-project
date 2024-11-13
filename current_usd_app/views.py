from datetime import datetime

from django.http import JsonResponse
from django.core.cache import cache

from .api import get_exchange_rate_data

REQUEST_DELAY = MAX_LATEST_RATES = 10


def get_current_usd(request) -> JsonResponse:
    user_id = request.user.id

    # достаем данные из кэша по id-шнику пользователя
    user_cache_data = cache.get(user_id, {})
    # время последнего запроса к этой ручке
    last_request_time = user_cache_data.get('last_time_request')
    # список последних 10 запросов курсов
    last_users_rates = user_cache_data.get('last_user_rates', [])

    if (
        last_request_time
        and (datetime.now() - last_request_time).seconds < REQUEST_DELAY
    ):
        result = {"message": "too many requests"}
    else:
        current_usd_rate_data = get_exchange_rate_data()

        if len(last_users_rates) > MAX_LATEST_RATES:
            last_users_rates.pop()
        last_users_rates.insert(0, current_usd_rate_data)

        last_request_time = datetime.now()
        cache.set(
            user_id,
            {
                'last_time_request': last_request_time,
                'last_user_rates': last_users_rates,
            }
        )

        result = {
            'current_usd': current_usd_rate_data,
            'latest_user_rates_requests': last_users_rates,
        }

    return JsonResponse(result)
