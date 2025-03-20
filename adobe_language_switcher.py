import tkinter as tk
from tkinter import messagebox, filedialog
import xml.etree.ElementTree as ET
import os
import sys
import ctypes
import json

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

CONFIG_FILE = 'config.json'
DEFAULT_XML_PATH = r"C:\Program Files\Adobe\Adobe After Effects 2022\Support Files\AMT\application.xml"

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {'xml_path': DEFAULT_XML_PATH}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("错误", f"保存配置失败：{str(e)}")

def get_xml_path():
    return load_config()['xml_path']

def show_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("配置AfterEffects语言文件路径")
    settings_window.geometry("500x150")
    settings_window.configure(bg='#f0f0f0')
    settings_window.resizable(False, False)
    
    # 设置窗口相对于主窗口居中
    x = root.winfo_x() + (root.winfo_width() - 500) // 2
    y = root.winfo_y() - 170  # 在主窗口上方显示
    if y < 0: y = root.winfo_y() + root.winfo_height() + 20  # 如果上方空间不足，则显示在下方
    settings_window.geometry(f"500x150+{x}+{y}")
    
    current_path = get_xml_path()
    
    path_frame = tk.Frame(settings_window, bg='#f0f0f0')
    path_frame.pack(pady=20, padx=20, fill='x')
    
    path_entry = tk.Entry(path_frame, width=50)
    path_entry.insert(0, current_path)
    path_entry.pack(side=tk.LEFT, padx=(0, 10))
    
    def browse_file():
        file_path = filedialog.askopenfilename(
            title="选择XML文件",
            filetypes=[("XML files", "*.xml")]
        )
        if file_path:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, file_path)
    
    tk.Button(
        path_frame,
        text="浏览",
        command=browse_file,
        bg='#4a90e2',
        fg='white',
        font=('微软雅黑', 10)
    ).pack(side=tk.LEFT)
    
    button_frame = tk.Frame(settings_window, bg='#f0f0f0')
    button_frame.pack(pady=20)
    
    def save_settings():
        new_path = path_entry.get().strip()
        if not new_path:
            messagebox.showerror("错误", "路径不能为空")
            return
        if not os.path.exists(new_path):
            messagebox.showerror("错误", "文件不存在")
            return
        config = load_config()
        config['xml_path'] = new_path
        save_config(config)
        settings_window.destroy()
        update_current_language()
    
    tk.Button(
        button_frame,
        text="保存",
        command=save_settings,
        width=10,
        bg='#4a90e2',
        fg='white',
        font=('微软雅黑', 10)
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        button_frame,
        text="取消",
        command=settings_window.destroy,
        width=10,
        bg='#4a90e2',
        fg='white',
        font=('微软雅黑', 10)
    ).pack(side=tk.LEFT, padx=5)

def get_current_language():
    try:
        tree = ET.parse(get_xml_path())
        root = tree.getroot()
        for elem in root.findall('.//Data[@key="installedLanguages"]'):
            return elem.text
    except Exception as e:
        messagebox.showerror("错误", f"读取语言设置失败：{str(e)}")
        return "未知"

def switch_language(lang):
    try:
        xml_path = get_xml_path()
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for elem in root.findall('.//Data[@key="installedLanguages"]'):
            elem.text = lang
            tree.write(xml_path, encoding='utf-8', xml_declaration=True)
            messagebox.showinfo("成功", f"语言已切换为{'中文' if lang == 'zh_CN' else '英文'}")
            update_current_language()
            return
    except Exception as e:
        messagebox.showerror("错误", f"切换语言失败：{str(e)}")

def update_current_language():
    current_lang = get_current_language()
    lang_text = "中文" if current_lang == "zh_CN" else "英文" if current_lang == "en_US" else current_lang
    current_lang_label.config(text=f"当前语言：{lang_text}")

# 确保以管理员权限运行
run_as_admin()

# 定义样式常量
COLORS = {
    'bg': '#f5f6fa',
    'primary': '#4a90e2',
    'primary_hover': '#357abd',
    'text': '#2c3e50',
    'label_bg': '#ffffff'
}

FONTS = {
    'title': ('微软雅黑', 14, 'bold'),
    'label': ('微软雅黑', 12),
    'button': ('微软雅黑', 10)
}

# 创建主窗口
root = tk.Tk()
root.title("Adobe After Effects 语言切换工具")
root.geometry("400x220")

# 设置窗口样式
root.configure(bg=COLORS['bg'])
root.resizable(False, False)

# 创建标题框架
title_frame = tk.Frame(root, bg=COLORS['bg'])
title_frame.pack(fill='x', pady=(20, 0))

# 创建标题标签
title_label = tk.Label(
    title_frame,
    text="After Effects 语言切换",
    font=FONTS['title'],
    bg=COLORS['bg'],
    fg=COLORS['text']
)
title_label.pack()

# 创建状态框架
status_frame = tk.Frame(root, bg=COLORS['label_bg'], bd=1, relief='solid')
status_frame.pack(fill='x', padx=30, pady=20)

# 创建并布局组件
current_lang_label = tk.Label(
    status_frame,
    text="当前语言：获取中...",
    bg=COLORS['label_bg'],
    fg=COLORS['text'],
    font=FONTS['label'],
    pady=10
)
current_lang_label.pack()

# 创建按钮框架
button_frame = tk.Frame(root, bg=COLORS['bg'])
button_frame.pack(pady=20)

# 创建版权信息标签
copyright_label = tk.Label(
    root,
    text="©️Yawiii  v1.0",
    bg=COLORS['bg'],
    fg=COLORS['text'],
    font=('微软雅黑', 9)
)
copyright_label.pack(side=tk.BOTTOM, pady=10)

# 创建按钮样式类
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.defaultBackground = kw.get('bg')
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = COLORS['primary_hover']

    def on_leave(self, e):
        self['bg'] = self.defaultBackground

# 创建语言切换按钮
HoverButton(
    button_frame,
    text="切换为英文",
    command=lambda: switch_language("en_US"),
    width=12,
    bg=COLORS['primary'],
    fg='white',
    font=FONTS['button'],
    relief='flat',
    cursor='hand2'
).pack(side=tk.LEFT, padx=5)

HoverButton(
    button_frame,
    text="切换为中文",
    command=lambda: switch_language("zh_CN"),
    width=12,
    bg=COLORS['primary'],
    fg='white',
    font=FONTS['button'],
    relief='flat',
    cursor='hand2'
).pack(side=tk.LEFT, padx=5)

# 更新当前语言显示
update_current_language()

# 创建设置按钮
HoverButton(
    button_frame,
    text="设置",
    command=show_settings,
    width=6,
    bg=COLORS['primary'],
    fg='white',
    font=FONTS['button'],
    relief='flat',
    cursor='hand2'
).pack(side=tk.RIGHT, padx=5)

# 启动主循环
root.mainloop()