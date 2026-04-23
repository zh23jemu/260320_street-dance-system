from copy import deepcopy
from pathlib import Path
import shutil

from docx import Document
from docx.enum.text import WD_BREAK, WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt


ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "网站设计毕设论文.docx"
SOURCE = ROOT / "基于JavaScript的街舞信息共享平台设计与实现-毕业论文.docx"
OUTPUT = ROOT / "基于JavaScript的街舞信息共享平台设计与实现-模板版论文.docx"


def clear_paragraph(paragraph):
    """清空段落中的所有运行节点，保留段落本身的样式、缩进和分页属性。"""
    for run in list(paragraph.runs):
        paragraph._p.remove(run._r)


def set_paragraph_text(paragraph, text):
    """在保留模板段落样式的前提下替换文字内容。"""
    clear_paragraph(paragraph)
    paragraph.add_run(text)


def append_page_break(paragraph):
    """在指定段落末尾追加分页符，沿用模板已有的分页节奏。"""
    run = paragraph.add_run()
    run.add_break(WD_BREAK.PAGE)


def remove_body_children_after_index(document, keep_until_index):
    """删除正文中指定位置之后的所有节点，只保留模板封面、声明、摘要等前置结构。"""
    body = document.element.body
    children = list(body.iterchildren())
    sect_pr = None
    if children and children[-1].tag == qn("w:sectPr"):
        sect_pr = deepcopy(children[-1])

    for child in children[keep_until_index + 1 :]:
        body.remove(child)

    if sect_pr is not None:
        body.append(sect_pr)


def remove_all_tables_after_first(document):
    """保留封面信息表，清理模板里原项目遗留的数据表和测试表。"""
    for table in list(document.tables)[1:]:
        table._element.getparent().remove(table._element)


def first_cell_paragraph(cell):
    """返回表格单元格的首个段落，用于安全写入封面信息。"""
    if not cell.paragraphs:
        cell._tc.append(OxmlElement("w:p"))
    return cell.paragraphs[0]


def set_cell_text(cell, text):
    """完整替换单元格文字，避免模板原单元格中的多段文字残留。"""
    cell.text = text


def set_cover_table(document):
    """填充模板封面表格，保留专业、姓名、学号和指导教师等可由用户后续补齐的空位。"""
    table = document.tables[0]
    rows = [
        ("题    目", "基于JavaScript的街舞信息共享平台设计与实现"),
        ("专    业", ""),
        ("学生姓名", ""),
        ("班级学号", ""),
        ("指导教师", ""),
        ("指导单位", ""),
    ]

    for index, (label, value) in enumerate(rows):
        set_cell_text(table.cell(index, 0), label)
        set_cell_text(table.cell(index, 1), value)


def set_basic_template_text(document):
    """替换模板封面、原创性声明和日期中与原项目相关的信息。"""
    replacements = {
        "日期： 2024年1月8日至   2024年6月7日": "日期：2026年3月20日至2026年6月7日",
        "日期：2024年6月7日": "日期：2026年6月7日",
    }

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text in replacements:
            set_paragraph_text(paragraph, replacements[text])
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER if text.startswith("日期： 2024") else paragraph.alignment
        elif text == "本人郑重声明：所提交的毕业设计（论文），是本人在导师指导下，独立进行研究工作所取得的成果。除文中已注明引用的内容外，本毕业设计（论文）不包含任何其他个人或集体已经发表或撰写过的作品成果。对本研究做出过重要贡献的个人和集体，均已在文中以明确方式标明并表示了谢意。":
            set_paragraph_text(
                paragraph,
                "本人郑重声明：所提交的毕业设计（论文），是在导师指导下独立进行研究工作所取得的成果。除文中已经注明引用的内容外，本毕业设计（论文）不包含任何其他个人或集体已经发表或撰写过的作品成果。对本研究做出过重要贡献的个人和集体，均已在文中以明确方式标明并表示谢意。",
            )


def copy_paragraph_style(source, target):
    """尽量复用已有模板段落样式，降低正文与模板格式不一致的概率。"""
    target.style = source.style
    target.alignment = source.alignment
    target.paragraph_format.first_line_indent = source.paragraph_format.first_line_indent
    target.paragraph_format.left_indent = source.paragraph_format.left_indent
    target.paragraph_format.right_indent = source.paragraph_format.right_indent
    target.paragraph_format.space_before = source.paragraph_format.space_before
    target.paragraph_format.space_after = source.paragraph_format.space_after
    target.paragraph_format.line_spacing = source.paragraph_format.line_spacing


def clone_run(source_run, target_paragraph):
    """复制文字运行，尽量继承加粗、字号、字体等基本格式。"""
    new_run = target_paragraph.add_run(source_run.text)
    new_run.bold = source_run.bold
    new_run.italic = source_run.italic
    new_run.underline = source_run.underline
    new_run.font.size = source_run.font.size
    new_run.font.name = source_run.font.name
    if source_run._r.rPr is not None:
        new_run._r.get_or_add_rPr().append(deepcopy(source_run._r.rPr))
    return new_run


def append_paragraph_from_source(document, source_paragraph):
    """把源论文段落追加到模板末尾，保留标题层级和常规正文格式。"""
    target = document.add_paragraph()
    copy_paragraph_style(source_paragraph, target)

    if source_paragraph.runs:
        for run in source_paragraph.runs:
            clone_run(run, target)
    else:
        target.add_run(source_paragraph.text)

    return target


def append_table_from_source(document, source_table):
    """复制源论文表格节点，保留数据库表和测试表的结构。"""
    document.element.body.insert(-1, deepcopy(source_table._element))


def add_picture_placeholder(document, title):
    """插入图片占位区域，后续截图准备好后可直接替换这里。"""
    caption = document.add_paragraph()
    caption.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = caption.add_run(title)
    run.bold = True

    placeholder = document.add_paragraph()
    placeholder.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = placeholder.add_run("【此处预留系统截图位置】")
    run.font.size = Pt(12)

    box = document.add_table(rows=1, cols=1)
    cell = box.cell(0, 0)
    set_paragraph_text(first_cell_paragraph(cell), "\n\n\n\n\n")

    note = document.add_paragraph()
    note.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    note.add_run("（截图待补充）")


def collect_blocks(source_document):
    """按源论文正文顺序收集段落和表格，避免表格被统一挪到文末。"""
    paragraph_map = {paragraph._p: paragraph for paragraph in source_document.paragraphs}
    table_map = {table._element: table for table in source_document.tables}
    blocks = []

    for child in source_document.element.body.iterchildren():
        if child in paragraph_map:
            blocks.append(("paragraph", paragraph_map[child]))
        elif child in table_map:
            blocks.append(("table", table_map[child]))
    return blocks


def append_source_body(document, source_document, body_start_paragraph_index):
    """从源论文的第一章开始追加正文，摘要和封面部分使用模板自身位置。"""
    blocks = collect_blocks(source_document)
    source_body_start_paragraph = source_document.paragraphs[body_start_paragraph_index]
    body_started = False
    pending_placeholders = {
        "2.4 系统总体架构设计": "图2.1 系统总体架构图",
        "2.5 系统功能模块设计": "图2.2 系统功能模块图",
        "3.2.1 用户认证与个人中心实现": "图3.1 登录与个人中心页面截图",
        "3.2.2 活动模块实现": "图3.2 活动模块页面截图",
        "3.2.3 视频模块实现": "图3.3 视频模块页面截图",
        "3.2.4 社交聊天室实现": "图3.4 社交聊天室页面截图",
        "3.2.5 商城模块实现": "图3.5 商城模块页面截图",
    }

    for kind, block in blocks:
        if kind == "paragraph" and block._p is source_body_start_paragraph._p:
            body_started = True

        if not body_started:
            continue

        if kind == "paragraph":
            appended = append_paragraph_from_source(document, block)
            title = block.text.strip()
            if title in pending_placeholders:
                add_picture_placeholder(document, pending_placeholders[title])
            if title in {"第一章 绪论", "第二章 设计方案", "第三章 制作过程分析", "第四章 总结与反思", "结束语", "致谢", "参考文献", "附录"}:
                appended.paragraph_format.page_break_before = True
        elif kind == "table":
            append_table_from_source(document, block)


def find_body_start_index(source_document):
    """定位源论文真正的第一章正文，跳过目录中的“第一章 绪论”文字。"""
    for index, paragraph in enumerate(source_document.paragraphs):
        style_name = paragraph.style.name if paragraph.style else ""
        if paragraph.text.strip() == "第一章 绪论" and style_name.startswith("Heading"):
            return index
    raise RuntimeError("未能在源论文中定位到真正的“第一章 绪论”。")


def find_body_child_index_by_text(document, text):
    """在Word正文XML中按段落文字查找节点位置，用于删除模板旧正文。"""
    for index, child in enumerate(document.element.body.iterchildren()):
        if child.tag == qn("w:p"):
            texts = [node.text for node in child.iter(qn("w:t")) if node.text]
            if "".join(texts).strip() == text:
                return index
    raise RuntimeError(f"未能在模板中定位到“{text}”。")


def remove_body_children_from_index(document, start_index):
    """删除正文中指定位置及之后的节点，只保留前面的模板封面和声明。"""
    body = document.element.body
    children = list(body.iterchildren())
    sect_pr = None
    if children and children[-1].tag == qn("w:sectPr"):
        sect_pr = deepcopy(children[-1])

    for child in children[start_index:]:
        body.remove(child)

    if sect_pr is not None:
        body.append(sect_pr)


def append_source_front(document, source_document, body_start_index):
    """把源论文的摘要、英文摘要和目录追加到模板声明之后，不带入源论文封面。"""
    source_paragraphs = source_document.paragraphs
    abstract_start = next(
        index for index, paragraph in enumerate(source_paragraphs) if paragraph.text.strip() == "摘  要"
    )

    for paragraph in source_paragraphs[abstract_start:body_start_index]:
        if paragraph.text.strip():
            append_paragraph_from_source(document, paragraph)


def main():
    """复制论文模板并填充街舞信息共享平台论文内容。"""
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"未找到模板文件：{TEMPLATE}")
    if not SOURCE.exists():
        raise FileNotFoundError(f"未找到源论文内容文件：{SOURCE}")

    shutil.copyfile(TEMPLATE, OUTPUT)
    document = Document(OUTPUT)
    source_document = Document(SOURCE)

    set_cover_table(document)
    set_basic_template_text(document)

    # 模板从“摘  要”开始仍是原项目内容，需要整体替换为街舞平台论文内容。
    template_abstract_index = find_body_child_index_by_text(document, "摘  要")
    source_body_start_index = find_body_start_index(source_document)
    remove_body_children_from_index(document, template_abstract_index)
    remove_all_tables_after_first(document)
    append_source_front(document, source_document, source_body_start_index)
    append_source_body(document, source_document, source_body_start_index)

    document.save(OUTPUT)
    print(f"已生成：{OUTPUT}")


if __name__ == "__main__":
    main()
