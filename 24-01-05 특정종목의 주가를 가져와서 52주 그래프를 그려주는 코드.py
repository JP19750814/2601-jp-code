import yfinance as yf
import matplotlib.pyplot as plt
import datetime

def get_stock_data(ticker):
    """
    주어진 종목 코드(ticker)에 대한 지난 52주간의 주가 데이터를 가져옵니다.
    """
    try:
        # 오늘 날짜와 52주 전 날짜 계산
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(weeks=52)
        
        # yfinance를 사용하여 데이터 다운로드
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            print(f"종목 코드 '{ticker}'에 대한 데이터를 찾을 수 없습니다.")
            return None
        return hist
    except Exception as e:
        print(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return None

def plot_52_week_range(hist, ticker):
    """
    주어진 주가 데이터(hist)를 사용하여 52주 변동폭 그래프를 그립니다.
    """
    plt.figure(figsize=(12, 6))
    
    # 종가(Close) 그래프 그리기
    plt.plot(hist.index, hist['Close'], label='종가', color='blue')
    
    # 최고가(High)와 최저가(Low) 그래프 그리기
    plt.plot(hist.index, hist['High'], label='52주 최고가', color='green', linestyle='--')
    plt.plot(hist.index, hist['Low'], label='52주 최저가', color='red', linestyle='--')
    
    plt.title(f"{ticker}의 지난 52주 주가 변동폭")
    plt.xlabel("날짜")
    plt.ylabel("가격 (USD)")  # 한국 주식을 원한다면 통화 단위를 KRW로 변경하세요.
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    # 사용자로부터 종목 코드 입력 받기
    ticker = input("주가를 조회할 종목 코드를 입력하세요 (예: AAPL, 005930.KS): ").strip().upper()
    
    # 주가 데이터 가져오기
    hist = get_stock_data(ticker)
    
    if hist is not None:
        # 그래프 그리기
        plot_52_week_range(hist, ticker)

if __name__ == "__main__":
    main()
