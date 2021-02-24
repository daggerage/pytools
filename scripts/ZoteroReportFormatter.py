from bs4 import BeautifulSoup

html = ''
with open('../text/ZoteroReport.html', 'r', encoding='utf8') as f:
    html = f.read()

soup = BeautifulSoup(html,features='lxml')
list = soup.find_all('li', attrs={'class': 'item'})
cells = ['标题', '背景', '科学问题', '解决思路', '优点', '缺点', '笔记']
md = '''
<style> table th:nth-of-type(1) { width: 15%; } </style>
|'''
for v in cells:
    md += v + '|'
md += '\n'
md += '|'
for v in cells:
    md += ':---|'
md += '\n'
lines = ['' for i in range(3)]  # 排序，分别是含科学问题的、仅含普通笔记的、仅含提取笔记的
for item in list:
    note = item.find('ul', {'class': 'notes'})
    if not note:
        continue
    dic = {x: '' for x in cells}
    dic['标题'] = item.h2.text
    intoCellAt = -1
    for tag in note.contents[1].contents[1].contents:
        content = str(tag)
        # 先判断是哪一种文字
        for k in cells:
            if type(tag) == str:
                break
            elif tag.string and tag.string.startswith(k):
                intoCellAt = cells.index(k)
                content = content.replace(k, '', 1).replace('：', '', 1)
        # 如果没任何标记，直接写入“笔记”
        if intoCellAt == -1:
            dic['笔记'] += content
        # 如果有标记，写到对应标记里
        else:
            dic[cells[intoCellAt]] += content
    line = '|'
    for v in cells:
        line += dic[v] + '|'
    line = line.replace('\n', '')

    line += '\n'

    if dic['科学问题']:
        lines[0] += line
    elif dic['笔记'].startswith('<p><strong>Extracted Annotations'):
        lines[2] += line
    else:
        lines[1] += line

for v in lines:
    md += v
with open('../text/output.md', 'w', encoding='utf8') as f:
    f.write(md)
