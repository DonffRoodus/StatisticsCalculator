# Statistics Calculator 统计计算器

A powerful and user-friendly statistical calculator built with Python and Tkinter. This application provides essential statistical calculations with an intuitive graphical interface.

基于Python和Tkinter构建的功能强大且用户友好的统计计算器。该应用程序通过直观的图形界面提供基本的统计计算功能。

## Features 功能特点

- **Multiple Statistical Operations 多种统计运算**
  - Mean (Average) 平均值
  - Median 中位数
  - Mode 众数
  - Standard Deviation 标准差
  - Variance 方差
  - Maximum and Minimum values 最大值和最小值
  - Range 范围
  - Quartiles 四分位数

- **User-Friendly Interface 用户友好界面**
  - Clear data input area 清晰的数据输入区域
  - Flexible data input format (comma, space, or newline separated) 灵活的数据输入格式（支持逗号、空格或换行分隔）
  - Adjustable decimal precision (1-10 digits) 可调整的小数精度（1-10位）
  - Scrollable results view 可滚动的结果视图
  - Copy results to clipboard functionality 复制结果到剪贴板功能

- **Data Input Support 数据输入支持**
  - Supports up to 100 numbers 支持最多100个数字
  - Accepts decimal numbers 接受小数输入
  - Multiple input formats (comma-separated, space-separated, or newline-separated) 多种输入格式（逗号分隔、空格分隔或换行分隔）

## Installation 安装说明

1. Clone the repository 克隆仓库:
   ```bash
   git clone https://github.com/yourusername/StatisticsCalculator.git
   cd StatisticsCalculator
   ```

2. Install the required dependencies 安装所需依赖:
   ```bash
   pip install -r calculator/requirements.txt
   ```

## Usage 使用说明

1. Run the calculator 运行计算器:
   ```bash
   python calculator/calculator.py
   ```

2. Enter your numbers in the input area using any of these formats 使用以下任意格式在输入区域输入数字:
   ```
   1.5, 2, 3.7
   1.5 2 3.7
   1.5
   2
   3.7
   ```

3. Select the statistical operations you want to perform 选择要执行的统计运算
4. Adjust the decimal precision if needed 根据需要调整小数精度
5. Click "Calculate" to see the results 点击"计算"查看结果
6. Use the "Copy Results" button to copy all results to clipboard 使用"复制结果"按钮将所有结果复制到剪贴板

## Dependencies 依赖项

- Python 3.x
- NumPy (1.24.3)
- Tkinter (included in Python standard library 包含在Python标准库中)

## Notes 注意事项

- Maximum input limit: 100 numbers 最大输入限制：100个数字
- Invalid inputs will trigger error messages 无效输入将触发错误消息
- Results can be copied to clipboard for easy sharing 结果可以复制到剪贴板以便分享
