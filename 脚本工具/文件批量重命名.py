# 该脚本实现对指定文件夹下的文件进行批量重命名。
'''
重命名格式：new_name_prefix（新的文件名） + start_index + 文件原始后缀。
'''

import os


def batch_rename_files(folder_path: str, new_name_prefix: str, start_index=1):

    if not os.path.isdir(folder_path):
        print("❌ 文件夹不存在！")
        return
    print("正在进行中，请稍后...")
    files = sorted(os.listdir(folder_path))
    for file in files:
        if  os.path.isfile(os.path.join(folder_path, file)):
            os.rename(os.path.join(folder_path,file), os.path.join(folder_path,new_name_prefix+str(start_index)+os.path.splitext(file)[-1]))
            start_index += 1
    print("重命名完成！")



def main():
    folder_path = input("请输入文件夹路径：")
    new_name_prefix = input("请输入新文件名前缀：")
    batch_rename_files(folder_path, new_name_prefix, 1)




if __name__ == "__main__":
    main()
