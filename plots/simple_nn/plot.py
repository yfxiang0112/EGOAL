import matplotlib.pyplot as plt

with open('plots/simple_nn/eval.txt') as f:
    evaluate_dict = eval(f.readline())

# Plot per-label accuracies
mean_accuracy = sum(evaluate_dict.values()) / len(evaluate_dict)

plt.figure(figsize=(8, 6))

plt.bar(evaluate_dict.keys(), evaluate_dict.values(), width=1, color='blue', label='Per-Label Accuracy')
plt.axhline(y=mean_accuracy, color='orange', linestyle='--', label=f'Mean Accuracy: {mean_accuracy:.3f}',
            linewidth=3)
plt.xlabel('Labels')
plt.ylabel('Accuracy')
plt.title('Per-Label Accuracy Plot')
#plt.xticks(rotation=90)
plt.legend()

# 调整布局，使得图像不重叠
plt.tight_layout()

# 保存图形
plt.savefig('per_label_accuracy.png')

# 显示图形
plt.show()
