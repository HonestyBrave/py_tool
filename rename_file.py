import os

root_dir = "D:/self_study/exampleForOpenCV/pictureSource/train_data/"

def get_all_dir():
    for root, dirs, files in os.walk(root_dir):
        for child_root in dirs:
            change_file_name(os.path.join(root_dir, child_root))

def change_file_name(file_dir):
    files = os.listdir(file_dir)
    i = 0;
    file_form = ".bmp"
    # 把文件根据文件名排序，不然重命名文件已存在
    files.sort(key=lambda x:int(x[:-4]))
    for file in files:
        os.rename(os.path.join(file_dir, file), os.path.join(file_dir, str(i)+file_form))
        i += 1


if __name__ == "__main__":
    get_all_dir()