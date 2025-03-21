import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy import stats
from tkinter.font import Font

class StatisticalCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title('统计计算器')
        self.root.geometry('800x600')
        
        # 创建主滚动区域
        # 创建主滚动区域
        self.main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # 配置主Canvas和滚动条的布局
        self.main_canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 绑定鼠标滚轮事件，只在主窗口区域生效
        self.main_canvas.bind('<MouseWheel>', lambda event: self.main_canvas.yview_scroll(-1 * (event.delta // 120), 'units'))
        
        # 配置主窗口的网格权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 配置主Canvas的网格权重
        self.main_canvas.grid_rowconfigure(0, weight=1)
        self.main_canvas.grid_columnconfigure(0, weight=1)
        
        # 添加退出按钮
        exit_button = ttk.Button(self.root, text='退出', command=self.root.destroy)
        exit_button.grid(row=0, column=2, sticky=(tk.S, tk.E), padx=5, pady=5)
        
        # 设置字体
        self.title_font = Font(family='Microsoft YaHei', size=12, weight='bold')
        self.normal_font = Font(family='Microsoft YaHei', size=10)

        # 创建主框架
        self.main_frame = ttk.Frame(self.scrollable_frame, padding='10')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 输入区域
        self.create_input_section()
        # 操作选择区域
        self.create_operation_section()
        # 结果显示区域
        self.create_result_section()

    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.main_frame, text='数据输入', padding='5')
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 输入规则说明
        rules_text = '输入规则：\n1. 请输入数字，多个数字用逗号或空格分隔\n2. 最多支持100个数字\n3. 示例：1.5, 2, 3.7 或 1.5 2 3.7'
        ttk.Label(input_frame, text=rules_text, font=self.normal_font).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)

        # 数据输入框和滚动条
        input_container = ttk.Frame(input_frame)
        input_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.data_input = tk.Text(input_container, height=4, width=60, font=self.normal_font)
        self.data_input.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        input_scrollbar = ttk.Scrollbar(input_container, orient=tk.VERTICAL, command=self.data_input.yview)
        input_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.data_input.configure(yscrollcommand=input_scrollbar.set)

        # 按钮区域
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=1, sticky=(tk.N, tk.S), padx=5)

        ttk.Button(btn_frame, text='清空', command=self.clear_input).grid(row=0, column=0, pady=2)
        ttk.Button(btn_frame, text='计算', command=self.calculate).grid(row=1, column=0, pady=2)

        # 精度控制
        self.precision = tk.StringVar(value='4')
        precision_frame = ttk.Frame(btn_frame)
        precision_frame.grid(row=2, column=0, pady=5)
        ttk.Label(precision_frame, text='小数位数:', font=self.normal_font).grid(row=0, column=0, padx=2)
        precision_combo = ttk.Combobox(precision_frame, textvariable=self.precision, values=[str(i) for i in range(1, 11)],
                                      width=3, state='readonly')
        precision_combo.grid(row=0, column=1, padx=2)

    def create_operation_section(self):
        operation_frame = ttk.LabelFrame(self.main_frame, text='选择操作', padding='5')
        operation_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.operations = [
            '均值 (Mean)',
            '中位数 (Median)',
            '众数 (Mode)',
            '标准差 (Standard Deviation)',
            '方差 (Variance)',
            '最大值 (Maximum)',
            '最小值 (Minimum)',
            '范围 (Range)',
            '四分位数 (Quartiles)',
        ]

        self.selected_ops = []
        for i, op in enumerate(self.operations):
            var = tk.BooleanVar(value=op in ['均值 (Mean)', '中位数 (Median)', '众数 (Mode)', '方差 (Variance)'])
            if var.get():
                self.selected_ops.append(op)
            cb = ttk.Checkbutton(operation_frame, text=op, variable=var, command=lambda v=var, o=op: self.update_selected_operations(v, o))
            cb.grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)

    def create_result_section(self):
        result_frame = ttk.LabelFrame(self.main_frame, text='计算结果', padding='5')
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # 创建表格和滚动条容器
        tree_frame = ttk.Frame(result_frame)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建表格 - 设置水平滚动
        self.result_tree = ttk.Treeview(tree_frame, columns=('操作', '结果'), show='headings', height=10)
        self.result_tree.heading('操作', text='操作')
        self.result_tree.heading('结果', text='结果')
        # 设置列宽，增加结果列宽度
        self.result_tree.column('操作', width=200, minwidth=150, stretch=False)
        self.result_tree.column('结果', width=500, minwidth=400, stretch=True)
        
        # 设置表格的样式，启用自动换行
        style = ttk.Style()
        style.configure('Treeview', rowheight=80, wrap=True)
        
        # 添加垂直滚动条
        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=vsb.set)
        
        # 添加水平滚动条 - 确保正确配置
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.result_tree.xview)
        self.result_tree.configure(xscrollcommand=hsb.set)
        
        # 布局表格和滚动条 - 确保水平滚动条正确显示和启用
        self.result_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.E, tk.W))
        
        # 配置tree_frame的网格权重 - 确保表格可以水平扩展
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # 配置result_frame的网格权重 - 修改行权重配置
        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_rowconfigure(1, weight=0)
        result_frame.grid_rowconfigure(2, weight=0)

        # 复制按钮 - 移至第3行，避免与水平滚动条重叠
        ttk.Button(result_frame, text='复制结果', command=self.copy_results).grid(row=2, column=0, pady=5)

    def update_selected_operations(self, var, operation):
        if var.get():
            if operation not in self.selected_ops:
                self.selected_ops.append(operation)
        else:
            if operation in self.selected_ops:
                self.selected_ops.remove(operation)

    def clear_input(self):
        self.data_input.delete('1.0', tk.END)

    def copy_results(self):
        results = []
        for item in self.result_tree.get_children():
            op, val = self.result_tree.item(item)['values']
            results.append(f'{op}: {val}')
        if results:
            self.root.clipboard_clear()
            self.root.clipboard_append('\n'.join(results))
            messagebox.showinfo('成功', '结果已复制到剪贴板')

    def parse_input(self):
        text = self.data_input.get('1.0', tk.END).strip()
        if not text:
            raise ValueError('请输入数据')

        # 支持逗号、空格和换行符分隔
        text = text.replace('\n', ' ')
        numbers = []
        for num in text.replace(',', ' ').split():
            try:
                numbers.append(float(num))
            except ValueError:
                raise ValueError(f'无效的数字: {num}')

        if len(numbers) > 100:
            raise ValueError('输入数据过多，最多支持100个数字')

        if not numbers:
            raise ValueError('请输入数据')

        return np.array(numbers)

    def calculate(self):
        try:
            data = self.parse_input()
        except ValueError as e:
            messagebox.showerror('错误', str(e))
            return

        if not self.selected_ops:
            messagebox.showwarning('警告', '请选择至少一个操作')
            return

        # 清空现有结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # 创建运算中标识
        calculating_label = ttk.Label(self.main_frame, text='运算中...', font=self.normal_font)
        calculating_label.grid(row=3, column=0, columnspan=2, pady=5)
        self.root.update()

        # 将众数操作移到最后
        mode_op = None
        other_ops = []
        for op in self.selected_ops:
            if '众数' in op:
                mode_op = op
            else:
                other_ops.append(op)

        # 计算并显示结果
        # 先处理非众数的统计量
        for op in other_ops:
            if '均值' in op:
                result = np.mean(data)
            elif '中位数' in op:
                result = np.median(data)
            elif '标准差' in op:
                result = np.std(data)
            elif '方差' in op:
                result = np.var(data)
            elif '最大值' in op:
                result = np.max(data)
            elif '最小值' in op:
                result = np.min(data)
            elif '范围' in op:
                result = np.max(data) - np.min(data)
            elif '四分位数' in op:
                q1, q2, q3 = np.percentile(data, [25, 50, 75])
                result = f'Q1={q1:.2f}, Q2={q2:.2f}, Q3={q3:.2f}'

            if isinstance(result, (int, float)):
                try:
                    precision = max(1, min(10, int(self.precision.get())))
                except ValueError:
                    precision = 4
                result = f'{result:.{precision}f}'
            self.result_tree.insert('', tk.END, values=(op, result))

        # 最后处理众数
        if mode_op:
            unique_values, counts = np.unique(data, return_counts=True)
            max_count = np.max(counts)
            modes = unique_values[counts == max_count]
            result = ', '.join([f'{x}' for x in modes])
            result = '\n'.join([result[i:i+50] for i in range(0, len(result), 50)])
            self.result_tree.insert('', tk.END, values=(mode_op, result))

        # 移除运算中标识
        calculating_label.destroy()

def main():
    root = tk.Tk()
    app = StatisticalCalculator(root)
    root.mainloop()

if __name__ == '__main__':
    main()