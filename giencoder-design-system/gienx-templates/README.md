# gienx-templates 页面模板工程化说明

> 目的：作为「页面模板」框架，未来在此基础上填充内容并新增更多页面模板。
> 硬约束：最终交付为零依赖、可离线静态浏览的自包含单文件。

## 目录契约

```
gienx-templates/
├── _shared/                  # ① 共享层（跨模板复用，唯一权威源）
│   ├── tokens.css            # 源启 Design Token（= colors_and_type.css）
│   └── components.css        # 源启核心组件样式
│
├── workbench/                # ② 首个模板范例（其它模板同此契约）
│   ├── index.html            # 页面骨架：<head> 内以 <link> 引用共享层与专属样式，
│   │                         #        底部以 <script src> 引用专属逻辑
│   ├── styles/workbench.css  # 本模板专属样式（页面级，只写本页的）
│   └── scripts/workbench.js  # 本模板专属交互逻辑
│
├── dashboard/  list-page/ …  # 未来新增模板（同 workbench 目录契约，各建 index.html）
│
├── build.py                  # 构建脚本：骨架 → 自包含单文件
└── dist/
    └── <template>/index.html # ③ 构建产物（自包含单文件，给交付 / 线上离线浏览）
```

## 新增一个模板的步骤

1. `mkdir gienx-templates/<name>/{styles,scripts}`，新建 `index.html`
2. 骨架里引用资源（相对路径，`.` 为模板根）：
   ```html
   <!-- 共享 token / 组件 -->
   <link rel="stylesheet" href="../_shared/tokens.css">
   <link rel="stylesheet" href="../_shared/components.css">
   <!-- 本模板专属 -->                               
   <link rel="stylesheet" href="styles/<name>.css">
   <script src="scripts/<name>.js"></script>
   ```
   > `_shared` 位于 `gienx-templates/_shared/`，模板位于 `gienx-templates/<name>/`，所以是 `../_shared/`。
3. 专属样式只写本页用到的（尽量只用 Design Token，不硬编码 hex）。
4. 可选：若新组件被多个模板复用，抽到 `_shared/`（如新增 `_shared/<token>.css`）。
5. 构建生成自包含单文件：
   ```
   python3 gienx-templates/build.py <name>
   ```
   产物在 `gienx-templates/dist/<name>/index.html`。

## 构建脚本

`python3 gienx-templates/build.py [template] --verify`
- 不传 template → 构建全部模板
- `--verify`：校验后打印提示

构建逻辑：把骨架中指向 `./`、`../_shared/` 的 `<link rel="stylesheet">` 与 `<script src>` 逐个内联；
自动剥离源文件自带的 `<style></style>` / `<script></script>` 外壳，统一包一层，避免嵌套。

## 交付规范

- **源码**（`gienx-templates/<name>/` 骨架 + styles + scripts）用于维护与二次开发。
- **交付/离线浏览** 一律使用构建产物 `gienx-templates/dist/<name>/index.html`（自包含）。
- 对外有多份 delivery 副本时，必须从 `dist/<name>/index.html` 复制，保证三份一致（用 md5 校验，改动产物前先比对）。
- 构建产物发布后，勿再手工改单文件；改源码 → 重新 build → 再同步。

## 当前状态

- `_shared/` 已从权威源建立（tokens.css = giencoder/colors_and_type.css，components.css = giencoder/components.css）。
- workbench 已按「骨架 + 专属 + 构建产物」落地；产物三份 md5 一致，无外部引用，可离线静态浏览。
- 已根治原单文件把 tokens/components 各内联两次导致的 ~70KB 冗余（183KB → 114KB）。
