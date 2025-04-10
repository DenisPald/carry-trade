import yfinance as yf
import pandas as pd

def get_interest_rate(country, file_path="bis_dp.csv"):
    """
    Получает годовую процентную ставку из CSV-файла.
    """
    try:
        # Пропуск первых 4 строк с метаданными
        df = pd.read_csv(file_path, skiprows=4)

        df_filtered = df[df["REF_AREA:Reference area"] == country]
        
        if df_filtered.empty:
            print(f"Не найдены данные для страны: {country}")
            return None

        latest_row = df_filtered.iloc[-1]
        
        rate = float(latest_row["OBS_VALUE:Value"])
        return rate/100 # Преобразование процента в десятичную дробь

    except Exception as e:
        print(f"Ошибка при получении ставки из файла: {e}")
        return None

def get_exchange_rate(ticker):
    """
    Получает текущий обменный курс через yfinance.
    ticker: тикер валютной пары (например, USDTRY=X)
    """
    try:
        data = yf.Ticker(ticker)
        # Получаем последний доступный курс
        rate = data.history(period='1d')['Close'].iloc[-1]
        return rate
    except Exception as e:
        print(f"Ошибка при получении курса: {e}")
        return None

def calculate_profit():
    """
    Рассчитывает прибыль для сделки США (кредит) → Турция (депозит) → США (вывод).
    """
    # Ввод данных пользователем
    S = float(input("Введите начальную сумму кредита в USD (S): "))
    c_i = float(input("Введите комиссию при переводе в Турцию (%): ")) / 100
    c_o = float(input("Введите комиссию при выводе обратно в США (%): ")) / 100
    t = float(input("Введите продолжительность вложения (лет): "))
    k2 = float(input("Введите прогнозируемый обменный курс USD/TRY на момент вывода (k2): "))
    
    r_c = get_interest_rate("US:United States") # Ставка по США
    r_d = get_interest_rate("TR:Türkiye") # Ставка по Турции 
    k1 = get_exchange_rate("USDTRY=X") # Текущий курс USD/TRY
    
    if None in (r_c, r_d, k1):
        print("Не удалось получить данные.")
        return
    
    # Расчет прибыли по формуле
    numerator = (S - S * c_i) * k1 * (1 + r_d * t) * (1 - c_o)
    P = (numerator / k2) - S * (1 - r_c * t)
    
    # Вывод результатов
    print("\nРезультаты расчета:")
    print(f"- Годовая ставка по кредиту в США (r_c): {r_c*100:.2f}%")
    print(f"- Годовая ставка по депозиту в Турции (r_d): {r_d*100:.2f}%")
    print(f"- Текущий обменный курс USD/TRY (k1): {k1:.2f}")
    print(f"- Прогнозируемая прибыль: {P:.2f} USD")

if __name__ == "__main__":
    calculate_profit()
