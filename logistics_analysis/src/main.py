import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """加载数据"""
    return pd.read_csv(file_path)

def clean_data(data):
    """清洗数据"""
    # 时间标准化
    data['sales_time'] = pd.to_datetime(data['sales_time'])
    data['delivery_time'] = pd.to_datetime(data['delivery_time'])

    # 删除缺失值
    data.dropna(subset=['order_id', 'sales_time', 'delivery_time'], inplace=True)

    # 替换空值
    data.fillna({'quantity': 0, 'status': 'Unknown'}, inplace=True)

    # 去重
    data.drop_duplicates(subset='order_id', inplace=True)

    return data

def exploratory_analysis(data):
    """探索性分析"""
    # 检查负数
    negative_values = data[data['quantity'] < 0]
    print("Negative values:\n", negative_values)
    data.loc[data['quantity'] < 0, 'quantity'] = abs(data['quantity'])

    # 绘制箱线图检查异常值
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=data['quantity'])
    plt.title('Quantity Distribution')
    plt.xlabel('Quantity')
    plt.ylabel('Frequency')
    plt.show()

def visualize_data(data):
    """可视化数据"""
    # 直方图
    plt.figure(figsize=(10, 6))
    plt.hist(data['quantity'], bins=20)
    plt.title('Quantity Distribution')
    plt.xlabel('Quantity')
    plt.ylabel('Frequency')
    plt.show()

    # 散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(data['sales_time'], data['delivery_time'])
    plt.title('Sales vs Delivery Time')
    plt.xlabel('Sales Time')
    plt.ylabel('Delivery Time')
    plt.show()

    # 柱状图
    status_counts = data['status'].value_counts()
    plt.figure(figsize=(10, 6))
    status_counts.plot(kind='bar')
    plt.title('Order Status Counts')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.show()

def analyze_delivery_performance(data):
    """分析物流表现"""
    # 计算准时到件率
    on_time_deliveries = data[data['delivery_time'] <= data['sales_time'] + pd.Timedelta(days=7)]
    on_time_rate = len(on_time_deliveries) / len(data) * 100
    print(f"On-time delivery rate: {on_time_rate:.2f}%")

    # 分析延迟订单的城市分布
    delayed_orders = data[data['delivery_time'] > data['sales_time'] + pd.Timedelta(days=7)]
    print("Delayed orders by city:\n", delayed_orders.groupby('city').size())

def main():
    # 设置数据文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(current_dir, '..', 'data', 'orders.csv')

    # 加载数据
    data = load_data(data_file_path)

    # 清洗数据
    cleaned_data = clean_data(data)

    # 探索性分析
    exploratory_analysis(cleaned_data)

    # 可视化数据
    visualize_data(cleaned_data)

    # 分析物流表现
    analyze_delivery_performance(cleaned_data)

if __name__ == "__main__":
    main()