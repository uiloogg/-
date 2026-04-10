from pycaret.datasets import get_data
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def getdata(file):
    df9 = get_data("insurance")
    if file == 'excel':
        df9.to_excel("C:/Users/user/Desktop/python_works/期末報告/insurance.xlsx")
    elif file == 'csv':
        df9.to_csv("C:/Users/user/Desktop/python_works/期末報告/insurance.csv")
    else:
        df9.to_excel("C:/Users/user/Desktop/Projects and shit/python_works/期末報告/insurance.xlsx")
        df9.to_csv("C:/Users/user/Desktop/Projects and shit/python_works/期末報告/insurance.csv")

# 檢查檔案是否存在並執行相應操作
xlsx_exists = os.path.isfile("C:/Users/user/Desktop/Projects and shit/python_works/期末報告/insurance.xlsx")
csv_exists = os.path.isfile("C:/Users/user/Desktop/Projects and shit/python_works/期末報告/insurance.csv")

if not xlsx_exists and csv_exists:
    getdata('excel')
elif not csv_exists and xlsx_exists:
    getdata('csv')
elif not xlsx_exists and not csv_exists:
    getdata('both')


data = pd.read_excel("C:/Users/user/Desktop/Projects and shit/python_works/期末報告/insurance.xlsx", index_col=0)
print(f'{data.head()}\n')
print(f'{data.tail()}\n')
print(f'{data.dtypes}\n')

mean_dict = data.mean(numeric_only=True).round(2)
mean_dict = mean_dict.to_dict()
print(f'總共有{data.index.max()}筆資料\n')
for key, value in mean_dict.items():
    print(f'{key} 的平均值是: {value}')
print('\n')
mid_dict = data.median(numeric_only=True).round(2)
mid_dict = mid_dict.to_dict()
for key, value in mid_dict.items():
    print(f'{key} 的中位數是: {value}')
print('\n')
max_dict = data.max(numeric_only=True).round(2)
max_dict = max_dict.to_dict()
for key, value in max_dict.items():
    print(f'{key} 的最大值是: {value}')
print('\n')
min_dict = data.min(numeric_only=True).round(2)
min_dict = min_dict.to_dict()
for key, value in min_dict.items():
    print(f'{key} 的最小值是: {value}')
print('\n')

null_dict = data.isnull().sum()
null_dict = null_dict.to_dict()
for key, value in null_dict.items():
    print(f'{key} 的缺失值有: {value}個')
null_percent = (data.isnull().sum() / len(data)) * 100
null_percent = null_percent.to_dict()
for key, value in null_percent.items():
    print(f'{key} 的缺失比有: {value}%')
print('\n')

plt.figure(figsize=(8, 6))
sns.heatmap(data.isnull(), cbar=False, cmap='viridis', yticklabels = 100)
plt.title('heatmap for null')
plt.show()

def detect_outliers(column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = max(0, Q1 - 1.5 * IQR)
    upper_bound = Q3 + 1.5 * IQR

    print(f"\n{column} 的異常值偵測:")
    print(f"Q1: {Q1}")
    print(f"Q3: {Q3}")
    print(f"IQR: {IQR}")
    print(f"異常值下限: {lower_bound}")
    print(f"異常值上限: {upper_bound}")
    plt.figure(figsize=(6, 8))
    sns.boxplot(y=data[column])
    plt.title(f'{column} 欄位的箱形圖（偵測異常值）')
    plt.ylabel(column)

    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers

# 呼叫函式偵測不同欄位的異常值
for col in ['age', 'bmi', 'charges']:
    outlier_data = detect_outliers(col)
    print(outlier_data)

# 使用 Matplotlib 繪製直方圖
plt.figure(figsize=(8, 6))
plt.hist(data['charges'], bins=10, edgecolor='black', color='skyblue')
plt.title('charges 欄位的直方圖 (Matplotlib)')
plt.xlabel('charges')
plt.ylabel('numbers')
plt.savefig(r'C:/Users/user/Desktop/Projects and shit/python_works/dataplot/plt直方圖.png')  # 儲存圖片檔
plt.close()

# 使用 Seaborn 繪製直方圖 (更簡潔，且可選 KDE)
plt.figure(figsize=(8, 6))
sns.histplot(data['charges'], bins=10, kde=True, color='salmon')
plt.title('charges 欄位的直方圖 (Seaborn with KDE)')
plt.xlabel('charges')
plt.ylabel('numbers')
plt.savefig(r'C:/Users/user/Desktop/Projects and shit/python_works/dataplot/sns直方圖.png')  # 儲存圖片檔
plt.close()


# 使用 Pandas Series 的 value_counts() 和 plot(kind='bar')
plt.figure(figsize=(8, 6))
data['age'].value_counts().plot(kind='bar', color='coral', edgecolor='black',alpha = 0.7)
plt.title('不同 ages 的保單數量(Pandas Series)')
plt.xlabel('age')
plt.ylabel('numbers')
plt.xticks(np.arange(0, len(data['age']), step=5), rotation=45)
plt.autoscale()
plt.savefig(r'C:/Users/user/Desktop/Projects and shit/python_works/dataplot/Pandas Series長條圖.png')  # 儲存圖片檔
plt.close()

# 使用 Seaborn 的 countplot
plt.figure(figsize=(8, 6))
sns.countplot(x='bmi', data=data, palette='pastel', order=data['bmi'].value_counts().index, alpha=0.7) 
plt.title('不同 bmi 的保單數量(Seaborn)')
plt.xlabel('bmi')
plt.ylabel('numbers')
plt.xticks(np.arange(0, len(data['bmi']), step=50), rotation=45)
plt.autoscale()
plt.savefig(r'C:/Users/user/Desktop/Projects and shit/python_works/dataplot/sns長條圖.png')  # 儲存圖片檔
plt.close()

# 使用 Matplotlib 繪製散佈圖
plt.figure(figsize=(8, 6))
plt.scatter(data['charges'], data['bmi'], alpha=0.7, color='blue', label='Linear Relationship')
plt.title('charges vs bmi 散佈圖 (Matplotlib)')
plt.xlabel('charges')
plt.ylabel('bmi')
plt.legend()
plt.savefig(r'C:/Users/user/Desktop/Projects and shit/python_works/dataplot/plt散佈圖.png')  # 儲存圖片檔
plt.close()


# 使用 Seaborn 繪製散佈圖 (更易於添加趨勢線等)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='charges', y='age', data=data, hue='smoker')
# sns.regplot(x='X', y='Y_Nonlinear', data=df_num_num, scatter=False, color='red') # 添加迴歸線 (可能不適合非線性)
plt.title('charges vs age 散佈圖 (Seaborn)')
plt.xlabel('charges')
plt.ylabel('ages')
plt.legend()
plt.savefig(r'C:/Users/user/Desktop/Projects and shit/python_works/dataplot/sns散佈圖.png')  # 儲存圖片檔
plt.close()


#從 status_type 建立 smoker 欄位
data['status_type'] = data['smoker'].apply(lambda x: 'Yes' if x == 'Smoker' else 'Non-Smoker')

# 使用 Seaborn 繪製分組長條圖
plt.figure(figsize=(10, 7))
sns.countplot(x='charges', hue='status_type', data=data, palette='viridis')
plt.title('不同 charges 下抽菸與否的分佈')
plt.xlabel('charges')
plt.ylabel('smokers')
plt.xticks(np.arange(0, len(data['charges']), step=100), rotation=45)
plt.autoscale()
plt.tight_layout()
plt.savefig(r'C:/Users/user/Desktop/Projects and shit/python_works/dataplot/分組長條圖.png')  # 儲存圖片檔
plt.close()


# 分組小提琴圖
plt.figure(figsize=(8, 6))
sns.violinplot(x='age', y='bmi', data=data, palette='muted')
plt.title('不同 age 的 bmi 分佈 (小提琴圖)')
plt.xticks(np.arange(0, len(data['bmi']), step=50), rotation=45)
plt.autoscale()
plt.savefig(r'C:/Users/user/Desktop/Projects and shit/python_works/dataplot/分組小提琴圖.png')  # 儲存圖片檔
plt.close()

