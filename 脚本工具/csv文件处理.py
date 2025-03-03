# 适用pandas处理csv文件，并执行相应操作。示例：

import pandas as pd
import os

def clean_csv(file_path, output_path="cleaned_data.csv"):
    try:
        # 1. 读取 CSV 文件
        df = pd.read_csv(file_path, encoding="utf-8")

        # 2. 去除重复项（基于 'id' 或 'email'）
        df.drop_duplicates(subset=["id", "email"], keep="first", inplace=True)

        # 3. 处理缺失值 填充
        for col in df.columns:
            if df[col].dtype == "object":  # 文本列填充 '未知'
                df[col].fillna("未知", inplace=True)
            elif df[col].dtype in ["int64", "float64"]:  # 数值列填充均值
                df[col].fillna(df[col].mean(), inplace=True)

        # 4. 格式统一
        if "email" in df.columns:
            df["email"] = df["email"].str.lower().str.strip()  # 邮箱转小写，去除空格
        if "name" in df.columns:
            df["name"] = df["name"].str.title()  # 名字首字母大写
        if "salary" in df.columns:
            df["salary"] = df["salary"].apply(lambda x: round(x, 2))  # 保留两位小数
        if "join_date" in df.columns:
            df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce").dt.strftime("%Y-%m-%d")
            df["join_date"].fillna("2000-01-01", inplace=True)  # 无效日期填充默认值

        # 5. 导出清理后的数据
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"✅ 数据清洗完成！已保存到：{output_path}")

    except Exception as e:
        print(f"❌ 处理文件时出错：{e}")

if __name__ == "__main__":
    file_path = input("请输入 CSV 文件路径：").strip()
    if os.path.exists(file_path):
        clean_csv(file_path)
    else:
        print("❌ 文件不存在，请检查路径是否正确！")
