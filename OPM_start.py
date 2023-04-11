import time
from numpy import corrcoef, isnan
from tradingview_ta import TA_Handler, Interval


MAIN_PAIR = 'ETHUSDT29U2023'
AFFECTING_PAIR = 'BTCUSDT'
PROVIDER = 'OKX'
INTERVAL = 60 # Интревал в секундах между запросами цен
DATA_LENGHT = 30 # Количество хранимых таймфреймов
CC_LENGTH = 20 # Количество таймфреймов для расчета коэффициента корреляции

def check_diff_sign(num0: float, num1: float) -> bool:
    """
    Проверяет, имеют ли числа разный знак.
    Возвращает истину, если знак разный. При сравнении с 0.0 так же возвращает истину.
    """
    return False if num0 * num1 > 0.0 else True

def normalize_cc(cc: float) -> float:
    """
    Нормализует коэффициент корреляции.
    """
    if isnan(cc):
        cc = 1.0
    if cc <= 0.0:
        cc = 0.001
    return cc
    

main_pair = TA_Handler(
    symbol = MAIN_PAIR,
    screener = 'crypto',
    exchange = PROVIDER,
    interval = Interval.INTERVAL_1_MINUTE
)

affecting_pair = TA_Handler(
    symbol = AFFECTING_PAIR,
    screener = 'crypto',
    exchange = PROVIDER,
    interval = Interval.INTERVAL_1_MINUTE
)

last_main_prices = [] # Список цен основного инструмента за указанный период.
last_affecting_prices = [] # Список цен оказывающего влияние инструмента за указанный период.
ch_main_prices = [] # Список изменений цен основного инструмента за указанный период.
ch_affecting_prices = [] # Список изменений цен оказывающего влияние инструмента за указанный период.
corr_ch_main_prices = [] # Список скорректированных цен основного инструмента за указанный период.

if __name__ == '__main__':
    
    while True:
        time.sleep(INTERVAL)
        cc = 1.0 # Коэффициент корреляции

        main_pair_price = main_pair.get_indicators(['close']).get('close')
        affecting_pair_price = affecting_pair.get_indicators(['close']).get('close')

        last_main_prices.append(main_pair_price)
        if len(last_main_prices) >= DATA_LENGHT + 1:
            last_main_prices.pop(0)

        last_affecting_prices.append(affecting_pair_price)
        if len(last_affecting_prices) >= DATA_LENGHT + 1:
            last_affecting_prices.pop(0)

        if len(last_main_prices) >= 2 and len(last_affecting_prices) >= 2:
            
            if len(last_main_prices) >= 20 and len(last_affecting_prices) >= 20:
                cc = normalize_cc(corrcoef(last_main_prices[-CC_LENGTH:], last_affecting_prices[-CC_LENGTH:])[0, 1])
                

            if len(last_main_prices) >= 2:
                ch_main_prices.append(last_main_prices[-1] / last_main_prices[-2] - 1)
            if len(ch_main_prices) >= DATA_LENGHT:
                ch_main_prices.pop(0)

            if len(last_affecting_prices) >= 2:
                ch_affecting_prices.append(last_affecting_prices[-1] / last_affecting_prices[-2] - 1)
            if len(ch_affecting_prices) >= DATA_LENGHT:
                ch_affecting_prices.pop(0)


            if check_diff_sign(ch_main_prices[-1], ch_affecting_prices[-1]) or ch_main_prices == ch_affecting_prices == 0.0 or cc < 0.01 :
                corr_ch_main_prices.append(ch_main_prices[-1])
            elif abs(ch_main_prices[-1]) > abs(ch_affecting_prices[-1]):
                if ch_main_prices[-1] > 0:
                    ch = ch_main_prices[-1] - (ch_affecting_prices[-1] * cc)
                elif ch_main_prices[-1] < 0:
                    ch = ch_main_prices[-1] + (ch_affecting_prices[-1] * cc)
                corr_ch_main_prices.append(ch)
            else:
                corr_ch_main_prices.append(0.0)


            if max(corr_ch_main_prices) >= 0.01 or min(corr_ch_main_prices) <= -0.01:
                print("Price change over than 1%")
                
            if len(corr_ch_main_prices) >= DATA_LENGHT:
                corr_ch_main_prices.pop(0)
