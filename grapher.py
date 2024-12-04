import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output.csv')

#over 1 second (in ns)
filtered_df = df[df['computation_time'] > 1000000000].copy()
filtered_df = filtered_df.reset_index()


avg_ns_per_cycle = (filtered_df['computation_time'] / filtered_df['total_quantum_cycles']).mean()

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

line1 = ax1.plot(filtered_df['computation_time'], marker='o', linestyle='-', 
                 linewidth=2, markersize=6, color='red', label='Computation Time')
ax1.set_xlabel('Sample Index', fontsize=12)
ax1.set_ylabel('Computation Time', color='red', fontsize=12)
ax1.tick_params(axis='y', labelcolor='red')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

line2 = ax2.plot(filtered_df['total_quantum_cycles'], marker='s', linestyle='-', 
                 linewidth=2, markersize=6, color='blue', label='Quantum Cycles')
ax2.set_ylabel('Total Quantum Cycles', color='blue', fontsize=12)
ax2.tick_params(axis='y', labelcolor='blue')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

plt.title('High Computation Times (>1,000,000) vs Quantum Cycles', fontsize=14, pad=20)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

note_text = f'Average: {avg_ns_per_cycle:.2f} ns/cycle'
plt.figtext(0.99, 0.01, note_text, ha='right', va='bottom', 
            bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8),
            fontsize=10)
            
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()