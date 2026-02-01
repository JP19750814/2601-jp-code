import os

def list_subfolders_two_depth(root_folder: str):
    """
    root_folder 기준으로 두 단계 아래(depth = 2)의 서브폴더만 출력
    """
    if not os.path.isdir(root_folder):
        raise NotADirectoryError(f"폴더가 존재하지 않습니다: {root_folder}")

    depth2_folders = []

    # 1단계 탐색
    for first in os.listdir(root_folder):
        first_path = os.path.join(root_folder, first)
        if os.path.isdir(first_path):

            # 2단계 탐색
            for second in os.listdir(first_path):
                second_path = os.path.join(first_path, second)
                if os.path.isdir(second_path):
                    depth2_folders.append(second)

    print(f"\n📁 '{root_folder}' 두 단계 아래 서브폴더 목록:")

    for f in depth2_folders:
        print(" -", f)

    print(f"\n총 {len(depth2_folders)}개 폴더가 있습니다.\n")


if __name__ == "__main__":
    root = input("부모 폴더 경로를 입력하세요: ").strip()
    list_subfolders_two_depth(root)
