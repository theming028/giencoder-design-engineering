#!/usr/bin/env python3
"""
GienCoder Design Engineering — 构建后质量验证脚本
参考 Vibe Designing Playbook 的 evaluator-rubric + gaps.log 思路
用法：python3 verify-design.py <pages-dir>
"""

import sys
import os
import re
from pathlib import Path

# ── 设计系统 Token 白名单 ──
TOKEN_PATTERNS = [
    r'var\(--color-',
    r'var\(--font-size-',
    r'var\(--font-family',
    r'var\(--border-radius-',
    r'var\(--spacing-',
    r'var\(--transition-',
]

# 允许的硬编码色值（设计稿 DevMode 直接给的，不强制改 token）
ALLOWED_HEX = {
    '#FFFFFF', '#FFF', '#ffffff', '#fff',
    '#E4E6EA', '#E5E5E5', '#E9ECEE', '#ECEEF2',
    '#F2F2F2', '#F3F4F5', '#F4F5F6',
    '#1E1E1E', '#1F1F1F', '#3770F7', '#7766FD',
    '#6B6B6B', '#868686', '#8E8E8E', '#A9A9A9', '#BEBEBE',
    '#A0BAF7', '#D3E2FF', '#ECF2FF',
    '#DAE3ED', '#E2E3E4',
    'rgba(255, 255, 255, 0.85)', 'rgba(255, 255, 255, 0.88)',
    'rgba(255, 255, 255, 0.5)', 'rgba(255, 255, 255, 0.9)',
    'rgba(0, 0, 0, 0.04)', 'rgba(0, 0, 0, 0.08)', 'rgba(0, 0, 0, 0.1)',
    'rgba(55, 112, 247, 0.12)',
}

# ── 检查规则 ──

class Issue:
    def __init__(self, severity, rule, file, line, desc, source=None, fix=None):
        self.severity = severity  # 🔴 critical / 🟡 warning / 🔵 info
        self.rule = rule
        self.file = file
        self.line = line
        self.desc = desc
        self.source = source or ''
        self.fix = fix or ''

    def __str__(self):
        s = f"{self.severity} [{self.rule}] {self.file}"
        if self.line:
            s += f":{self.line}"
        s += f"\n  问题: {self.desc}"
        if self.source:
            s += f"\n  代码: {self.source[:120]}"
        if self.fix:
            s += f"\n  修复: {self.fix}"
        return s


def check_hardcoded_hex(content, filename):
    """检查 CSS 上下文里的硬编码 hex 色值（SVG path fill 属性除外）"""
    issues = []
    # 只检查 CSS 属性：color/background/border-color/boxShadow 后面跟 hex
    # 排除 SVG path 的 fill:`#XXX`（JS 字符串，不是 CSS）
    css_hex_pattern = re.compile(
        r'(?<!fill[`:])'  # 不在 fill: 后面
        r'(?:color|background|borderColor|border-color|boxShadow|box-shadow)'
        r'\s*[`:]\s*'
        r'(?![^`]*var\()'  # 同行没有 var(
        r'(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8}))',
        re.IGNORECASE
    )
    
    for i, line in enumerate(content.split('\n'), 1):
        if '<!--' in line or '/*' in line:
            continue
        
        for match in css_hex_pattern.finditer(line):
            hex_val = match.group(1)
            in_whitelist = any(hex_val.lower() == w.lower() for w in ALLOWED_HEX)
            if not in_whitelist:
                issues.append(Issue(
                    '🟡', 'TOKEN-GAP', filename, i,
                    f'CSS 硬编码色值 {hex_val}，应使用设计系统变量 var(--color-*)',
                    line.strip()[:120],
                    '查 giencoder-design-system/tokens.md 找对应 token，记入 gaps.log'
                ))
    return issues


def check_hardcoded_px_fontsize(content, filename):
    """检查硬编码 px 字号（应该用 var(--font-size-*)）"""
    issues = []
    # 匹配 font-size: XXpx 或 fontSize:XXpx
    px_pattern = re.compile(r'font-?size[`:]*\s*(\d+)px', re.IGNORECASE)
    # 也匹配 font: ... XXpx/...
    font_shorthand = re.compile(r'font[`:]*\s*\d+\s*([^/]+/[^;}`]+)', re.IGNORECASE)
    
    for i, line in enumerate(content.split('\n'), 1):
        if 'var(--font' in line:
            continue
        matches = px_pattern.findall(line)
        for m in matches:
            issues.append(Issue(
                '🟡', 'TOKEN-GAP', filename, i,
                f'硬编码字号 {m}px，应使用 var(--font-size-*)',
                line.strip()[:120],
                '查 giencoder-design-system/tokens.md 找对应 font-size token'
            ))
    return issues


def check_animation_duration(content, filename):
    """检查动画时长超过 300ms（craft.md 约束）"""
    issues = []
    # 匹配 animation: ... Xms 或 transition: ... Xms
    dur_pattern = re.compile(r'(?:animation|transition)[^;}`]*?(\d+)ms', re.IGNORECASE)
    
    for i, line in enumerate(content.split('\n'), 1):
        matches = dur_pattern.findall(line)
        for m in matches:
            ms = int(m)
            if ms > 300:
                issues.append(Issue(
                    '🟡', 'CRAFT-ANIM', filename, i,
                    f'动画时长 {ms}ms 超过 300ms 上限（craft.md: UI 动画不超过 300ms）',
                    line.strip()[:120],
                    '缩短到 300ms 以内，或说明为什么需要更长（如骨架屏过渡）'
                ))
    return issues


def check_missing_states(content, filename):
    """检查缺失的空态/加载态/错误态（spec.md: L5 边界条件）"""
    issues = []
    page_name = Path(filename).stem
    
    # 只检查有交互的页面（base/dev 有输入框和列表）
    interactive_pages = ['base', 'dev']
    if page_name not in interactive_pages:
        return issues
    
    checks = {
        '空态(empty)': [r'空态', r'empty', r'暂无', r'no data', r'placeholder'],
        '加载态(loading)': [r'loading', r'加载', r'skeleton', r'骨架', r'spin', r'animate-spin'],
        '错误态(error)': [r'error', r'错误', r'失败', r'重试', r'retry'],
    }
    
    for state, patterns in checks.items():
        found = False
        for p in patterns:
            if re.search(p, content, re.IGNORECASE):
                found = True
                break
        if not found:
            issues.append(Issue(
                '🔵', 'SPEC-L5', filename, '',
                f'页面未检测到 {state} 相关文案/组件（spec.md L5: 边界条件）',
                '',
                f'检查 {page_name} 页面是否有 {state} 的 UI 处理'
            ))
    return issues


def check_ai_slop(content, filename):
    """检查 AI Slop 特征（craft.md: 避免无意义动效、层级平均化）"""
    issues = []
    
    # 检查等大白卡（grid grid-cols-N gap-N 连续出现 4+ 个相同卡片）
    card_pattern = re.compile(r'rounded.*border.*p-\d.*bg-')
    card_count = len(card_pattern.findall(content))
    if card_count >= 8:
        issues.append(Issue(
            '🔵', 'CRAFT-SLOP', filename, '',
            f'检测到 {card_count} 个卡片样式元素，可能存在"等大白卡"问题（craft.md: 避免等大白卡和无层级网格）',
            '',
            '检查是否有层级变化，避免所有卡片视觉权重相同'
        ))
    
    # 检查无意义渐变背景
    gradient_count = len(re.findall(r'linear-gradient|radial-gradient|conic-gradient', content, re.IGNORECASE))
    if gradient_count >= 3:
        issues.append(Issue(
            '🔵', 'CRAFT-SLOP', filename, '',
            f'检测到 {gradient_count} 处渐变，可能过度装饰（craft.md: 品牌色一屏不超过 3 处重点使用）',
            '',
            '检查渐变是否必要，克制使用'
        ))
    
    return issues


def check_component_misuse(content, filename):
    """检查组件误用（components.md: Badge vs Tag, Dialog vs Drawer）"""
    issues = []
    
    # 检查 Badge 和 Tag 是否混用
    # Badge 用于状态/计数/风险，Tag 用于分类/类型/环境
    badge_in_tag_context = re.findall(r'<span[^>]*class="[^"]*tag[^"]*"[^>]*>(运行中|失败|完成|排队|超时)', content, re.IGNORECASE)
    for m in badge_in_tag_context:
        issues.append(Issue(
            '🟡', 'COMPONENT', filename, '',
            f'状态词 "{m}" 用在 Tag 上下文里，应使用 Badge（components.md: Badge 表达状态，Tag 表达分类）',
            '',
            '将状态展示从 Tag 改为 Badge 组件'
        ))
    
    return issues


def check_border_compensation(content, filename):
    """检查 border + box-sizing:border-box 容器的子元素坐标补偿"""
    issues = []
    
    # 找到有 border + box-sizing:border-box 的容器
    border_box_pattern = re.compile(r'box-sizing[^;}`]*border-box[^;}`]*border[^;}`]*1px', re.IGNORECASE)
    if border_box_pattern.search(content):
        # 检查同文件里是否有 position:absolute 的子元素
        abs_children = re.findall(r'position[`:]*absolute.*?left[`:]*\d+', content, re.IGNORECASE)
        # 这个检查比较粗，只做提示
        if abs_children:
            # 检查是否有 left:0 的子元素（可能没做补偿）
            for match in abs_children[:5]:
                if 'left:0' in match or 'left:`0`' in match:
                    issues.append(Issue(
                        '🔵', 'BORDER-COMP', filename, '',
                        'border+border-box 容器内有 position:absolute 子元素 left:0，可能需要 border 宽度补偿',
                        match[:80],
                        '子元素 left/top 减去 border 宽度（通常 1px）'
                    ))
                    break
    
    return issues


def generate_gaps_log(issues, output_dir):
    """生成 gaps.log：记录找不到 token 的硬编码值"""
    gaps = []
    for issue in issues:
        if issue.rule == 'TOKEN-GAP':
            gaps.append(f"{issue.file}:{issue.line} — {issue.desc}")
    
    if gaps:
        gaps_path = os.path.join(output_dir, 'gaps.log')
        with open(gaps_path, 'w', encoding='utf-8') as f:
            f.write('# gaps.log — 设计系统 Token 缺口记录\n')
            f.write('# 以下硬编码值未找到对应的设计系统 token，需手动补充\n\n')
            for g in gaps:
                f.write(g + '\n')
        return gaps_path
    return None


def main():
    if len(sys.argv) < 2:
        print("用法: python3 verify-design.py <pages-dir>")
        print("示例: python3 verify-design.py /Users/shaoyuming/Documents/GienCoderDesignEngineering/pages")
        sys.exit(1)
    
    pages_dir = sys.argv[1]
    if not os.path.isdir(pages_dir):
        print(f"❌ 目录不存在: {pages_dir}")
        sys.exit(1)
    
    html_files = sorted(Path(pages_dir).glob('*.html'))
    if not html_files:
        print(f"❌ 未找到 HTML 文件: {pages_dir}")
        sys.exit(1)
    
    print(f"╔══════════════════════════════════════════════════════════")
    print(f"║ GienCoder Design Engineering — 质量验证报告")
    print(f"║ 扫描 {len(html_files)} 个 HTML 文件")
    print(f"╚══════════════════════════════════════════════════════════\n")
    
    all_issues = []
    summary = {'🔴': 0, '🟡': 0, '🔵': 0}
    
    for html_file in html_files:
        filename = html_file.name
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_issues = []
        file_issues += check_hardcoded_hex(content, filename)
        file_issues += check_hardcoded_px_fontsize(content, filename)
        file_issues += check_animation_duration(content, filename)
        file_issues += check_missing_states(content, filename)
        file_issues += check_ai_slop(content, filename)
        file_issues += check_component_misuse(content, filename)
        file_issues += check_border_compensation(content, filename)
        
        if file_issues:
            print(f"┌─ {filename} ({len(file_issues)} issues)")
            for issue in file_issues:
                print(f"│ {issue}")
                summary[issue.severity] = summary.get(issue.severity, 0) + 1
                all_issues.append(issue)
            print(f"└─\n")
        else:
            print(f"✅ {filename} — 无问题\n")
    
    # 生成 gaps.log
    gaps_path = generate_gaps_log(all_issues, pages_dir)
    
    # 汇总
    print(f"{'═' * 58}")
    print(f"汇总: {len(all_issues)} 个问题")
    print(f"  🟡 warning:  {summary.get('🟡', 0)} — 需修复")
    print(f"  🔵 info:     {summary.get('🔵', 0)} — 建议检查")
    print(f"  🔴 critical: {summary.get('🔴', 0)} — 必须修复")
    
    if gaps_path:
        print(f"\n📄 Token 缺口记录: {gaps_path}")
    
    # 退出码：有 🟡 或 🔴 就非 0
    if summary.get('🟡', 0) > 0 or summary.get('🔴', 0) > 0:
        sys.exit(1)
    else:
        print("\n✅ 质量门禁通过")
        sys.exit(0)


if __name__ == '__main__':
    main()
