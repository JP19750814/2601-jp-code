# -*- coding: utf-8 -*-
"""
매크로 단축키 창
- 실행 시 독립 창이 뜨고 1~9 단축키가 표시됨
- 각 숫자 키를 누르면 해당 매크로 실행
- ESC: 창 닫고 종료
"""

import tkinter as tk
import subprocess
import sys
import os

# 구글 캘린더 URL
GOOGLE_CALENDAR_URL = "https://calendar.google.com"

# Windows에서 Chrome 경로 (일반적인 설치 위치)
CHROME_PATHS = [
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
]


def find_chrome():
    """설치된 Chrome 실행 파일 경로 찾기"""
    for path in CHROME_PATHS:
        if path and os.path.isfile(path):
            return path
    return None


def macro_1():
    """크롬으로 구글 캘린더 열기"""
    chrome = find_chrome()
    if chrome:
        try:
            subprocess.Popen([chrome, GOOGLE_CALENDAR_URL])
        except Exception as e:
            print(f"Chrome 실행 실패: {e}")
            # 기본 브라우저로 시도
            import webbrowser
            webbrowser.open(GOOGLE_CALENDAR_URL)
    else:
        import webbrowser
        webbrowser.open(GOOGLE_CALENDAR_URL)


def macro_2():
    """2번 매크로 (원하는 동작으로 수정)"""
    pass


def macro_3():
    """3번 매크로"""
    pass


def macro_4():
    """4번 매크로"""
    pass


def macro_5():
    """5번 매크로"""
    pass


def macro_6():
    """6번 매크로"""
    pass


def macro_7():
    """7번 매크로"""
    pass


def macro_8():
    """8번 매크로"""
    pass


def macro_9():
    """9번 매크로"""
    pass


MACROS = {
    "1": ("1. 구글 캘린더 (Chrome)", macro_1),
    "2": ("2. (설정 가능)", macro_2),
    "3": ("3. (설정 가능)", macro_3),
    "4": ("4. (설정 가능)", macro_4),
    "5": ("5. (설정 가능)", macro_5),
    "6": ("6. (설정 가능)", macro_6),
    "7": ("7. (설정 가능)", macro_7),
    "8": ("8. (설정 가능)", macro_8),
    "9": ("9. (설정 가능)", macro_9),
}


def main():
    root = tk.Tk()
    root.title("매크로 단축키")
    root.resizable(False, False)
    root.attributes("-topmost", True)  # 항상 위에

    # ESC로 종료
    def on_escape(event):
        root.destroy()
        sys.exit(0)

    root.bind("<Escape>", on_escape)

    # 1~9 키 바인딩 (일반 키 + 숫자패드)
    for key, (label, func) in MACROS.items():
        root.bind(f"<Key-{key}>", lambda e, f=func: f())
    numpad = {"1": "KP_1", "2": "KP_2", "3": "KP_3", "4": "KP_4", "5": "KP_5",
              "6": "KP_6", "7": "KP_7", "8": "KP_8", "9": "KP_9"}
    for key, event_name in numpad.items():
        if key in MACROS:
            root.bind(f"<Key-{event_name}>", lambda e, f=MACROS[key][1]: f())

    # UI: 단축키 목록
    frame = tk.Frame(root, padx=16, pady=12)
    frame.pack()

    tk.Label(frame, text="단축키 (1~9)", font=("맑은 고딕", 11, "bold")).pack(anchor="w")
    tk.Label(frame, text="ESC: 닫기", font=("맑은 고딕", 9), fg="gray").pack(anchor="w")

    for key, (label, _) in MACROS.items():
        row = tk.Frame(frame)
        row.pack(anchor="w", pady=2)
        tk.Label(row, text=f"[{key}]", font=("맑은 고딕", 10), width=4, anchor="w").pack(side="left")
        tk.Label(row, text=label, font=("맑은 고딕", 10)).pack(side="left")

    # UI 배치 후 창 크기·위치 설정 (화면 중앙)
    root.update_idletasks()
    w = max(320, root.winfo_reqwidth())
    h = max(280, root.winfo_reqheight())
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = max(0, (sw - w) // 2)
    y = max(0, (sh - h) // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # 창이 확실히 맨 앞에 보이도록
    def bring_to_front():
        root.lift()
        root.attributes("-topmost", True)
        root.focus_force()

    root.after(100, bring_to_front)
    root.mainloop()


if __name__ == "__main__":
    main()
