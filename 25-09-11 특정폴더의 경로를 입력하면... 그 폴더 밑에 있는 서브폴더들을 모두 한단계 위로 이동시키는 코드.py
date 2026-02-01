import os
import shutil

def move_subfolders_up(folder_path):
    """
    지정한 폴더 안의 모든 서브폴더들을 한 단계 위로 이동시키는 함수.
    """
    if not os.path.isdir(folder_path):
        print(f"❌ 잘못된 경로: {folder_path}")
        return
    
    parent_dir = os.path.dirname(folder_path)  # 한 단계 위 경로
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):  # 서브폴더일 때만 이동
            new_path = os.path.join(parent_dir, item)
            
            # 동일한 이름의 폴더가 이미 있을 경우 이름 뒤에 숫자 붙이기
            counter = 1
            while os.path.exists(new_path):
                new_path = os.path.join(parent_dir, f"{item}_{counter}")
                counter += 1
            
            print(f"📂 {item_path} → {new_path}")
            shutil.move(item_path, new_path)

    print("✅ 모든 서브폴더 이동 완료!")

if __name__ == "__main__":
    folder_path = input("👉 이동시킬 기준 폴더 경로를 입력하세요: ").strip()
    move_subfolders_up(folder_path)
