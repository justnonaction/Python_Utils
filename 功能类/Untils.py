from treelib import Tree
import re
import os
from typing import Set, List, Tuple



class Find:
    @staticmethod
    def _create_tree() -> Tree:
        """Initialize the tree with root node"""
        tree = Tree()
        tree.create_node("Root", "root")
        return tree

    @staticmethod
    def _find_matching_files(path: str, pattern: re.Pattern) -> Tuple[Set[str], List[Tuple[str, str]]]:
        """Find all matching files and their directory paths"""
        required_dirs = set()
        file_paths = []

        for root, _, files in os.walk(path):
            for file in files:
                if pattern.search(file):
                    current_path = root
                    while current_path >= path:
                        required_dirs.add(current_path)
                        current_path = os.path.dirname(current_path)
                    file_paths.append((root, file))

        return required_dirs, file_paths

    @staticmethod
    def _build_directory_tree(tree: Tree, directories: Set[str], path: str) -> None:
        """Build directory structure in the tree"""
        sorted_dirs = sorted(directories, key=lambda x: len(x.split(os.sep)))

        for dir_path in sorted_dirs:
            if dir_path == path:
                continue

            dir_name = os.path.basename(dir_path) or dir_path
            parent_path = os.path.dirname(dir_path)
            parent_id = "root" if parent_path == path or dir_path == path else parent_path

            try:
                if not tree.contains(dir_path):
                    tree.create_node(dir_name, dir_path, parent=parent_id)
            except Exception:
                continue

    @staticmethod
    def _add_files_to_tree(tree: Tree, file_paths: List[Tuple[str, str]]) -> None:
        """Add matching files to the tree"""
        for root, file in file_paths:
            try:
                tree.create_node(f"📄 {file}", os.path.join(root, file), parent=root)
            except Exception:
                continue

    @staticmethod
    def search_file(path: str, key_word: str, mod: int) -> None:
        """Main search function"""
        print("正在查找文件，请稍后...")
        pattern = re.compile(key_word)
        tree = Find._create_tree()

        if mod == 1:  # 完整目录结构
            for root, _, files in os.walk(path):
                dir_name = os.path.basename(root) or root
                parent_path = os.path.dirname(root)
                parent_id = "root" if parent_path == path else parent_path

                try:
                    tree.create_node(dir_name, root, parent=parent_id)
                    for file in files:
                        if pattern.search(file):
                            tree.create_node(f"📄 {file}", os.path.join(root, file), parent=root)
                except Exception:
                    continue

        elif mod == 2:  # 仅匹配文件的目录结构
            required_dirs, file_paths = Find._find_matching_files(path, pattern)
            Find._build_directory_tree(tree, required_dirs, path)
            Find._add_files_to_tree(tree, file_paths)

        print("搜索完成，已将结果保存在tree.txt文件")
        tree.save2file("tree.txt")