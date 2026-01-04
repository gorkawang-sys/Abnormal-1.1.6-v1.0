# Abnormal 插件翻译问题排查指南

## 问题现象
重新加载插件后,UI 界面依然显示英文。

## 根本原因分析

之前的翻译方案**错误地直接修改了源代码中的字符串**,这种方法在 Blender 插件中是**无效的**,因为:

1. ❌ **直接修改字符串不会被 Blender 翻译系统识别**
2. ❌ **没有使用 `bpy.app.translations` API**
3. ❌ **没有注册翻译字典**
4. ❌ **Blender 无法根据用户语言设置自动切换**

## 正确的翻译方案

现在已经采用 **Blender 官方翻译 API** 重新实现:

### ✅ 1. 创建翻译字典 (translations.py)

```python
translation_dict = {
    "zh_CN": {
        ("Operator", "Start Normal Editor"): "启动法线编辑器",
        ("*", "Filter Vertex Group"): "筛选顶点组",
        # ... 更多翻译条目
    }
}
```

**格式说明**:
- **键**: `(上下文, "原文")` 元组
  - 上下文通常是 `"Operator"` 或 `"*"` (通配符)
  - 原文必须与代码中的 `bl_label` 或 `text` 参数**完全一致**
- **值**: 翻译后的中文文本

### ✅ 2. 注册翻译系统 (__init__.py)

```python
def register():
    # 注册翻译
    bpy.app.translations.register(__name__, translations.translation_dict)
    # ... 其他注册代码

def unregister():
    # 取消注册翻译
    bpy.app.translations.unregister(__name__)
    # ... 其他取消注册代码
```

### ✅ 3. 添加调试输出

注册时会在控制台输出:
```
[Abnormal] 翻译系统注册成功
[Abnormal] 当前 Blender 语言: zh_CN
[Abnormal] 翻译条目数: 150
```

## 排查步骤

### 第 1 步: 检查 Blender 语言设置

1. 打开 **编辑 → 偏好设置 → 界面**
2. 找到 **翻译** 部分
3. 确认勾选了 **"翻译"** 复选框
4. 语言设置为 **"简体中文 (Simplified Chinese)"**
5. 确保勾选了 **"工具提示"** 和 **"界面"**

### 第 2 步: 查看控制台输出

**Windows**: 窗口 → 切换系统控制台  
**macOS/Linux**: 从终端启动 Blender

查找以下消息:

✅ **成功**:
```
[Abnormal] 翻译系统注册成功
[Abnormal] 当前 Blender 语言: zh_CN
[Abnormal] 翻译条目数: 150
```

❌ **失败**:
```
[Abnormal] 翻译系统注册失败: [错误信息]
```

### 第 3 步: 运行调试脚本

1. 在 Blender 中打开 **脚本编辑器**
2. 点击 **打开** → 选择 `translation_debug.py`
3. 点击 **运行脚本** (▶ 按钮)
4. 查看控制台输出的详细调试信息

调试脚本会检查:
- ✓ Blender 当前语言设置
- ✓ 翻译字典是否正确加载
- ✓ 翻译函数是否工作
- ✓ 插件是否已启用

### 第 4 步: 完全重启

如果以上步骤都正常,但翻译仍未生效:

1. **禁用插件**: 偏好设置 → 插件 → 取消勾选 Abnormal
2. **保存偏好设置**: 点击左下角 ☰ → 保存偏好设置
3. **完全关闭 Blender**
4. **重新启动 Blender**
5. **启用插件**: 偏好设置 → 插件 → 勾选 Abnormal
6. **查看控制台**: 确认看到 `[Abnormal] 翻译系统注册成功`

## 常见问题

### Q1: 为什么有些文本翻译了,有些没有?

**原因**: 翻译字典中的原文必须与代码中的文本**完全匹配**。

**解决方法**:
1. 找到未翻译的文本
2. 在代码中搜索该文本
3. 确认拼写、大小写、空格完全一致
4. 在 `translations.py` 中添加对应条目

### Q2: 控制台显示 "翻译系统注册成功" 但界面仍是英文?

**可能原因**:

1. **Blender 语言未设置为中文**
   - 检查: 编辑 → 偏好设置 → 界面 → 翻译
   - 确保语言为 "简体中文"

2. **上下文不匹配**
   - 翻译字典中的上下文 (Context) 必须正确
   - 大多数情况使用 `"*"` 通配符
   - 操作符使用 `"Operator"`

3. **缓存问题**
   - 完全关闭 Blender 并重启
   - 清除 Blender 配置缓存 (高级)

### Q3: 如何添加新的翻译条目?

编辑 `translations.py`:

```python
translation_dict = {
    "zh_CN": {
        # 添加新条目
        ("*", "Your English Text"): "你的中文翻译",
        
        # 操作符使用 "Operator" 上下文
        ("Operator", "My Operator"): "我的操作符",
        
        # 其他文本使用 "*" 通配符
        ("*", "Some Label"): "某个标签",
    }
}
```

### Q4: 模态编辑器内的动态文本如何翻译?

**问题**: `functions_modal_buttons.py` 中的文本是动态生成的,不使用 `bl_label`。

**解决方案**: 这些文本需要在代码中手动调用翻译函数:

```python
# 原代码
but = row.add_button(20, 'Reset UI')

# 修改为
but = row.add_button(20, bpy.app.translations.pgettext_iface('Reset UI'))
```

**注意**: 由于这涉及大量代码修改,当前版本暂未实现。如需此功能,需要进一步修改 `functions_modal_buttons.py`。

## 技术细节

### 翻译 API 使用

```python
# 注册翻译
bpy.app.translations.register(__name__, translation_dict)

# 手动翻译文本
translated = bpy.app.translations.pgettext_iface("Original Text")

# 带上下文的翻译
translated = bpy.app.translations.pgettext_iface("Original Text", "Context")

# 取消注册
bpy.app.translations.unregister(__name__)
```

### 上下文 (Context) 说明

| 上下文 | 用途 | 示例 |
|--------|------|------|
| `"*"` | 通配符,匹配所有 | 一般 UI 文本 |
| `"Operator"` | 操作符 | `bl_label`, `bl_description` |
| `"Property"` | 属性 | 属性描述 |
| `"Menu"` | 菜单 | 菜单项 |

### 语言代码

- **简体中文**: `zh_CN` 或 `zh_HANS`
- **繁体中文**: `zh_TW` 或 `zh_HANT`
- **英文**: `en_US`

Blender 4.x 推荐使用 `zh_CN`。

## 验证翻译是否生效

### 方法 1: 查看主面板

1. 在 3D 视口按 `N` 键
2. 找到 "BNPR Abnormal" 选项卡
3. 点击 **"启动法线编辑器"** 按钮 (原文: Start Normal Editor)

如果显示中文,说明翻译已生效。

### 方法 2: 查看操作符

1. 在搜索框 (F3) 输入 "abnormal"
2. 查看操作符名称是否为中文
3. 例如: "启动法线编辑器" 而不是 "Start Normal Editor"

### 方法 3: 查看偏好设置

1. 编辑 → 偏好设置 → 插件
2. 找到 Abnormal 插件
3. 展开插件设置
4. 查看选项卡名称: "显示"、"行为"、"按键映射-选择" 等

## 已知限制

### 1. 动态生成的 UI 文本

`functions_modal_buttons.py` 中的按钮文本是动态生成的,当前版本**已通过直接修改字符串实现中文显示**,但这不是标准的翻译方式。

**影响**: 这些文本不会随 Blender 语言设置自动切换。

**未来改进**: 需要修改代码,在每个文本生成处调用 `bpy.app.translations.pgettext_iface()`。

### 2. 部分系统消息

某些底层错误消息可能仍显示英文,因为它们来自 Blender 核心或 Python 异常。

### 3. 插件名称

插件名称 "Abnormal" 和 "BNPR" 保持英文,这是品牌名称,不进行翻译。

## 技术支持

如果按照以上步骤操作后翻译仍未生效:

1. **收集信息**:
   - Blender 版本
   - 操作系统
   - 控制台完整输出
   - `translation_debug.py` 运行结果

2. **检查文件**:
   - 确认 `translations.py` 文件存在
   - 确认 `__init__.py` 包含翻译注册代码
   - 确认 ZIP 包结构正确

3. **提供反馈**:
   - 描述具体哪些文本未翻译
   - 提供截图
   - 附上控制台输出

---

**文档版本**: 2.0  
**更新日期**: 2026年1月4日  
**适用插件版本**: Abnormal 1.1.6 中文版
