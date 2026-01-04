# Abnormal 插件翻译修复说明 (v3.0)

## 版本信息
- **插件名称**: Abnormal (BNPR 法线编辑工具)
- **原版本**: 1.1.6
- **汉化版本**: 1.1.6 中文版 v3.0 (修复版)
- **适用 Blender 版本**: 4.5.0+
- **修复日期**: 2026年1月4日

## 🔧 本次修复内容

### 问题诊断

用户反馈: **N面板显示中文,但3D视图工具栏仍显示英文**

### 根本原因

经过深入排查,发现了关键问题:

1. ❌ **v2.0 版本错误**: 直接在源代码中硬编码了中文字符串
   - `ui.py` 中 `text='筛选顶点组'` (应该是英文)
   - `operators.py` 中 `bl_label = "法线 ---> 顶点色"` (应该是英文)
   - `properties.py` 中 `name='设置'` (应该是英文)

2. ❌ **翻译字典上下文错误**: 使用了 `("Operator", ...)` 而不是 `("*", ...)`

3. ✅ **为什么 N面板显示中文**: 因为代码已经是中文,不需要翻译
4. ❌ **为什么工具栏显示英文**: Blender 翻译系统找不到匹配的英文原文

### 修复方案

#### 1. 恢复所有英文原文

**ui.py**:
```python
# 修复前 (错误)
text='筛选顶点组'
text='面角属性'
text='顶点色'
text='移至标题栏'
text='移至侧栏'

# 修复后 (正确)
text='Filter Vertex Group'
text='Face Corner Attribute'
text='Vertex Color'
text='Move to Header Tab'
text='Move to N Panel Tab'
```

**operators.py**:
```python
# 修复前 (错误)
bl_label = "法线  --->  顶点色"
bl_description = '将当前自定义法线转换为所选顶点色'

# 修复后 (正确)
bl_label = "Normals  --->  Vertex Colors"
bl_description = 'Convert current custom normals to the selected Vertex Colors'
```

**operators_modal.py**:
```python
# 修复前 (错误)
bl_label = "启动法线编辑器"
self.report({'WARNING'}, "发生错误。取消模态")

# 修复后 (正确)
bl_label = "Start Normal Editor"
self.report({'WARNING'}, "Something went wrong. Cancelling modal")
```

**properties.py**:
```python
# 修复前 (错误)
settings: EnumProperty(
    name='设置', description='要显示的设置',
    items=[('PREFS_DISPLAY', '显示', ''),
           ('PREFS_BEHAVIOR', '行为', ''), ...]
)

# 修复后 (正确)
settings: EnumProperty(
    name='Settings', description='Settings to display',
    items=[('PREFS_DISPLAY', 'Display', ''),
           ('PREFS_BEHAVIOR', 'Behavior', ''), ...]
)
```

#### 2. 修正翻译字典上下文

**translations.py**:
```python
# 修复前 (错误 - 使用 "Operator" 上下文)
("Operator", "Normals  --->  Vertex Colors"): "法线  --->  顶点色",
("Operator", "Start Normal Editor"): "启动法线编辑器",

# 修复后 (正确 - 使用 "*" 通配符)
("*", "Normals  --->  Vertex Colors"): "法线  --->  顶点色",
("*", "Start Normal Editor"): "启动法线编辑器",
```

**为什么要用 `"*"` 通配符?**

- `"Operator"` 上下文: 仅匹配操作符搜索菜单 (F3)
- `"*"` 通配符: 匹配所有位置,包括 N面板、工具栏、按钮等

#### 3. 添加缺失的翻译条目

新增:
```python
("*", "Convert current custom normals to the selected Face Corner Attribute"): "将当前自定义法线转换为所选面角属性",
("*", "Convert selected Face Corner Attribute to custom normals"): "将所选面角属性转换为自定义法线",
```

## ✅ 修复验证

### 测试步骤

1. **完全卸载旧版本**
   ```
   编辑 → 偏好设置 → 插件 → 移除 Abnormal
   完全关闭 Blender
   ```

2. **确认语言设置**
   ```
   编辑 → 偏好设置 → 界面
   ✅ 翻译: 勾选
   ✅ 语言: 简体中文
   ✅ 工具提示: 勾选
   ✅ 界面: 勾选
   ```

3. **安装新版本**
   ```
   编辑 → 偏好设置 → 插件 → 安装
   选择 Abnormal_CN_1_1_6.zip
   ✅ 勾选启用
   保存偏好设置
   ```

4. **查看控制台**
   ```
   Windows: 窗口 → 切换系统控制台
   
   应该看到:
   [Abnormal] 翻译系统注册成功
   [Abnormal] 当前 Blender 语言: zh_CN
   [Abnormal] 翻译条目数: 154
   ```

5. **验证 N面板**
   ```
   3D 视口按 N 键
   找到 "BNPR Abnormal" 选项卡
   
   应该看到:
   ✅ "启动法线编辑器" (按钮)
   ✅ "筛选顶点组" (输入框)
   ✅ "面角属性" (输入框)
   ✅ "法线 ---> 面角属性" (按钮)
   ✅ "面角属性 ---> 法线" (按钮)
   ✅ "移至标题栏" (按钮)
   ```

6. **验证 3D 视图工具栏**
   ```
   3D 视图 → 标题栏 → BNPR Abnormal 菜单
   
   应该看到:
   ✅ "启动法线编辑器" (按钮)
   ✅ "筛选顶点组" (输入框)
   ✅ "面角属性" (输入框)
   ✅ "法线 ---> 面角属性" (按钮)
   ✅ "面角属性 ---> 法线" (按钮)
   ✅ "移至侧栏" (按钮)
   ```

7. **验证搜索菜单**
   ```
   按 F3 打开搜索
   输入 "abnormal" 或 "法线"
   
   应该看到:
   ✅ "启动法线编辑器"
   ✅ "法线 ---> 顶点色"
   ✅ "顶点色 ---> 法线"
   ✅ "法线 ---> 面角属性"
   ✅ "面角属性 ---> 法线"
   ```

8. **验证偏好设置**
   ```
   编辑 → 偏好设置 → 插件 → Abnormal (展开)
   
   应该看到选项卡:
   ✅ "显示"
   ✅ "行为"
   ✅ "按键映射-选择"
   ✅ "按键映射-快捷键"
   ✅ "按键映射-工具"
   ```

## 📊 修复对比

| 位置 | v2.0 (错误) | v3.0 (正确) |
|------|------------|------------|
| **源代码** | 硬编码中文 | 保持英文原文 |
| **翻译字典** | `("Operator", ...)` | `("*", ...)` |
| **N面板** | ✅ 显示中文 | ✅ 显示中文 |
| **工具栏** | ❌ 显示英文 | ✅ 显示中文 |
| **搜索菜单** | ✅ 显示中文 | ✅ 显示中文 |
| **偏好设置** | ✅ 显示中文 | ✅ 显示中文 |

## 🔍 技术细节

### Blender 翻译系统工作原理

```
1. Blender 读取 UI 代码中的英文文本
   ↓
2. 检查当前用户语言设置 (zh_CN)
   ↓
3. 在翻译字典中查找匹配项
   查找规则: (上下文, "原文") → "译文"
   ↓
4. 如果找到匹配,显示译文
   如果未找到,显示原文
```

### 上下文匹配规则

| 上下文 | 匹配范围 | 使用场景 |
|--------|---------|---------|
| `"*"` | **所有位置** | 通用文本、按钮、标签 |
| `"Operator"` | 操作符搜索菜单 (F3) | 操作符名称 |
| `"Property"` | 属性面板 | 属性描述 |
| `"Menu"` | 菜单项 | 菜单文本 |

**最佳实践**: 对于插件 UI,优先使用 `"*"` 通配符,确保所有位置都能翻译。

### 翻译条目数统计

- **UI 界面**: 6 条
- **操作符**: 11 条
- **模态操作符**: 6 条
- **属性设置**: 11 条
- **显示偏好**: 17 条
- **行为偏好**: 5 条
- **按键映射**: 98 条

**总计**: 154 条翻译

## 🐛 故障排除

### 问题 1: 翻译仍未生效

**解决方法**:
1. 完全卸载插件
2. 关闭 Blender
3. 删除缓存 (可选):
   - Windows: `%APPDATA%\Blender Foundation\Blender\4.x\`
   - macOS: `~/Library/Application Support/Blender/4.x/`
   - Linux: `~/.config/blender/4.x/`
4. 重新启动 Blender
5. 重新安装插件

### 问题 2: 部分文本仍显示英文

**可能原因**:
- 翻译字典中缺少该条目
- 原文拼写不完全匹配 (注意空格、大小写)

**解决方法**:
1. 找到显示英文的文本
2. 在源代码中搜索该文本
3. 确认拼写完全一致
4. 在 `translations.py` 中添加对应条目

### 问题 3: 控制台显示 "翻译系统注册失败"

**可能原因**:
- `translations.py` 文件语法错误
- Python 版本不兼容

**解决方法**:
1. 查看完整错误信息
2. 检查 `translations.py` 语法
3. 确认 Blender 版本 ≥ 4.5.0

## 📚 相关文档

- **汉化说明_v2.md** - 完整安装指南
- **翻译问题排查指南.md** - 详细故障排除
- **翻译对照表.md** - 术语对照表
- **translation_debug.py** - 调试工具脚本

## 📝 版本历史

### v3.0 (2026-01-04) - 修复版
- ✅ 恢复所有源代码为英文原文
- ✅ 修正翻译字典上下文为 `"*"` 通配符
- ✅ 添加缺失的翻译条目
- ✅ 修复 3D 视图工具栏显示英文的问题

### v2.0 (2026-01-04) - 翻译系统版
- ✅ 实现 Blender 官方翻译 API
- ✅ 创建翻译字典文件
- ✅ 添加调试工具
- ❌ 源代码硬编码中文 (错误)
- ❌ 翻译字典上下文错误 (错误)

### v1.0 (2026-01-04) - 初始版
- ❌ 直接修改源代码字符串 (错误方法)
- ❌ 未使用翻译 API

## ⚠️ 重要提醒

1. **必须完全卸载旧版本**: 否则可能导致翻译冲突
2. **必须设置语言为简体中文**: 翻译才会生效
3. **必须查看控制台**: 确认翻译系统注册成功
4. **不要修改源代码中的英文文本**: 保持英文原文,让翻译系统工作

## 许可证

本汉化版遵循原插件的 MIT License 许可证。

---

**修复版本**: v3.0  
**原作者**: Cody Winchester (CodyWinch), Tyler Walker (BeyondDev)  
**原项目**: BNPR Abnormal  
**GitHub**: https://github.com/bnpr/Abnormal  
**文档**: https://bnpr.gitbook.io/abnormal-wiki/
