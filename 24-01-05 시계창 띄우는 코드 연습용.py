import tkinter as tk
import time

def update_clock():
    """현재 시간을 HH:MM:SS 형식으로 표시"""
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    # 1초마다 update_clock 함수를 다시 호출
    clock_label.after(1000, update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("디지털 시계")

    # 1cm 당 약 37.79픽셀 기준으로 계산
    cm_to_px = 37.79  
    width_px = int(10 * cm_to_px)  # 가로 10cm
    height_px = int(5 * cm_to_px)  # 세로 5cm

    # tkinter 창의 크기를 (가로 x 세로) 픽셀로 지정
    root.geometry(f"{width_px}x{height_px}")

    # 시계 표시용 라벨(글자 크기는 적절히 조절)
    clock_label = tk.Label(root, font=("Helvetica", 35), fg="black")
    clock_label.pack(expand=True, fill="both")

    # 처음 시계 업데이트 실행
    update_clock()

    root.mainloop()
