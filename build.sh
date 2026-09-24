#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# GienCoder Design Engineering — 构建脚本
# 为每个页面生成独立 HTML，共享 CSS/JS 分离到 assets/ 目录
# ═══════════════════════════════════════════════════════════
set -e

PROJECT_DIR="/private/tmp/cloudai-demo"
OUTPUT_DIR="/Users/shaoyuming/Documents/GienCoderDesignEngineering/pages"

echo "🧹 清理旧产物..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

cd "$PROJECT_DIR"

# 用多入口构建（分离 CSS/JS）
echo "📦 构建中..."
export PATH="/usr/local/bin:$PATH"
node ./node_modules/.bin/vite build 2>&1 | tail -15

# 移动 HTML 到根目录（Vite 会放到 src/pages/entries/ 下）
cd "$OUTPUT_DIR"
if [ -d "src/pages/entries" ]; then
  mv src/pages/entries/*.html .
  rm -rf src
fi

# 生成首页导航
cat > index.html << 'NAV'
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GienCoder Design Engineering — 页面导航</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, system-ui, sans-serif; background: #F4F5F6; color: #1E1E1E; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
    .container { max-width: 640px; width: 100%; padding: 40px; }
    h1 { font-size: 24px; font-weight: 600; margin-bottom: 8px; }
    p { color: #8E8E8E; font-size: 14px; margin-bottom: 24px; }
    .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
    a { display: flex; flex-direction: column; gap: 4px; padding: 20px; background: #fff; border: 1px solid #ECEEF2; border-radius: 12px; text-decoration: none; color: inherit; transition: border-color 0.2s, box-shadow 0.2s; }
    a:hover { border-color: #3770F7; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    a strong { font-size: 15px; font-weight: 500; }
    a span { font-size: 12px; color: #8E8E8E; }
  </style>
</head>
<body>
  <div class="container">
    <h1>GienCoder Design Engineering</h1>
    <p>点击进入对应页面，或用本地服务器预览（python3 serve.py）</p>
    <div class="grid">
      <a href="base.html"><strong>基础工作台</strong><span>对话框 + 工作空间切换</span></a>
      <a href="dev.html"><strong>研发工作台</strong><span>代码仓库 + 构建</span></a>
      <a href="avatar.html"><strong>数字分身</strong><span>AI 分身管理</span></a>
      <a href="automation.html"><strong>自动化</strong><span>定时任务编排</span></a>
      <a href="skills.html"><strong>技能 Skills</strong><span>能力与工作流</span></a>
      <a href="settings.html"><strong>设置</strong><span>外观 / 账户 / 通知</span></a>
    </div>
  </div>
</body>
</html>
NAV

# 生成 serve.py（一键启动本地预览）
cat > serve.py << 'SERVE'
#!/usr/bin/env python3
"""GienCoder Design Engineering — 本地预览服务器
用法：python3 serve.py
然后浏览器打开 http://localhost:8080
"""
import http.server
import sys

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

if __name__ == '__main__':
    print(f'🚀 启动预览服务器: http://localhost:{PORT}')
    print(f'   按 Ctrl+C 停止')
    http.server.HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
SERVE

echo ""
echo "✅ 构建完成！"
echo ""
echo "📁 文件结构："
find . -type f | sort
echo ""
echo "🔗 预览方式："
echo "   方式1（本地服务器，推荐）：cd $OUTPUT_DIR && python3 serve.py"
echo "   方式2（直接打开）：用浏览器打开 index.html"
