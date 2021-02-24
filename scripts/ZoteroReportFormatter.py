from bs4 import BeautifulSoup
from bs4.element import Tag
import sys
import re


def getMarkdownHeaders(cells: [list]):

    md = '''<style>
    table th:nth-of-type(1) { width: 15%; }'''

    if '日期' in cells:
        i = cells.index('日期')
        md+= '\ntable th:nth-of-type({}) {{ width: 5%; }}\n'.format(i+1)
    if '作者' in cells:
        i = cells.index('作者')
        md+= '\ntable th:nth-of-type({}) {{ width: 5%; }}\n'.format(i+1)
    md += '''</style>\n|'''
    for v in cells:
        md += v + '|'
    md += '\n'
    md += '|'
    for v in cells:
        md += ':---|'
    md += '\n'
    return md

def getDate(item: [Tag]):
    dateTag = item.find('th', text=re.compile("\\b(日期)"))
    date=''
    if dateTag:
        date = dateTag.parent.td.text
    return date

def getAuthor(item: [Tag]):
    list = item.find_all('th', attrs={'class': 'author'})
    if not list:
        return
    author=list[0].parent.td.text
    for i in range(1,len(list)):
        author+=', '+list[i].parent.td.text
    return author

def fillMarkdown(cells, list):
    md = getMarkdownHeaders(cells)
    lines = ['' for i in range(3)]  # 排序，分别是含科学问题的、仅含普通笔记的、仅含提取笔记的
    for item in list:
        note = item.find('ul', {'class': 'notes'})
        if not note:
            continue
        dic = {x: '' for x in cells}
        dic['标题'] = item.h2.text
        if '日期' in cells:
            dic['日期']=getDate(item)
        if '作者' in cells:
            dic['作者']=getAuthor(item)
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
        for header in cells:
            v = ''
            if header in dic:
                v = dic[header]
            line += v + '|'
        line = line.replace('\n', '')

        line += '\n'

        if '科学问题' in dic and dic['科学问题']:
            lines[0] += line
        elif dic['笔记'].startswith('<p><strong>Extracted Annotations'):
            lines[2] += line
        else:
            lines[1] += line

    for header in lines:
        md += header
    return md


def wyj(list):
    cells = ['标题','日期', '背景', '科学问题', '解决思路', '优点', '缺点', '笔记']
    return fillMarkdown(cells, list)

def lxy(list):
    cells = ['标题', '日期', '作者', '笔记']
    return fillMarkdown(cells, list)

if __name__ == '__main__':
    print('''
[Zotero报告转markdown工具 v0.2]

可通过命令行参数指定style
目前可选：
    1. wyj（默认）： {}
    2. lxy：{}
    
开始处理...
    '''.format(['标题','日期', '背景', '科学问题', '解决思路', '优点', '缺点', '笔记'],
               ['标题', '日期', '作者', '笔记']))

    html = ''
    with open('../text/ZoteroReport.html', 'r', encoding='utf8') as f:
        html = f.read()

    soup = BeautifulSoup(html, features='lxml')
    list = soup.find_all('li', attrs={'class': 'item'})

    style = 'wyj'
    if len(sys.argv) > 1:
        style = sys.argv[1]

    markdown = ''
    if style == 'wyj':
        markdown = wyj(list)
    if style == 'lxy':
        markdown = lxy(list)

    with open('../text/output.md', 'w', encoding='utf8') as f:
        f.write(markdown)

    print('处理结束！')