import pandas as pd
import matplotlib.pyplot as plt

# 示例数据
data = {'x': [1, 2, 3, 4], 'y': [1, 4, 9, 16]}
df = pd.DataFrame(data, index=['A', 'B', 'C', 'D'])

# 边关系字典
edges = {'A': ['B', 'C'], 'B': ['C', 'D'], 'C': ['D']}

# 绘制散点图
plt.scatter(df['x'], df['y'])

# 标注结点
for label, x, y in zip(df.index, df['x'], df['y']):
    plt.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha='center')

# 绘制边
for start, ends in edges.items():
    for end in ends:
        x_values = [df.loc[start, 'x'], df.loc[end, 'x']]
        y_values = [df.loc[start, 'y'], df.loc[end, 'y']]
        plt.plot(x_values, y_values, 'k-')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Graph Visualization')
plt.show()
