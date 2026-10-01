# -*- coding: utf-8 -*-
import io
t = io.open('.workbuddy/memory/PAGES.md', 'r', encoding='utf-8', newline='').read()
i = t.find(u'一字不动')
print(t[i - 40:i + 180])
print('--- 结构图 ---')
j = t.find(u'\u251c section.td-mod.td-mod-term')
print(t[j:j + 260])
print('--- 固定事实表新增行 ---')
k = t.find(u'**\u7ec8\u7aef\u6807\u7b7e\u6761**')
print(t[k - 120:k + 120])
