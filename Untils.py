#寻找指定文件的指定内容，并将其写入到新的文件中。
class Find:

    @staticmethod
    def search_file(path: str  , key_word: str,tree: int): # key_word 为正则表达式.tree 为0则不使用树状图展示。否则使用树状图展示
        import re
        import os
        # paths = []
        regex = re.compile(key_word)
        print("正在查找文件，请稍后...")
        for root, sub_files, files in os.walk(path):
            for file in files:
                if regex.findall(file):
                    print(f"找到文件：{os.path.join(root, file)}")
                    # paths.append(os.path.join(root, file))





