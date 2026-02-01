import os
import shutil

def move_subfolders_up(base_folder):
    # 최상위 폴더가 존재하지 않으면 종료
    if not os.path.exists(base_folder):
        print(f"Folder '{base_folder}' does not exist.")
        return

    # "yes to all" 상태를 위한 플래그
    yes_to_all = False

    # 최상위 폴더의 바로 하위 폴더 탐색
    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        if os.path.isdir(subfolder_path):
            # 하위 폴더의 서브폴더 탐색 (2단계 서브폴더)
            for sub_subfolder in os.listdir(subfolder_path):
                sub_subfolder_path = os.path.join(subfolder_path, sub_subfolder)

                if os.path.isdir(sub_subfolder_path):
                    # 서브폴더를 최상위 폴더의 하위 폴더로 이동
                    new_path = os.path.join(base_folder, sub_subfolder)

                    # 사용자 확인 요청
                    if not yes_to_all:
                        response = input(f"Move {sub_subfolder_path} to {new_path}? (y/n/a): ").strip().lower()
                        if response == 'y':
                            try:
                                shutil.move(sub_subfolder_path, new_path)
                                print(f"Moved: {sub_subfolder_path} -> {new_path}")
                            except Exception as e:
                                print(f"Error moving {sub_subfolder_path} to {new_path}: {e}")
                        elif response == 'n':
                            print(f"Skipped: {sub_subfolder_path}")
                        elif response == 'a':
                            yes_to_all = True
                            try:
                                shutil.move(sub_subfolder_path, new_path)
                                print(f"Moved: {sub_subfolder_path} -> {new_path}")
                            except Exception as e:
                                print(f"Error moving {sub_subfolder_path} to {new_path}: {e}")
                    else:
                        try:
                            shutil.move(sub_subfolder_path, new_path)
                            print(f"Moved: {sub_subfolder_path} -> {new_path}")
                        except Exception as e:
                            print(f"Error moving {sub_subfolder_path} to {new_path}: {e}")

if __name__ == "__main__":
    while True:
        folder_name = input("Enter the base folder path: ")
        if not folder_name.strip():
            print("No folder path provided. Exiting.")
            break
        move_subfolders_up(folder_name)
        print("[새로운 작업 폴더를 알려주십시요, 만일 입력없이 엔터를 치면 이 작업은 종료됩니다]")

