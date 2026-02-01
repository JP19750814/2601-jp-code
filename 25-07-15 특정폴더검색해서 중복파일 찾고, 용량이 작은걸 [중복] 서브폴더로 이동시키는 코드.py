import os
import re
import shutil

def group_by_pattern(folder_path, pattern):
    """
    지정된 정규표현식에 따라 중복 후보 파일들을 그룹핑합니다.
    """
    grouped = {}
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if not os.path.isfile(fpath):
            continue

        match = pattern.search(fname)
        if match:
            key = match.group(0)  # 예: '-123'
            grouped.setdefault(key, []).append(fpath)

    return grouped

def move_duplicates(folder_path):
    """
    중복 패턴이 있는 파일들 중에서, 가장 큰 파일을 제외한 나머지를 '[중복]' 폴더로 이동.
    """
    pattern = re.compile(r"-\d{3}")  # '-001', '-123' 같은 패턴
    duplicates_folder = os.path.join(folder_path, "[중복]")

    # [중복] 폴더가 없으면 생성
    os.makedirs(duplicates_folder, exist_ok=True)

    grouped_files = group_by_pattern(folder_path, pattern)
    moved_count = 0

    for key, file_list in grouped_files.items():
        if len(file_list) <= 1:
            continue  # 중복 아님

        # 파일 크기 기준으로 내림차순 정렬
        file_list.sort(key=lambda f: os.path.getsize(f), reverse=True)

        # 첫 번째(가장 큰) 파일은 유지, 나머지는 이동
        for dup_file in file_list[1:]:
            dest_path = os.path.join(duplicates_folder, os.path.basename(dup_file))

            # 이름 충돌 시 "_1", "_2" 붙이기
            dest_path = resolve_conflict(dest_path)

            try:
                shutil.move(dup_file, dest_path)
                print(f"✅ 중복 파일 이동됨: {os.path.basename(dup_file)} → [중복] 폴더")
                moved_count += 1
            except Exception as e:
                print(f"⚠️ 이동 오류: {dup_file} → {e}")

    print(f"\n📦 총 {moved_count}개의 중복 파일이 '[중복]' 폴더로 이동되었습니다.")

def resolve_conflict(dest_path):
    """
    동일한 이름의 파일이 [중복] 폴더에 있을 경우 _1, _2 등 숫자를 붙여 덮어쓰기 방지.
    """
    base, ext = os.path.splitext(dest_path)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = f"{base}_{counter}{ext}"
        counter += 1
    return dest_path

def main():
    folder_path = input("📁 검사할 폴더 경로를 입력하세요: ").strip()
    if not os.path.isdir(folder_path):
        print("❌ 유효한 폴더 경로가 아닙니다.")
        return

    move_duplicates(folder_path)

if __name__ == "__main__":
    main()
