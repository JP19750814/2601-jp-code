import os
import shutil

def resolve_conflict_path(dest_path):
    """이미 존재하는 파일 이름의 충돌을 피하기 위해 숫자를 붙임"""
    if not os.path.exists(dest_path):
        return dest_path

    base, ext = os.path.splitext(dest_path)
    counter = 1
    new_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base}_{counter}{ext}"
    return new_path

def move_files_from_subfolders_up(base_folder):
    if not os.path.exists(base_folder):
        print(f"❌ 폴더가 존재하지 않습니다: {base_folder}")
        return

    # 하위 폴더 탐색
    for entry in os.listdir(base_folder):
        entry_path = os.path.join(base_folder, entry)
        if os.path.isdir(entry_path):
            # 해당 하위 폴더 내의 파일만 이동
            for item in os.listdir(entry_path):
                item_path = os.path.join(entry_path, item)
                if os.path.isfile(item_path):
                    dest_path = os.path.join(base_folder, item)
                    dest_path = resolve_conflict_path(dest_path)
                    try:
                        shutil.move(item_path, dest_path)
                        print(f"✅ Moved: {item_path} → {dest_path}")
                    except Exception as e:
                        print(f"⚠️ Error moving {item_path}: {e}")

if __name__ == "__main__":
    while True:
        folder_name = input("📁 상위 폴더 경로를 입력하세요 (엔터 입력 시 종료): ").strip()
        if not folder_name:
            print("프로그램을 종료합니다.")
            break
        move_files_from_subfolders_up(folder_name)
