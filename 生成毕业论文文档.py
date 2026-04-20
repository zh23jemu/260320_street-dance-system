from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


OUTPUT = Path("基于JavaScript的街舞信息共享平台设计与实现-毕业论文.docx")


def xml_text(text):
    """将普通文本转为 Word XML 安全文本，避免特殊符号破坏文档结构。"""
    return escape(str(text), {"'": "&apos;", '"': "&quot;"})


def run_text(text):
    """生成一个文字运行节点，保留中文、英文和必要空格。"""
    return f'<w:r><w:t xml:space="preserve">{xml_text(text)}</w:t></w:r>'


def paragraph(text="", style=None, align=None, bold=False, page_break=False):
    """生成段落节点，可控制标题样式、居中、加粗和分页。"""
    props = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        props.append(f'<w:jc w:val="{align}"/>')
    ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else ""
    if page_break:
        return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    if bold:
        return f'<w:p>{ppr}<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{xml_text(text)}</w:t></w:r></w:p>'
    return f"<w:p>{ppr}{run_text(text)}</w:p>"


def table(rows):
    """生成简洁三线表风格的 Word 表格，用于数据库设计和测试用例展示。"""
    cells_xml = []
    for row in rows:
        cell_parts = []
        for cell in row:
            cell_parts.append(
                "<w:tc>"
                "<w:tcPr><w:tcW w:w=\"2400\" w:type=\"dxa\"/></w:tcPr>"
                f"{paragraph(cell)}"
                "</w:tc>"
            )
        cells_xml.append(f"<w:tr>{''.join(cell_parts)}</w:tr>")
    return (
        "<w:tbl>"
        "<w:tblPr>"
        "<w:tblStyle w:val=\"TableGrid\"/>"
        "<w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "</w:tblPr>"
        f"{''.join(cells_xml)}"
        "</w:tbl>"
    )


def h1(text):
    return paragraph(text, style="Heading1")


def h2(text):
    return paragraph(text, style="Heading2")


def h3(text):
    return paragraph(text, style="Heading3")


sections = []

# 封面与声明内容按原模板的论文结构组织，具体信息可由学生后续填写。
sections.extend(
    [
        paragraph("南京邮电大学", align="center", bold=True),
        paragraph("毕 业 设 计（论 文）", align="center", bold=True),
        paragraph("", align="center"),
        paragraph("题    目", align="center"),
        paragraph("基于JavaScript的街舞信息共享平台设计与实现", align="center", bold=True),
        paragraph("专    业", align="center"),
        paragraph("学生姓名", align="center"),
        paragraph("班级学号", align="center"),
        paragraph("指导教师", align="center"),
        paragraph("指导单位", align="center"),
        paragraph("日期：2026年3月20日至2026年6月7日", align="center"),
        paragraph(page_break=True),
        h1("毕业设计（论文）原创性声明"),
        paragraph(
            "本人郑重声明：所提交的毕业设计（论文），是在导师指导下独立进行研究工作所取得的成果。"
            "除文中已经注明引用的内容外，本毕业设计（论文）不包含任何其他个人或集体已经发表或撰写过的作品成果。"
            "对本研究做出过重要贡献的个人和集体，均已在文中以明确方式标明并表示谢意。"
        ),
        paragraph("论文作者签名："),
        paragraph("日期：2026年6月7日"),
        paragraph(page_break=True),
    ]
)

sections.extend(
    [
        h1("摘  要"),
        paragraph(
            "随着街舞文化从线下社群走向大众传播，街舞赛事、商演招募、舞房交流、作品展示和周边商品交易等需求不断增加。"
            "但在实际使用场景中，街舞相关信息往往分散在社交媒体、微信群、公众号和线下渠道中，用户需要在多个平台之间反复切换，"
            "活动主办方也难以高效触达目标舞者。针对这一问题，本文设计并实现了一个基于JavaScript的街舞信息共享平台，"
            "希望通过统一的Web入口整合活动发布与报名、视频分享与互动、分类聊天室、街舞商城以及个人中心等功能，为舞者、"
            "爱好者、活动组织者和商家提供较完整的线上服务闭环。"
        ),
        paragraph(
            "系统采用前后端分离架构。前端使用JavaScript、HTML5、CSS3、React 19、React Router和Vite完成页面展示与交互逻辑；"
            "后端使用Python、Django 6和Django ORM实现业务接口、用户认证、数据模型和后台管理能力；数据库采用SQLite存储用户、"
            "活动、报名、视频、评论、聊天室、消息、商品、购物车、订单、收藏和关注等结构化数据。系统实现了注册登录、个人资料维护、"
            "活动发布、报名、签到、收藏、视频发布、点赞、评论、分类聊天室发言、商品浏览、加入购物车、创建订单、模拟支付和个人中心统计等功能。"
        ),
        paragraph(
            "通过功能测试与联调验证，系统能够完成街舞信息共享平台的主要业务流程，页面结构清晰，模块边界明确，具备较好的可维护性和扩展性。"
            "本课题的实现表明，将React前端与Django后端结合用于垂直文化社区平台开发具有较好的可行性，可为街舞信息整合、社群互动和商业服务提供基础支撑。"
        ),
        paragraph("关键词：街舞信息共享平台；JavaScript；React；Django；SQLite"),
        h1("ABSTRACT"),
        paragraph(
            "With the rapid development of street dance culture, demands for events, performances, recruitment, work sharing, community communication and related commerce are increasing. "
            "However, street-dance information is often scattered across social media, chat groups, public accounts and offline communities, which causes high information acquisition costs and inefficient resource matching. "
            "To address this problem, this thesis designs and implements a JavaScript-based street dance information sharing platform. "
            "The platform integrates activity publishing and registration, video sharing and interaction, categorized chat rooms, a street-dance mall and a personal center into one web application."
        ),
        paragraph(
            "The system adopts a front-end and back-end separated architecture. The front end is built with JavaScript, HTML5, CSS3, React 19, React Router and Vite, while the back end is implemented with Python, Django 6 and Django ORM. "
            "SQLite is used to store structured data including users, activities, registrations, videos, comments, chat rooms, messages, products, cart items, orders, favorites and follows. "
            "The implemented functions include registration and login, profile management, activity publishing, registration and check-in, video publishing, likes, comments, categorized chat, shopping cart, order creation, simulated payment and personal dashboard statistics."
        ),
        paragraph(
            "Functional tests show that the main business processes of the platform can run correctly. The system has clear module boundaries, good maintainability and basic extensibility. "
            "The project demonstrates that combining React and Django is feasible for building a vertical cultural community platform."
        ),
        paragraph("Key words: Street Dance Information Sharing Platform; JavaScript; React; Django; SQLite"),
        paragraph(page_break=True),
    ]
)

sections.extend(
    [
        h1("目  录"),
        paragraph("第一章 绪论"),
        paragraph("1.1 研究背景"),
        paragraph("1.2 研究意义"),
        paragraph("1.3 国内外研究现状"),
        paragraph("1.4 毕设主要工作"),
        paragraph("第二章 设计方案"),
        paragraph("2.1 网站开发技术介绍"),
        paragraph("2.2 网站开发工具介绍"),
        paragraph("2.3 用户需求调研分析"),
        paragraph("2.4 系统总体架构设计"),
        paragraph("2.5 系统功能模块设计"),
        paragraph("2.6 数据库表结构设计"),
        paragraph("第三章 制作过程分析"),
        paragraph("3.1 系统开发环境搭建"),
        paragraph("3.2 系统功能模块实现"),
        paragraph("3.3 前后端接口联调"),
        paragraph("3.4 功能测试"),
        paragraph("第四章 总结与反思"),
        paragraph("4.1 总结"),
        paragraph("4.2 反思"),
        paragraph("结束语"),
        paragraph("致谢"),
        paragraph("参考文献"),
        paragraph("附录"),
        paragraph(page_break=True),
    ]
)

sections.extend(
    [
        h1("第一章 绪论"),
        h2("1.1 研究背景"),
        h3("1.1.1 街舞文化数字化传播需求持续增长"),
        paragraph(
            "街舞是一种兼具竞技性、艺术性和社群性的青年文化形式。随着街舞综艺节目、城市赛事、商业演出、舞房培训和高校社团的发展，"
            "街舞已经从相对小众的线下圈层逐步进入更广泛的大众视野。不同风格的舞种，如Hiphop、Jazz、Popping、Locking、Breaking等，"
            "吸引了大量学习者和爱好者参与。街舞用户在成长过程中不仅需要获取比赛、公开课、商演和伴舞招募信息，也需要观看作品、分享训练经验、"
            "寻找练习伙伴，并购买服装、鞋帽、护具等相关商品。"
        ),
        paragraph(
            "目前街舞领域的信息传播仍然较为分散。活动信息可能发布在公众号、短视频平台或微信群中，视频作品主要依赖通用内容平台，"
            "舞房招聘和比赛经验则常常沉淀在即时通讯群聊中，商城服务又分布在不同电商平台。信息来源碎片化导致用户获取成本较高，"
            "主办方和商家也难以面向精准人群进行信息分发。对于普通爱好者来说，错过报名时间、不了解活动地点、无法找到合适交流群等问题比较常见；"
            "对于活动组织者来说，报名管理、签到统计和用户沉淀也缺少统一工具。"
        ),
        h3("1.1.2 垂直信息平台具有现实应用价值"),
        paragraph(
            "通用社交平台虽然具有较强的流量优势，但在垂直场景下往往缺乏结构化管理能力。街舞信息共享平台需要围绕街舞用户的真实行为链路进行设计，"
            "将活动、作品、交流、消费和个人资料管理整合在同一系统中。通过统一的数据模型和页面入口，平台能够降低用户查找信息的成本，"
            "也能让活动报名、视频互动、聊天室交流和商品订单之间形成关联，为后续的推荐、统计和运营提供基础。"
        ),
        paragraph(
            "因此，开发一个面向街舞领域的垂直Web平台，不仅可以作为毕业设计中前后端分离开发、数据库设计和交互实现的综合实践，"
            "也具有一定的现实意义。该平台以服务街舞用户为核心，通过现代Web技术完成信息共享和社区互动，体现了软件工程技术在文化社群场景中的应用价值。"
        ),
        h2("1.2 研究意义"),
        paragraph(
            "从用户角度看，平台为舞者和爱好者提供了统一入口。用户可以在活动模块查看赛事、商演、公开课和伴舞等信息，完成报名、收藏与签到；"
            "可以在视频模块发布自己的作品，与其他用户进行点赞、评论和收藏互动；可以在社交模块进入不同舞种或主题聊天室进行交流；"
            "还可以在商城模块浏览街舞相关商品并完成购物车、订单和模拟支付流程。个人中心则集中展示用户的发布、报名、收藏、关注和订单信息，"
            "方便用户回顾自己的平台行为。"
        ),
        paragraph(
            "从技术角度看，本课题覆盖了前端单页应用、后端接口、会话认证、数据库关系设计、业务校验、前后端联调和功能测试等内容。"
            "前端使用React和Vite实现组件化页面组织，后端使用Django框架和SQLite数据库完成业务逻辑与数据持久化。"
            "这种组合适合毕业设计阶段快速构建功能完整、结构清晰、可演示的Web平台，也能为后续升级到更复杂的部署方案、实时通信和推荐系统打下基础。"
        ),
        h2("1.3 国内外研究现状"),
        paragraph(
            "在信息共享平台研究方面，国内外已有大量针对垂直社区、内容分享平台和电子商务系统的研究。相关研究普遍认为，垂直平台的价值在于围绕特定用户群体和场景，"
            "对内容、关系和服务进行结构化整合。与综合门户或通用社交平台相比，垂直平台更强调精准匹配、功能闭环和社区归属感。"
        ),
        paragraph(
            "在Web前端技术方面，HTML5、CSS3和JavaScript已经成为现代网页开发的基础。React等前端框架通过组件化思想将页面拆分为可维护的模块，"
            "能够提升单页应用开发效率。Vite等构建工具进一步优化了开发启动和热更新体验，适合中小型系统快速迭代。"
            "本系统前端正是基于React组件划分，将首页、登录页、活动页、视频页、社交页、商城页和个人中心页分别组织，使页面逻辑更加清晰。"
        ),
        paragraph(
            "在后端开发方面，Django是成熟的Python Web框架，提供了路由、视图、ORM、认证、后台管理和安全中间件等能力。"
            "对于毕业设计类型的系统而言，Django能够在较短时间内搭建稳定的业务接口，并通过模型类清晰描述数据库结构。"
            "本系统后端按照用户、活动、视频、社交和商城五个应用拆分，符合模块化开发思路。"
        ),
        paragraph(
            "在社区互动与内容管理方面，已有研究表明，信息质量、互动便利性和用户参与感会影响虚拟社区的活跃程度。"
            "街舞平台既需要提供结构化信息，如活动时间、地点、报名状态和商品库存，也需要提供非结构化交流空间，如视频评论和聊天室消息。"
            "因此，本课题在功能设计中同时关注信息管理和社区互动，以满足用户“找活动、看作品、聊经验、买装备、管个人信息”的连续需求。"
        ),
        h2("1.4 毕设主要工作"),
        paragraph(
            "本毕业设计围绕“基于JavaScript的街舞信息共享平台设计与实现”展开，主要完成以下工作：第一，分析街舞用户、活动主办方和商家在信息共享场景下的需求，"
            "确定系统需要覆盖用户、活动、视频、社交、商城和个人中心等核心模块。第二，设计系统总体架构，采用React前端、Django后端和SQLite数据库的前后端分离方案。"
            "第三，完成数据库模型设计，建立用户、收藏、关注、活动、活动报名、视频、视频评论、聊天室、聊天消息、商品、购物车、订单和订单明细等实体。"
            "第四，实现前后端主要功能，包括注册登录、活动发布报名、视频互动、聊天室发言、商品下单、模拟支付和个人中心统计。"
            "第五，通过功能测试和接口联调验证系统可用性，并对项目不足与后续优化方向进行总结。"
        ),
    ]
)

sections.extend(
    [
        h1("第二章 设计方案"),
        h2("2.1 网站开发技术介绍"),
        h3("2.1.1 JavaScript、HTML5与CSS3"),
        paragraph(
            "JavaScript是本系统前端交互逻辑的核心语言，主要负责处理用户输入、页面状态更新、接口请求和数据渲染。"
            "HTML5用于构建网页结构，CSS3用于完成视觉样式、响应式布局、卡片效果和页面背景。系统界面采用侧边导航与内容卡片结合的布局，"
            "通过CSS Grid、Flex布局和媒体查询适配桌面端与移动端访问。"
        ),
        h3("2.1.2 React与Vite"),
        paragraph(
            "React是一种用于构建用户界面的JavaScript库，适合将复杂页面拆分为独立组件。本系统前端使用React 19和React Router实现单页应用路由，"
            "将首页、活动、视频、社交、商城、登录和个人中心分别封装为页面组件。Vite作为前端构建工具，负责开发服务器、模块加载和生产构建。"
            "项目中的vite.config.js配置了代理规则，将/users、/activities、/videos、/social和/mall等路径转发到Django后端，方便开发阶段前后端联调。"
        ),
        h3("2.1.3 Python与Django"),
        paragraph(
            "后端采用Python语言和Django框架实现。Django提供了MTV开发模式、URL路由、视图函数、ORM模型、Session认证和Admin后台等能力。"
            "本系统在Django中创建了users、activities、videos、social和mall五个业务应用，分别处理用户关系、活动报名、视频互动、聊天室消息和商城订单。"
            "视图层主要返回JSON数据，前端通过fetch请求接口并根据返回结果更新页面状态。"
        ),
        h3("2.1.4 SQLite数据库"),
        paragraph(
            "数据库采用SQLite。SQLite轻量、部署简单、与Django默认兼容，适合毕业设计阶段进行原型开发和演示。"
            "系统将结构化数据存储在db.sqlite3中，后端通过Django ORM完成增删改查，避免直接拼接SQL语句，提高了代码可读性和维护性。"
            "如果后期系统面向真实线上环境，可将SQLite迁移至MySQL或PostgreSQL，并配合缓存、对象存储和消息服务提升性能。"
        ),
        h2("2.2 网站开发工具介绍"),
        paragraph(
            "本系统开发过程中主要使用Windows环境、PowerShell终端、Python虚拟环境、Django管理命令、Node.js、npm和浏览器调试工具。"
            "后端通过项目本地.venv虚拟环境安装Django 6.0.3和Pillow 12.1.1，使用manage.py执行迁移、检查和开发服务器启动。"
            "前端通过npm管理React、React DOM、React Router和Vite依赖，并使用npm run dev进行开发调试，使用npm run build生成前端构建产物。"
        ),
        h2("2.3 用户需求调研分析"),
        h3("2.3.1 用户角色分析"),
        paragraph(
            "系统面向的主要用户包括普通街舞爱好者、舞者用户、活动主办方和商城管理方。普通用户主要需要浏览活动、观看视频、进入聊天室和购买商品；"
            "舞者用户需要发布作品、参与比赛或公开课、与其他舞者交流；活动主办方需要发布比赛、商演、表演和伴舞等活动，并管理报名情况；"
            "商城管理方需要维护商品信息、库存和订单状态。"
        ),
        h3("2.3.2 功能性需求"),
        paragraph(
            "根据需求文档与项目实现，系统功能性需求包括：用户注册、登录、退出和个人资料维护；活动列表展示、活动发布、活动报名、签到、收藏和我的活动；"
            "视频列表展示、视频发布、详情查看、点赞、收藏、评论和我的视频；社交聊天室分类展示、房间详情查看和消息发送；"
            "商城商品展示、商品创建、加入购物车、创建订单、模拟支付和订单记录；个人中心统计用户发布、报名、视频、收藏、关注和订单等信息。"
        ),
        h3("2.3.3 非功能性需求"),
        paragraph(
            "系统应满足易用性、可靠性、安全性、可维护性和可扩展性要求。易用性体现在导航清晰、页面分类明确、操作反馈及时；"
            "可靠性体现在接口对空值、非法时间、重复报名、重复收藏、库存不足等异常情况进行校验；安全性体现在未登录用户不能执行发布、报名、评论、购物和个人信息查看等操作；"
            "可维护性体现在前端页面组件化和后端应用模块化；可扩展性体现在数据库实体关系清晰，后续可扩展地图定位、WebSocket实时聊天、真实文件上传和推荐算法。"
        ),
        h2("2.4 系统总体架构设计"),
        paragraph(
            "本系统采用B/S架构和前后端分离模式。用户通过浏览器访问React前端页面，前端根据用户操作向Django后端发送HTTP请求。"
            "Django后端接收请求后完成身份认证、业务校验、数据库读写和JSON响应。SQLite数据库负责持久化保存系统数据。"
            "这种架构能够将页面表现层与业务逻辑层分离，降低模块耦合度，也便于后续分别优化前端交互和后端接口。"
        ),
        table(
            [
                ["层次", "技术或模块", "主要职责"],
                ["表现层", "React、React Router、CSS3", "页面展示、路由跳转、表单输入、状态更新"],
                ["接口层", "fetch、JSON、Vite代理", "前端请求发送、错误提示、跨服务联调"],
                ["业务层", "Django Views、Session认证", "用户认证、活动报名、视频互动、商城订单等业务处理"],
                ["数据层", "Django ORM、SQLite", "实体建模、关系维护、数据持久化"],
            ]
        ),
        h2("2.5 系统功能模块设计"),
        h3("2.5.1 用户模块"),
        paragraph(
            "用户模块负责账号注册、登录、退出、个人资料维护、关注关系、收藏列表和个人中心统计。系统基于Django自定义User模型扩展昵称、头像、性别、手机号和个人简介字段。"
            "注册时后端校验用户名、密码和确认密码；登录时使用Django authenticate完成账号密码验证；登录成功后使用Session保持用户状态。"
            "个人中心通过dashboard接口统计用户发布活动、报名活动、视频、收藏、关注、粉丝和订单数量，并返回最近数据用于页面展示。"
        ),
        h3("2.5.2 活动模块"),
        paragraph(
            "活动模块面向赛事、商演、表演、伴舞和其他街舞活动。活动实体包含标题、类型、封面、内容、组织者、地点、经纬度、开始时间、结束时间、报名截止时间和状态。"
            "用户登录后可以发布活动，后端会校验必填字段、时间格式、结束时间是否晚于开始时间以及报名截止时间是否早于活动开始时间。"
            "用户可以报名活动，系统通过activity与user的唯一约束避免重复报名；也可以对已报名活动进行签到，并将签到状态和签到时间记录到数据库。"
        ),
        h3("2.5.3 视频模块"),
        paragraph(
            "视频模块用于展示街舞作品。用户可以发布作品标题、视频地址或文件路径和作品描述；其他用户可以查看视频详情、点赞、收藏并发表评论。"
            "视频表记录点赞数、收藏数和评论数，评论表记录评论用户、评论内容和创建时间。收藏视频时系统会在Favorite表中记录target_type为video的数据，"
            "并更新视频收藏数量。该模块为舞者展示作品和形成互动反馈提供了基础。"
        ),
        h3("2.5.4 社交模块"),
        paragraph(
            "社交模块提供分类聊天室。系统默认创建舞房招聘、舞蹈心得交流、比赛经验、Hiphop、Swag、Jazz、Popping、Locking、Breaking和其他舞蹈分类等房间。"
            "用户可以查看房间列表和房间消息，登录后可以发送消息。当前实现采用普通HTTP接口保存和读取消息记录，适合毕业设计原型演示；后续可升级为WebSocket实时通信。"
        ),
        h3("2.5.5 商城模块"),
        paragraph(
            "商城模块用于街舞服饰和装备展示。商品表记录名称、分类、封面、价格、库存、描述和状态。用户可以浏览商品，登录后加入购物车。"
            "创建订单时，系统会读取当前用户购物车项目，在数据库事务中检查库存、扣减库存、创建订单和订单明细，并清空购物车。"
            "支付功能采用模拟支付流程，将订单状态更新为已支付，满足毕业设计演示中对购买流程闭环的要求。"
        ),
        h3("2.5.6 前端页面模块"),
        paragraph(
            "前端页面包括首页、登录页、活动页、视频页、社交页、商城页和个人中心页。首页集中展示平台简介、聊天室分类、最新视频、商城商品和开发状态；"
            "登录页提供登录和注册表单；活动页展示活动列表并提供发布、报名、收藏操作；视频页采用列表与详情并列布局，支持点赞、收藏和评论；"
            "社交页展示聊天室列表和消息流；商城页展示商品、购物车和订单；个人中心页展示资料编辑、统计指标、收藏、关注和最近动态。"
        ),
        h2("2.6 数据库表结构设计"),
        paragraph(
            "系统数据库围绕用户、内容、互动和交易四类数据展开。用户类数据包括用户、关注和收藏；内容类数据包括活动、活动报名、视频和视频评论；"
            "互动类数据包括聊天室和聊天消息；交易类数据包括商品、购物车、订单和订单明细。以下为核心数据表说明。"
        ),
        table(
            [
                ["表名", "核心字段", "说明"],
                ["users_user", "id、username、password、nickname、gender、phone、profile", "保存平台用户账号和扩展资料"],
                ["users_favorite", "id、user_id、target_type、target_id、created_at", "保存活动或视频收藏关系"],
                ["users_follow", "id、follower_id、following_id、created_at", "保存用户关注关系"],
                ["activities_activity", "id、organizer_id、title、activity_type、location、start_time、status", "保存活动基础信息"],
                ["activities_activityregistration", "id、activity_id、user_id、signup_time、checked_in", "保存活动报名和签到信息"],
                ["videos_video", "id、user_id、title、video_file、like_count、favorite_count、comment_count", "保存视频作品信息"],
                ["videos_videocomment", "id、video_id、user_id、content、created_at", "保存视频评论"],
                ["social_chatroom", "id、room_name、category、description、created_at", "保存聊天室分类"],
                ["social_chatmessage", "id、room_id、user_id、content、sent_at", "保存聊天室消息"],
                ["mall_product", "id、name、category、price、stock、status", "保存商城商品"],
                ["mall_cartitem", "id、user_id、product_id、quantity", "保存购物车项目"],
                ["mall_order", "id、user_id、total_amount、order_status、payment_status", "保存订单主表"],
                ["mall_orderitem", "id、order_id、product_id、quantity、unit_price", "保存订单明细"],
            ]
        ),
        paragraph(
            "数据库设计中对部分业务关系设置唯一约束。例如活动报名表对activity和user设置联合唯一，避免同一用户重复报名同一活动；"
            "收藏表对user、target_type和target_id设置联合唯一，避免重复收藏；关注表对follower和following设置联合唯一，避免重复关注。"
            "这些约束可以在数据库层面保证数据一致性。"
        ),
    ]
)

sections.extend(
    [
        h1("第三章 制作过程分析"),
        h2("3.1 系统开发环境搭建"),
        paragraph(
            "后端开发首先创建项目本地Python虚拟环境.venv，并在虚拟环境中安装Django和Pillow依赖。项目根目录包含manage.py和config配置目录，"
            "config/settings.py中配置INSTALLED_APPS、MIDDLEWARE、DATABASES、AUTH_USER_MODEL、STATIC_URL、MEDIA_URL和时区等内容。"
            "数据库使用SQLite，执行迁移后生成db.sqlite3文件。后端可通过manage.py runserver启动，默认运行在http://127.0.0.1:8000。"
        ),
        paragraph(
            "前端位于frontend目录，使用Vite创建React项目。package.json中定义dev和build脚本，依赖包括react、react-dom、react-router-dom、vite和@vitejs/plugin-react。"
            "开发阶段通过npm run dev启动前端服务，默认访问地址为http://127.0.0.1:5173。Vite代理将业务接口路径转发到后端，减少前端开发时的跨域配置成本。"
        ),
        h2("3.2 系统功能模块实现"),
        h3("3.2.1 用户认证与个人中心实现"),
        paragraph(
            "用户认证由users应用实现。register接口接收用户名、密码、确认密码、昵称、邮箱、手机号等信息，完成非空校验、密码一致性校验和用户名唯一性校验后创建用户，"
            "并自动登录。login接口通过Django authenticate校验账号密码，成功后写入Session。logout接口清除当前会话。me接口支持GET获取当前用户信息，"
            "支持PATCH修改昵称、邮箱、手机号、性别和个人简介。"
        ),
        paragraph(
            "个人中心通过dashboard接口聚合数据。后端分别统计当前用户发布的活动、报名的活动、发布的视频、收藏数、关注数、粉丝数和订单数，"
            "并返回最近发布活动、最近报名活动、最近视频和最近订单。前端ProfilePage在用户登录后并行请求dashboard、favorites和following接口，"
            "在页面中展示个人概况、统计卡片、资料编辑表单、收藏列表、关注列表和最近动态。"
        ),
        h3("3.2.2 活动模块实现"),
        paragraph(
            "活动后端由activities应用实现。activity_list接口同时支持GET和POST。GET请求可根据keyword、activity_type和status进行筛选，"
            "并返回活动列表、组织者信息、报名人数、当前用户是否报名和是否收藏等数据。POST请求用于发布活动，要求用户登录，并校验标题、类型、内容、地点和时间字段。"
            "活动详情、我的发布、我的报名、报名活动、签到活动和收藏活动分别由独立接口处理。"
        ),
        paragraph(
            "活动前端页面ActivitiesPage在加载时请求活动列表，并将活动类型、状态、标题、内容、地点和开始时间以卡片形式展示。"
            "用户可以点击报名和收藏按钮触发对应接口，也可以在右侧表单中填写活动标题、类型、地点、描述、开始时间、结束时间和报名截止时间发布新活动。"
            "操作成功或失败均通过页面顶部notice区域提示用户。"
        ),
        h3("3.2.3 视频模块实现"),
        paragraph(
            "视频后端由videos应用实现。video_list接口支持获取视频列表和发布视频；video_detail接口返回视频详情和评论列表；my_videos接口返回当前用户发布的视频；"
            "like_video接口递增点赞数；favorite_video接口写入收藏记录并递增收藏数；comment_video接口创建评论并更新评论数量。"
            "所有发布、点赞、收藏和评论操作均要求用户登录，未登录时返回401状态。"
        ),
        paragraph(
            "视频前端页面VideosPage采用左右结构。左侧显示作品列表，右侧显示当前选中作品详情、视频文件路径、点赞数、收藏数、评论列表和评论表单。"
            "用户可在下方发布新视频，表单字段包括作品标题、视频地址或文件路径和作品描述。该模块实现了视频内容展示与互动反馈的基本闭环。"
        ),
        h3("3.2.4 社交聊天室实现"),
        paragraph(
            "社交后端由social应用实现。room_list接口在返回房间列表前会调用默认房间初始化逻辑，保证系统中存在舞房招聘、舞蹈心得交流、比赛经验和多个舞种分类房间。"
            "room_detail接口返回房间信息和消息记录。send_message接口要求用户登录，接收消息内容后创建ChatMessage记录。"
        ),
        paragraph(
            "社交前端页面SocialPage显示房间列表和当前房间消息流。用户选择房间后，页面请求房间详情并渲染历史消息；登录用户可以在文本框中输入消息并发送。"
            "当前实现以HTTP轮询式交互为主，虽然尚未达到实时通信效果，但已经能够完成分类讨论和消息沉淀。"
        ),
        h3("3.2.5 商城模块实现"),
        paragraph(
            "商城后端由mall应用实现。product_list接口支持商品查询和商品创建，cart_items接口支持查看购物车和加入购物车。"
            "创建订单时，后端使用transaction.atomic开启数据库事务，依次检查商品库存、扣减库存、创建Order和OrderItem记录，并清空购物车。"
            "pay_order接口模拟支付，将payment_status设为True，并将order_status更新为paid。my_orders接口返回当前用户订单和订单明细。"
        ),
        paragraph(
            "商城前端页面MallPage包含商品列表、新增商品、购物车和订单记录四部分。商品卡片展示名称、分类、描述、价格和库存，用户可将商品加入购物车。"
            "购物车区域可以创建订单，订单区域对未支付订单提供立即支付按钮。通过该流程，系统完成了从商品浏览到支付状态更新的演示闭环。"
        ),
        h3("3.2.6 首页与整体交互实现"),
        paragraph(
            "App组件负责全局布局、导航、登录状态维护和路由配置。页面左侧为固定侧边栏，显示平台名称、导航链接和当前登录状态；右侧为主要内容区域。"
            "App初始化时请求/users/me/接口刷新当前用户状态，退出登录后清除用户状态并跳转到登录页。首页HomePage通过Promise.all并行请求聊天室、视频和商品数据，"
            "展示平台简介、聊天室分类、最新视频、商城商品和开发状态，使用户能够快速理解平台功能。"
        ),
        h2("3.3 前后端接口联调"),
        paragraph(
            "系统接口采用JSON作为主要数据格式，前端统一通过apiFetch方法发送请求。apiFetch默认携带Content-Type: application/json和credentials: include，"
            "保证Django Session能够在前后端请求中保持登录状态。当接口响应状态不是成功状态时，apiFetch会读取后端detail字段并抛出错误，前端页面捕获后展示提示信息。"
            "这种统一封装减少了各页面重复处理请求和错误的代码。"
        ),
        table(
            [
                ["模块", "主要接口", "说明"],
                ["用户", "/users/register/、/users/login/、/users/me/、/users/dashboard/", "注册登录、资料维护和个人中心统计"],
                ["活动", "/activities/list/、/activities/<id>/register/、/activities/<id>/checkin/", "活动列表、发布、报名和签到"],
                ["视频", "/videos/list/、/videos/<id>/like/、/videos/<id>/favorite/、/videos/<id>/comments/", "视频发布、点赞、收藏和评论"],
                ["社交", "/social/rooms/、/social/rooms/<id>/、/social/rooms/<id>/messages/", "聊天室列表、详情和消息发送"],
                ["商城", "/mall/products/、/mall/cart/、/mall/orders/create/、/mall/orders/<id>/pay/", "商品、购物车、订单和支付"],
            ]
        ),
        h2("3.4 功能测试"),
        paragraph(
            "系统测试主要采用黑盒测试方法，从用户操作角度验证各模块是否符合预期。测试重点包括正常流程是否可完成、异常输入是否有提示、未登录权限是否被拦截、"
            "重复操作是否被限制以及数据是否正确更新。测试环境为本地Django后端、React前端和SQLite数据库。"
        ),
        table(
            [
                ["测试编号", "测试内容", "预期结果", "测试结论"],
                ["T01", "访问系统首页", "首页显示平台简介、聊天室、视频和商品概览", "通过"],
                ["T02", "用户注册并自动登录", "注册成功后进入登录态，个人中心可访问", "通过"],
                ["T03", "使用错误密码登录", "系统提示用户名或密码错误", "通过"],
                ["T04", "未登录发布活动", "接口返回请先登录，页面显示错误提示", "通过"],
                ["T05", "发布合法活动", "活动创建成功并出现在活动列表", "通过"],
                ["T06", "报名同一活动两次", "第一次成功，第二次提示已报名", "通过"],
                ["T07", "活动签到", "报名用户签到成功并记录签到时间", "通过"],
                ["T08", "发布视频并评论", "视频出现在列表，评论显示在详情页", "通过"],
                ["T09", "收藏同一视频两次", "第一次成功，第二次提示已收藏", "通过"],
                ["T10", "进入聊天室发送消息", "消息保存并展示在房间消息列表中", "通过"],
                ["T11", "商品加入购物车并创建订单", "购物车清空，生成订单并扣减库存", "通过"],
                ["T12", "模拟支付订单", "订单状态更新为已支付", "通过"],
                ["T13", "修改个人资料", "资料保存成功，页面显示新昵称和简介", "通过"],
            ]
        ),
        paragraph(
            "从测试结果看，系统主要功能能够按照设计要求运行。需要注意的是，当前视频发布主要填写视频地址或文件路径，尚未实现浏览器端真实大文件上传；"
            "聊天室采用普通HTTP接口而非WebSocket，因此实时性还有提升空间；支付为模拟流程，不涉及真实第三方支付平台。"
        ),
    ]
)

sections.extend(
    [
        h1("第四章 总结与反思"),
        h2("4.1 总结"),
        paragraph(
            "本文围绕街舞领域信息分散、活动报名不便、作品互动和社群交流缺乏统一入口等问题，设计并实现了基于JavaScript的街舞信息共享平台。"
            "系统采用React + Vite前端、Django后端和SQLite数据库的前后端分离架构，完成了用户、活动、视频、社交、商城和个人中心等主要模块。"
            "通过系统实现，用户可以完成注册登录、活动发布报名、视频发布互动、聊天室交流、商城下单和个人行为数据查看等操作。"
        ),
        paragraph(
            "在开发过程中，前端通过组件化页面组织提升了代码可维护性，后端通过Django应用拆分明确了模块边界，数据库通过ORM模型描述实体和关系。"
            "系统还提供了演示数据初始化命令，便于答辩和功能展示。总体来看，本系统达到了毕业设计原型系统的预期目标，能够较完整地展示街舞信息共享平台的业务流程。"
        ),
        h2("4.2 反思"),
        paragraph(
            "受开发周期和毕业设计规模限制，系统仍存在一些不足。第一，视频模块当前以视频地址或文件路径作为输入，尚未实现完整的文件上传、转码、封面截取和对象存储能力。"
            "第二，聊天室当前采用HTTP请求保存和读取消息，实时互动体验不如WebSocket方案。第三，活动模块虽然预留经纬度字段，但尚未接入地图服务和附近活动推荐。"
            "第四，商城支付流程为模拟支付，未接入真实支付渠道，也未实现退单、发货、物流等完整电商流程。第五，系统安全性仍可继续增强，例如CSRF策略、上传文件校验、"
            "接口权限细分、生产环境密钥管理和日志审计等。"
        ),
        paragraph(
            "后续优化可以从以下方向展开：在视频模块中接入真实文件上传和媒体存储；在社交模块中使用WebSocket实现实时聊天；"
            "在活动模块中接入地图定位和距离计算；在首页和视频列表中增加标签、搜索排序和个性化推荐；在商城模块中完善订单生命周期；"
            "在部署方面将数据库升级为MySQL或PostgreSQL，并配置Nginx、HTTPS和云服务器环境。"
        ),
        h1("结束语"),
        paragraph(
            "本毕业设计从街舞用户的实际需求出发，完成了街舞信息共享平台的需求分析、架构设计、数据库设计、功能实现和测试验证。"
            "通过本课题的开发，我进一步理解了前后端分离Web系统的完整开发流程，也加深了对React组件化开发、Django后端接口设计、SQLite数据建模和业务联调的认识。"
            "虽然系统仍有很多可完善之处，但其核心功能已经能够支撑活动、作品、社交、商城和个人中心等主要业务场景。"
            "未来如果继续迭代，本平台可以进一步发展为更真实、更高效、更具社区活力的街舞数字服务平台。"
        ),
        h1("致谢"),
        paragraph(
            "在本论文和系统开发完成之际，首先感谢指导教师在选题、需求分析、系统设计和论文撰写过程中给予的指导与帮助。"
            "老师的建议使我能够更清晰地把握毕业设计的研究方向，也帮助我在开发过程中及时发现问题、调整方案。"
            "同时感谢同学和朋友在系统需求讨论、功能体验和测试反馈中提供的帮助，使平台功能更加贴近真实使用场景。"
            "最后感谢家人在学习和生活上的支持，使我能够顺利完成本次毕业设计。"
        ),
        h1("参考文献"),
        paragraph("[1] 吴伟敏. 网站设计与开发基础研究[M]. 北京: 清华大学出版社, 2009."),
        paragraph("[2] 赵怡娜. HTML5与CSS3在现代网页设计中的应用研究[J]. 信息与电脑, 2021."),
        paragraph("[3] 王萍利. 基于HTML5的前端框架应用与实践[J]. 电脑知识与技术, 2021."),
        paragraph("[4] 宫道. HTML5+CSS3网页性能优化与视觉实现研究[J]. 软件导刊, 2020."),
        paragraph("[5] 郭鹤楠. 基于Django框架的网站开发流程研究[J]. 电脑编程技巧与维护, 2023."),
        paragraph("[6] 华厚强. 基于Python的校园交易平台设计与实现[J]. 现代信息科技, 2022."),
        paragraph("[7] 宋永生. 基于Python的视频信息挖掘技术研究[J]. 计算机应用研究, 2019."),
        paragraph("[8] 张炫秋. 虚拟社区信息共享意愿影响因素研究[J]. 情报科学, 2015."),
        paragraph("[9] Facebook Open Source. React Documentation[EB/OL]. https://react.dev/."),
        paragraph("[10] Django Software Foundation. Django Documentation[EB/OL]. https://docs.djangoproject.com/."),
        paragraph("[11] Vite Team. Vite Documentation[EB/OL]. https://vite.dev/."),
        h1("附录"),
        h2("附录A 核心接口列表"),
        paragraph("用户模块：POST /users/register/，POST /users/login/，POST /users/logout/，GET/PATCH /users/me/，GET /users/dashboard/。"),
        paragraph("活动模块：GET/POST /activities/list/，GET /activities/<activity_id>/，POST /activities/<activity_id>/register/，POST /activities/<activity_id>/checkin/，POST /activities/<activity_id>/favorite/。"),
        paragraph("视频模块：GET/POST /videos/list/，GET /videos/<video_id>/，POST /videos/<video_id>/like/，POST /videos/<video_id>/favorite/，POST /videos/<video_id>/comments/。"),
        paragraph("社交模块：GET /social/rooms/，GET /social/rooms/<room_id>/，POST /social/rooms/<room_id>/messages/。"),
        paragraph("商城模块：GET/POST /mall/products/，GET/POST /mall/cart/，POST /mall/orders/create/，POST /mall/orders/<order_id>/pay/，GET /mall/orders/。"),
        h2("附录B 演示账号"),
        paragraph("管理员：admin_demo / Admin123456。"),
        paragraph("普通用户：bboy_chen / Dance123456，studio_muse / Dance123456，jazz_luna / Dance123456。"),
        h2("附录C 运行说明"),
        paragraph("后端运行：使用项目本地虚拟环境执行 .venv\\Scripts\\python.exe manage.py migrate，随后执行 .venv\\Scripts\\python.exe manage.py seed_demo_data，最后执行 .venv\\Scripts\\python.exe manage.py runserver。"),
        paragraph("前端运行：进入frontend目录后执行npm install安装依赖，再执行npm run dev启动开发服务器。"),
    ]
)


document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14">
  <w:body>
    {''.join(sections)}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>
</w:document>
"""


styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="360" w:after="240"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="黑体" w:hAnsi="Times New Roman"/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="240" w:after="160"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="黑体" w:hAnsi="Times New Roman"/><w:sz w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="180" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体" w:hAnsi="Times New Roman"/><w:sz w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>
"""


content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""


rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


document_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""


now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
core_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>基于JavaScript的街舞信息共享平台设计与实现</dc:title>
  <dc:subject>毕业设计论文</dc:subject>
  <dc:creator>Codex</dc:creator>
  <cp:keywords>街舞信息共享平台;JavaScript;React;Django;SQLite</cp:keywords>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


app_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <Company></Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0000</AppVersion>
</Properties>
"""


def main():
    """写出docx文件，并保持生成过程只新增目标论文文档。"""
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types_xml)
        docx.writestr("_rels/.rels", rels_xml)
        docx.writestr("word/document.xml", document_xml)
        docx.writestr("word/_rels/document.xml.rels", document_rels_xml)
        docx.writestr("word/styles.xml", styles_xml)
        docx.writestr("docProps/core.xml", core_xml)
        docx.writestr("docProps/app.xml", app_xml)
    print(f"已生成：{OUTPUT.resolve()}")


if __name__ == "__main__":
    main()
