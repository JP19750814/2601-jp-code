import os
import shutil

def move_subfolders_up(base_folder, target_string):
    # 최상위 폴더가 존재하지 않으면 종료
    if not os.path.exists(base_folder):
        print(f"Folder '{base_folder}' does not exist.")
        return

    # 최상위 폴더의 바로 하위 폴더 탐색
    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        if os.path.isdir(subfolder_path):
            # 하위 폴더의 서브폴더 탐색 (2단계 서브폴더)
            for sub_subfolder in os.listdir(subfolder_path):
                sub_subfolder_path = os.path.join(subfolder_path, sub_subfolder)

                if os.path.isdir(sub_subfolder_path):
                    # 특정 문자열이 이름에 포함되어 있는지 확인
                    if target_string in sub_subfolder:
                        # 서브폴더를 최상위 폴더의 하위 폴더로 이동
                        new_path = os.path.join(base_folder, sub_subfolder)
                        try:
                            shutil.move(sub_subfolder_path, new_path)
                            print(f"Moved: {sub_subfolder_path} -> {new_path}")
                        except Exception as e:
                            print(f"Error moving {sub_subfolder_path} to {new_path}: {e}")
                    else:
                        print(f"Skipped: {sub_subfolder_path} (does not contain '{target_string}')")

if __name__ == "__main__":
    while True:
        folder_name = input("Enter the base folder path: ")
        if not folder_name.strip():
            print("No folder path provided. Exiting.")
            break
        target_string = input("Enter the target string to look for in subfolder names: ").strip()
        if not target_string:
            print("No target string provided. Exiting.")
            break
        move_subfolders_up(folder_name, target_string)
        print("[새로운 작업 폴더를 알려주십시요, 만일 입력없이 엔터를 치면 이 작업은 종료됩니다]")

