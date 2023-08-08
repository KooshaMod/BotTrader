from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from statistics import variance, mean, stdev
from math import sqrt


def get_diff(prices, config):
    """
    accept a list, each item is a dict with price_datetime,current_price and future_price keys
    """
    prices_diff = [(x.get('future_price') - x.get('current_price')) for x in prices]
    if (prices_diff[len(prices_diff) - 1] > mean(prices_diff[:-1]) + (
            config.get('variance_dis') * sqrt(variance(prices_diff[:-1])))
            or prices_diff[len(prices_diff) - 1] < mean(prices_diff[:-1]) - (config.get('variance_dis') *
                                                                        sqrt(variance(prices_diff[:-1])))):
        return True
    return False


@api_view(['POST'])
def make_decision(request):
    """
    Accept a post request the input should be like below
    {"prices" :
        [
            {"price_datetime": time of the given price (datetime timestamp),
            "current_price": price of the asset now (int),
            "future_price": price of the future contract of the asset (int)
            }
        ],
    "timeframe": the time frame of each candle (1m,5m,30m,1h,4h,daily,monthly,yearly)
        }
    """
    data = request.data
    prices = data.get('prices')
    timeframe = data.get('timeframe', 'daily')
    CONFIG = {'variance_dis': 3}
    return JsonResponse({'result': get_diff(prices, CONFIG)})
