import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

df = pd.read_csv('output.csv')
filtered_df = df[df['computation_time'] > 10000000000].copy()
filtered_df = filtered_df.reset_index()
avg_ns_per_cycle = (filtered_df['computation_time'] / filtered_df['total_quantum_cycles']).mean()

x = np.arange(len(filtered_df))
x_log = np.log(x + 1)

slope_time, intercept_time, r_value_time, p_value_time, std_err_time = stats.linregress(x_log, filtered_df['computation_time'])

slope_cycles, intercept_cycles, r_value_cycles, p_value_cycles, std_err_cycles = stats.linregress(x_log, filtered_df['total_quantum_cycles'])

print("\nLogarithmic Regression Equations:")
print(f"Computation Time: y = {slope_time:.8f}ln(x) + {intercept_time:.8f}")
print(f"Quantum Cycles: y = {slope_cycles:.8f}ln(x) + {intercept_cycles:.8f}")

top_3_indices = filtered_df.nlargest(5, 'computation_time').index
top_3_factors = filtered_df.loc[top_3_indices, 'factors']
top_3_times = filtered_df.loc[top_3_indices, 'computation_time']

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

line1 = ax1.plot(filtered_df['computation_time'], marker='o', linestyle='-',
                 linewidth=2, markersize=6, color='red', label='Computation Time')
x_smooth = np.linspace(1, len(filtered_df), 1000)
y_time_log = slope_time * np.log(x_smooth) + intercept_time
line1_trend = ax1.plot(x_smooth - 1, y_time_log, '--', color='darkred',
                       label=f'Time Log Fit (R²={r_value_time**2:.3f})')

for idx, factor, time in zip(top_3_indices, top_3_factors, top_3_times):
    ax1.annotate(f'{factor}',
                xy=(idx, time),
                xytext=(10, 20),
                textcoords='offset points',
                bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8),
                arrowprops=dict(arrowstyle='->'),
                ha='left')

ax1.set_xlabel('Sample Index', fontsize=12)
ax1.set_ylabel('Computation Time', color='red', fontsize=12)
ax1.tick_params(axis='y', labelcolor='red')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

line2 = ax2.plot(filtered_df['total_quantum_cycles'], marker='s', linestyle='-',
                 linewidth=2, markersize=6, color='blue', label='Quantum Cycles')
y_cycles_log = slope_cycles * np.log(x_smooth) + intercept_cycles
line2_trend = ax2.plot(x_smooth - 1, y_cycles_log, '--', color='darkblue',
                       label=f'Cycles Log Fit (R²={r_value_cycles**2:.3f})')

ax2.set_ylabel('Total Quantum Cycles', color='blue', fontsize=12)
ax2.tick_params(axis='y', labelcolor='blue')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

plt.title('High Computation Times vs Quantum Cycles (Log Fit)', fontsize=14, pad=20)
lines = line1 + line1_trend + line2 + line2_trend
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

note_text = f'Average: {avg_ns_per_cycle:.2f} ns/cycle'
plt.figtext(0.99, 0.01, note_text, ha='right', va='bottom',
            bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8),
            fontsize=10)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()