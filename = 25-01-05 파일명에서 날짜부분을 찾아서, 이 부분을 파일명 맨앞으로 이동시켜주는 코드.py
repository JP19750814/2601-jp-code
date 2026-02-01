import os
import re
import time

def resolve_name_conflict(folder: str, filename: str) -> str:
    base, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{base}_{counter}{ext}"
        counter += 1
    return new_name

def is_modified_within_last_hour(file_path: str) -> bool:
    return (time.time() - os.path.getmtime(file_path)) < 3600

def normalize_date_str(year: str, month: str, day: str) -> str:
    yy = year[-2:]          # 2019 -> 19, 24 -> 24
    mm = month.zfill(2)
    dd = day.zfill(2)
    return f"{yy}-{mm}-{dd}"

def build_patterns():
    """
    날짜 후보들을 '완전한 토큰'으로만 매칭하도록 (?!\d) 등을 넣음.
    - YYYY.MM.DD
    - DD.MM.YYYY  (유럽/서양식 표기)
    - YY.MM.DD
    - YY-MM-DD
    - YYYY-MM-DD
    - DD-MM-YYYY
    """
    # 공통: 앞뒤가 숫자로 붙어있는 부분매칭 방지용
    # (?<!\d) : 앞이 숫자가 아니어야 함
    # (?!\d)  : 뒤가 숫자가 아니어야 함
    # 이렇게 하면 21.02.2019 안에서 21.02.20 부분매칭이 안 됨.
    return [
        # 1) YYYY.MM.DD
        re.compile(r"(?<!\d)(?P<y>\d{4})\.(?P<m>\d{2})\.(?P<d>\d{2})(?!\d)"),
        # 2) DD.MM.YYYY (서양식)
        re.compile(r"(?<!\d)(?P<d>\d{2})\.(?P<m>\d{2})\.(?P<y>\d{4})(?!\d)"),

        # 3) YYYY-MM-DD
        re.compile(r"(?<!\d)(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})(?!\d)"),
        # 4) DD-MM-YYYY (서양식)
        re.compile(r"(?<!\d)(?P<d>\d{2})-(?P<m>\d{2})-(?P<y>\d{4})(?!\d)"),

        # 5) YY.MM.DD  (주의: 부분매칭 방지 꼭 필요)
        re.compile(r"(?<!\d)(?P<y>\d{2})\.(?P<m>\d{2})\.(?P<d>\d{2})(?!\d)"),
        # 6) YY-MM-DD
        re.compile(r"(?<!\d)(?P<y>\d{2})-(?P<m>\d{2})-(?P<d>\d{2})(?!\d)"),
    ]

def get_patterns_with_ui():
    print("\n✅ 파일명에서 날짜를 찾아 맨 앞으로 옮깁니다.")
    print("   (옮겨지는 날짜 표기는 모두 'YY-MM-DD'로 통일됩니다. 예: 19-02-21)\n")

    print("자동 인식하는 날짜 형식(기본):")
    print("  - YY.MM.DD      (예: 23.11.04)")
    print("  - YYYY.MM.DD    (예: 2023.11.04)")
    print("  - DD.MM.YYYY    (예: 21.02.2019)  ← 이 케이스를 2019-02-21로 인식")
    print("  - YY-MM-DD      (예: 23-11-04)")
    print("  - YYYY-MM-DD    (예: 2023-11-04)")
    print("  - DD-MM-YYYY    (예: 21-02-2019)\n")

    expert = input("추가로 '특정 예시 날짜' 형식을 더 넣고 싶으면 입력 (Enter=건너뜀): ").strip()

    patterns = build_patterns()

    if expert:
        # 예시 날짜에서 구분자와 자리수(2/4)를 읽어 같은 형식을 추가
        m = re.fullmatch(r"(\d{2}|\d{4})([.\-])(\d{2})\2(\d{2}|\d{4})", expert)
        # 위는 "a.sep.b.sep.c" 형태만 받도록 간단화(혼합 구분자 X)
        if not m:
            print("⚠️ 예시 날짜 형식 인식 실패. 기본 형식만 사용합니다.")
        else:
            a, sep, b, c = m.groups()
            sep_esc = re.escape(sep)

            # a와 c 중 4자리인 쪽을 year로 판단
            if len(a) == 4 and len(c) == 2:
                # YYYY.sep.MM.sep.DD 형태라고 가정 (YYYY.MM.DD)
                pat = re.compile(rf"(?<!\d)(?P<y>\d{{4}}){sep_esc}(?P<m>\d{{2}}){sep_esc}(?P<d>\d{{2}})(?!\d)")
                patterns.insert(0, pat)
                print("✅ 전문가 형식 추가: YYYY{sep}MM{sep}DD")
            elif len(a) == 2 and len(c) == 4:
                # DD.sep.MM.sep.YYYY 형태라고 가정 (DD.MM.YYYY)
                pat = re.compile(rf"(?<!\d)(?P<d>\d{{2}}){sep_esc}(?P<m>\d{{2}}){sep_esc}(?P<y>\d{{4}})(?!\d)")
                patterns.insert(0, pat)
                print("✅ 전문가 형식 추가: DD{sep}MM{sep}YYYY")
            else:
                # 2-2-2 또는 4-2-4 같은 애매 케이스는 생략
                print("⚠️ 예시 날짜가 애매해서(연도 위치 판단 불가) 기본 형식만 사용합니다.")

    return patterns

def find_first_date(name_part: str, patterns):
    best = None
    best_pos = None
    for pat in patterns:
        m = pat.search(name_part)
        if not m:
            continue
        if best_pos is None or m.start() < best_pos:
            best = m
            best_pos = m.start()
    return best

def move_date_to_front(folder_path: str):
    patterns = get_patterns_with_ui()
    changed_count = 0

    for file_name in os.listdir(folder_path):
        old_path = os.path.join(folder_path, file_name)

        if os.path.isdir(old_path):
            continue

        if is_modified_within_last_hour(old_path):
            print(f"⏭️ 최근 1시간 내 수정: {file_name}")
            continue

        if file_name.startswith("=") or file_name[0].isdigit():
            print(f"⏭️ 조건(= 또는 숫자시작)으로 건너뜀: {file_name}")
            continue

        name_part, ext = os.path.splitext(file_name)

        m = find_first_date(name_part, patterns)
        if not m:
            continue

        y = m.group("y")
        mo = m.group("m")
        d = m.group("d")

        normalized = normalize_date_str(y, mo, d)

        # 이미 정규화 날짜로 시작하면 스킵
        if name_part.startswith(normalized):
            print(f"✅ 이미 정규화 날짜로 시작: {file_name}")
            continue

        matched_text = m.group(0)
        remainder = name_part.replace(matched_text, "").strip()

        new_base = f"{normalized} {remainder}".strip()
        new_base = " ".join(new_base.split())

        new_file_name = resolve_name_conflict(folder_path, f"{new_base}{ext}")
        new_path = os.path.join(folder_path, new_file_name)

        try:
            os.rename(old_path, new_path)
            print(f"✅ '{file_name}' → '{new_file_name}'")
            changed_count += 1
        except Exception as e:
            print(f"⚠️ 변경 실패: '{file_name}' - {e}")

    print(f"\n🔄 총 {changed_count}개의 파일명이 변경되었습니다.")

def main():
    folder_path = input("📁 작업할 폴더 경로를 입력하세요: ").strip()
    if not os.path.isdir(folder_path):
        print("❌ 유효한 폴더 경로가 아닙니다.")
        return
    move_date_to_front(folder_path)

if __name__ == "__main__":
    main()
