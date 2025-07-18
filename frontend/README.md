# ALLWEONE® AI 演示文稿生成器（Gamma 替代品）
⭐ 帮助我们让更多开发者了解并壮大 ALLWEONE 社区，为本仓库点个 Star！

https://github.com/user-attachments/assets/a21dbd49-75b8-4822-bcec-a75b581d9c60


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

一个受 gamma.app 启发的开源 AI 演示文稿生成器，能用 AI 快速生成精美幻灯片，并可自定义。该工具是 ALLWEONE AI 平台的一部分。

[在线演示](https://allweone.com/presentations) | [视频教程](https://www.youtube.com/watch?v=UUePLJeFqVQ)

## 🌟 功能亮点

- **AI 内容生成**：用 AI 一键生成任意主题的完整演示文稿
- **自定义幻灯片**：可选择幻灯片数量、语言和页面风格
- **可编辑大纲**：生成后可审阅和修改大纲
- **多主题支持**：内置 9 种主题，更多主题即将上线
- **自定义主题**：可从零创建并保存自己的主题
- **图片生成**：可选不同 AI 图片生成模型为幻灯片配图
- **受众风格选择**：支持专业/休闲两种演示风格
- **实时生成**：演示文稿内容实时生成可见
- **完全可编辑**：可修改文本、字体和设计元素
- **演示模式**：可直接在应用内放映演示文稿
- **自动保存**：编辑内容自动保存

## 🚀 快速开始

### 前置条件

- Node.js 18.x 或更高版本
- npm 或 yarn
- OpenAI API Key（用于 AI 生成）
- Together AI API Key（用于图片生成）
- Google Client ID 和 Secret（用于认证功能）

### 安装步骤
0: 安装docker postgresql
```
docker run --name postgresdb -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=welcome -d postgres
```

1. 安装依赖(当前frontend目录下)：

   ```bash
   cp env_template .env
   npm install -g pnpm
   pnpm install
   ```

2. 设置数据库：

   ```bash
   pnpm db:push
   ```

3. 应该是插入了一条数据到数据库(以前有用户认证，我给删掉了，用一条默认用户测试)
```
INSERT INTO public."User" (
    "id",
    "name",
    "email",
    "password",
    "emailVerified",
    "image",
    "headline",
    "bio",
    "interests",
    "location",
    "website",
    "role",
    "hasAccess"
) VALUES (
    '01',
    'Admin User',
    'admin@example.com',
    'hashed_password_here',
    NOW(),
    NULL,
    'Administrator',
    'Default admin account',
    ARRAY['admin', 'manager'],
    'Global',
    'https://example.com',
    'ADMIN',
    true
);
```

4. 检查.env文件
cp env_template .env
```
DATABASE_URL="postgresql://postgres:welcome@localhost:5432/presentation_ai"
A2A_AGENT_OUTLINE_URL="http://localhost:10001"
A2A_AGENT_SLIDES_URL="http://localhost:10011"
#下载成ppt的后端
DOWNLOAD_SLIDES_URL="http://localhost:10021"  
```

5. 启动开发服务器：

   ```bash
   pnpm dev
   ```

6. 在浏览器中打开 [http://localhost:3000](http://localhost:3000) 查看应用。

## 💻 使用指南

### 创建演示文稿

1. 进入仪表板
2. 输入演示文稿主题
3. 选择幻灯片数量（推荐：5-10）
4. 选择您偏好的语言
5. 选择页面风格
6. 点击“生成大纲”
7. 审阅并编辑 AI 生成的大纲
8. 为演示文稿选择一个主题
9. 选择图像生成模型
10. 选择您的演示风格（专业/休闲）
11. 点击“生成演示文稿”
12. 等待 AI 实时创建幻灯片
13. 根据需要预览、编辑和完善演示文稿
14. 直接从应用中演示或导出演示文稿

### 自定义主题

1. 点击“创建新主题”
2. 从头开始或从现有主题派生
3. 自定义颜色、字体和布局
4. 保存您的主题以供将来使用

## 🧰 技术栈

该项目使用以下技术构建：

- **Next.js**：用于服务器渲染应用的 React 框架
- **React**：构建用户界面的 UI 库
- **Prisma**：带有 PostgreSQL 的数据库 ORM
- **Tailwind CSS**：实用优先的 CSS 框架
- **TypeScript**：带类型的 JavaScript
- **OpenAI API**：用于 AI 内容生成
- **Radix UI**：无头 UI 组件
- **Plate Editor**：用于处理文本、图像和幻灯片组件的富文本编辑系统
- **身份验证**：NextAuth.js 用于用户身份验证
- **UploadThing**：文件上传
- **DND Kit**：拖放功能

## 🛠️ 项目结构

```
presentation/
├── .next/               # Next.js 构建输出
├── node_modules/        # 依赖
├── prisma/              # 数据库模式
│   └── schema.prisma    # Prisma 数据库模型
├── src/                 # 源代码
│   ├── app/             # Next.js 应用路由
│   ├── components/      # 可重用的 UI 组件
│   │   ├── auth/        # 身份验证组件
│   │   ├── presentation/  # 演示文稿相关组件
│   │   │   ├── dashboard/   # 仪表板 UI
│   │   │   ├── editor/      # 演示文稿编辑器
│   │   │   │   ├── custom-elements/  # 自定义编辑器元素
│   │   │   │   ├── dnd/              # 拖放功能
│   │   │   │   └── native-elements/  # 原生编辑器元素
│   │   │   ├── outline/     # 演示文稿大纲组件
│   │   │   ├── theme/       # 主题相关组件
│   │   │   └── utils/       # 演示文稿工具
│   │   ├── prose-mirror/  # ProseMirror 编辑器组件，用于大纲部分
│   │   ├── text-editor/   # 文本编辑器组件
│   │   │   ├── hooks/       # 编辑器钩子
│   │   │   ├── lib/         # 编辑器库
│   │   │   ├── plate-ui/    # Plate 编辑器 UI 组件
│   │   │   └── plugins/     # 编辑器插件
│   │   └── ui/           # 共享 UI 组件
│   ├── hooks/           # 自定义 React 钩子
│   ├── lib/             # 工具函数和共享代码
│   ├── provider/        # 上下文提供者
│   ├── server/          # 服务器端代码
│   ├── states/          # 状态管理
│   ├── middleware.ts    # Next.js 中间件
│   └── env.js           # 环境配置
├── .env                 # 环境变量
├── .env.example         # 示例环境变量
├── next.config.js       # Next.js 配置
├── package.json         # 项目依赖和脚本
├── tailwind.config.ts   # Tailwind CSS 配置
└── tsconfig.json        # TypeScript 配置
```

## 🤝 贡献代码

我们欢迎您为 ALLWEONE 演示文稿生成器贡献代码！以下是您可以帮助的方式：

1. Fork 本仓库
2. 创建一个特性分支（`git checkout -b feature/amazing-feature`）
3. 提交您的更改（`git commit -m 'Add some amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 提交一个 Pull Request


由 ALLWEONE™ 团队 ❤️ 打造 🇺🇸🇧🇷🇳🇵🇮🇳🇨🇳🇯🇵🇸🇬🇩🇪🏴🇺🇦🇰🇿🇷🇺🇦🇪🇸🇦🇰🇷🇹🇭🇮🇩🇲🇽🇬🇹🇫🇷🇮🇱🇻🇳🇵🇹🇮🇹🇨🇱🇨🇦🇵🇰🇸🇪🇱🇧

如有任何问题或支持，请在 GitHub 上提交问题或通过 Discord 联系我们 https://discord.gg/wSVNudUBdY




# 生成ppt内容： src/components/presentation/dashboard/PresentationGenerationManager.tsx
/api/presentation/outline


# 生成结果
```
curl 'http://localhost:3000/api/presentation/outline' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en,zh-CN;q=0.9,zh;q=0.8' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b 'Pycharm-b84366fb=76978326-c369-483f-a7ed-69508bdbe922; __clerk_db_jwt=dvb_2qux2dBXAvqA6fqgpg7DM01ryzu; __clerk_db_jwt_LkzGSFga=dvb_2qux2dBXAvqA6fqgpg7DM01ryzu; __session_LkzGSFga=eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18ycXV3bWNqUUdLT3VqZThVTEh3Z0RwM2hWWVAiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJleHAiOjE3MzU1MjY3MzAsImZ2YSI6WzgsLTFdLCJpYXQiOjE3MzU1MjY2NzAsImlzcyI6Imh0dHBzOi8vc3VwZXItZHJhZ29uLTQwLmNsZXJrLmFjY291bnRzLmRldiIsIm5iZiI6MTczNTUyNjY2MCwic2lkIjoic2Vzc18ycXV4SVpNNlBPRmJRVFhDOTRXYU5MYU83bTEiLCJzdWIiOiJ1c2VyXzJxdXhHUEVYWUVLbnE4eHFvVmpITmQzV2VGdCJ9.SAGwDy9ArFVXFbzg3KNltZlrJBnScdBF0pvv2aBPEKjeakX6ALGNWIahsz-jC7BbR1lPG8p1FpyvMATEp1VYIGOdY5aTJSKM6gzxZVT6jjHbTKWbCOR7WGS-J2nh7PwknzmK0r7kJn4LhtpuPbIzja1ArNLJ3t9k9rpcejoY59DIrcmOpuBRprM6py_nrMzRVOuc6erNJVkYLR6p33ZH2WFDdH8imoZFct-1mNsDdqSEr4v4PHk5MqldQwUqzFyFeMtafqe8dhDRJK2ZZh80Ks9F28d3RS-PYh4Zbe4LxBC5xBfIUUOcasqbgedslq7CZ39jpxOtTFKrXBdS4GejSg; __session=eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18ycXV3bWNqUUdLT3VqZThVTEh3Z0RwM2hWWVAiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJleHAiOjE3MzU1MjY3MzAsImZ2YSI6WzgsLTFdLCJpYXQiOjE3MzU1MjY2NzAsImlzcyI6Imh0dHBzOi8vc3VwZXItZHJhZ29uLTQwLmNsZXJrLmFjY291bnRzLmRldiIsIm5iZiI6MTczNTUyNjY2MCwic2lkIjoic2Vzc18ycXV4SVpNNlBPRmJRVFhDOTRXYU5MYU83bTEiLCJzdWIiOiJ1c2VyXzJxdXhHUEVYWUVLbnE4eHFvVmpITmQzV2VGdCJ9.SAGwDy9ArFVXFbzg3KNltZlrJBnScdBF0pvv2aBPEKjeakX6ALGNWIahsz-jC7BbR1lPG8p1FpyvMATEp1VYIGOdY5aTJSKM6gzxZVT6jjHbTKWbCOR7WGS-J2nh7PwknzmK0r7kJn4LhtpuPbIzja1ArNLJ3t9k9rpcejoY59DIrcmOpuBRprM6py_nrMzRVOuc6erNJVkYLR6p33ZH2WFDdH8imoZFct-1mNsDdqSEr4v4PHk5MqldQwUqzFyFeMtafqe8dhDRJK2ZZh80Ks9F28d3RS-PYh4Zbe4LxBC5xBfIUUOcasqbgedslq7CZ39jpxOtTFKrXBdS4GejSg; __client_uat_LkzGSFga=1735526181; __client_uat=1735526181' \
  -H 'Origin: http://localhost:3000' \
  -H 'Referer: http://localhost:3000/presentation/generate/cmc5wczhr0000a7fthnhe2ckv' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw '{"prompt":"xiao mi Car","numberOfCards":10,"language":"en-US"}'
```

输出结果：
0:"#"
0:" Introduction"
0:" to"
0:" Xiaomi"
0:" Car"
0:"\n"
0:"-"
0:" Overview"
0:" of"
0:" Xiaomi"
0:"'s"
0:" entry"
0:" into"
0:" the"
0:" automotive"
0:" market"
0:".\n"
0:"-"
0:" Importance"
0:" of"
0:" electric"
0:" vehicles"
0:" in"
0:" today's"
0:" economy"
0:".\n"
0:"-"
0:" Brief"
0:" mention"
0:" of"
0:" Xiaomi"
0:"'s"
0:" reputation"
0:" in"
0:" technology"
0:".\n\n"
0:"#"
0:" Xiaomi"
0:"'s"
0:" Vision"
0:" for"
0:" Smart"
0:" Mobility"
0:"\n"
0:"-"
0:" Explanation"
0:" of"
0:" the"
0:" concept"
0:" of"
0:" smart"
0:" mobility"
0:".\n"
0:"-"
0:" Integration"
0:" of"
0:" Io"
0:"T"
0:" and"
0:" AI"
0:" in"
0:" Xiaomi"
0:"'s"
0:" car"
0:" technology"
0:".\n"
0:"-"
0:" Potential"
0:" benefits"
0:" for"
0:" consumers"
0:" and"
0:" cities"
0:".\n\n"
0:"#"
0:" Design"
0:" and"
0:" A"
0:"est"
0:"hetics"
0:"\n"
0:"-"
0:" Focus"
0:" on"
0:" the"
0:" design"
0:" philosophy"
0:" behind"
0:" the"
0:" Xiaomi"
0:" car"
0:".\n"
0:"-"
0:" Key"
0:" aesthetic"
0:" features"
0:" that"
0:" distinguish"
0:" it"
0:" from"
0:" competitors"
0:".\n"
0:"-"
0:" User"
0:" experience"
0:" considerations"
0:" in"
0:" design"
0:".\n\n"
0:"#"
0:" Electric"
0:" Vehicle"
0:" Technology"
0:"\n"
0:"-"
0:" Overview"
0:" of"
0:" the"
0:" battery"
0:" technology"
0:" utilized"
0:" in"
0:" Xiaomi"
0:" cars"
0:".\n"
0:"-"
0:" Discussion"
0:" on"
0:" range"
0:" and"
0:" charging"
0:" capabilities"
0:".\n"
0:"-"
0:" Environmental"
0:" impact"
0:" and"
0:" sustainability"
0:" efforts"
0:".\n\n"
0:"#"
0:" Autonomous"
0:" Driving"
0:" Features"
0:"\n"
0:"-"
0:" Explanation"
0:" of"
0:" autonomous"
0:" driving"
0:" capabilities"
0:" in"
0:" Xiaomi"
0:"'s"
0:" vehicles"
0:".\n"
0:"-"
0:" Safety"
0:" features"
0:" and"
0:" technology"
0:" that"
0:" support"
0:" autonomous"
0:" driving"
0:".\n"
0:"-"
0:" Future"
0:" developments"
0:" and"
0:" regulatory"
0:" considerations"
0:".\n\n"
0:"#"
0:" Connectivity"
0:" and"
0:" Smart"
0:" Features"
0:"\n"
0:"-"
0:" Overview"
0:" of"
0:" the"
0:" connectivity"
0:" features"
0:" integrated"
0:" into"
0:" the"
0:" Xiaomi"
0:" car"
0:".\n"
0:"-"
0:" Importance"
0:" of"
0:" app"
0:" integration"
0:" and"
0:" user"
0:" interface"
0:".\n"
0:"-"
0:" Smart"
0:" features"
0:" that"
0:" enhance"
0:" driver"
0:" and"
0:" passenger"
0:" experience"
0:".\n\n"
0:"#"
0:" Competitive"
0:" Landscape"
0:"\n"
0:"-"
0:" Analysis"
0:" of"
0:" major"
0:" competitors"
0:" in"
0:" the"
0:" electric"
0:" vehicle"
0:" market"
0:".\n"
0:"-"
0:" Xiaomi"
0:"'s"
0:" unique"
0:" selling"
0:" propositions"
0:" compared"
0:" to"
0:" other"
0:" brands"
0:".\n"
0:"-"
0:" Market"
0:" trends"
0:" influencing"
0:" competition"
0:" and"
0:" innovation"
0:".\n\n"
0:"#"
0:" Consumer"
0:" Target"
0:" Dem"
0:"ographics"
0:"\n"
0:"-"
0:" Identification"
0:" of"
0:" target"
0:" consumer"
0:" segments"
0:" for"
0:" the"
0:" Xiaomi"
0:" car"
0:".\n"
0:"-"
0:" Insights"
0:" into"
0:" consumer"
0:" preferences"
0:" for"
0:" electric"
0:" vehicles"
0:".\n"
0:"-"
0:" Strategies"
0:" for"
0:" marketing"
0:" and"
0:" outreach"
0:".\n\n"
0:"#"
0:" Future"
0:" of"
0:" Xiaomi"
0:" in"
0:" the"
0:" Automotive"
0:" Industry"
0:"\n"
0:"-"
0:" Predictions"
0:" for"
0:" Xiaomi"
0:"'s"
0:" growth"
0:" in"
0:" the"
0:" car"
0:" market"
0:" over"
0:" the"
0:" next"
0:" decade"
0:".\n"
0:"-"
0:" Potential"
0:" collaborations"
0:" or"
0:" partnerships"
0:" to"
0:" expand"
0:" capabilities"
0:".\n"
0:"-"
0:" Challenges"
0:" and"
0:" opportunities"
0:" in"
0:" the"
0:" evolving"
0:" automotive"
0:" landscape"
0:".\n\n"
0:"#"
0:" Conclusion"
0:" and"
0:" Call"
0:" to"
0:" Action"
0:"\n"
0:"-"
0:" Rec"
0:"ap"
0:" of"
0:" Xiaomi"
0:"'s"
0:" vision"
0:" and"
0:" innovation"
0:" in"
0:" the"
0:" automotive"
0:" sector"
0:".\n"
0:"-"
0:" Encour"
0:"agement"
0:" for"
0:" audience"
0:" engagement"
0:" with"
0:" the"
0:" brand"
0:".\n"
0:"-"
0:" Final"
0:" thoughts"
0:" on"
0:" the"
0:" future"
0:" of"
0:" electric"
0:" and"
0:" smart"
0:" vehicles"
0:"."


## PPT的XML示例格式内容
```xml
<PRESENTATION>

<SECTION layout="vertical">
  <H1>AI in Education</H1>
  <P>Discover how artificial intelligence is transforming the educational landscape, enhancing learning experiences, and preparing students for a tech-driven future.</P>
  <IMG query="students engaging with AI technology in a modern classroom setting, utilizing tablets and interactive screens" />
</SECTION>

<SECTION layout="left">
  <H2>Benefits for Teachers and Students</H2>
  <BULLETS>
    <DIV>
      <H3>Personalized Learning</H3>
      <P>AI systems analyze student performance data to tailor educational content, ensuring that each learner receives customized support aligned with their unique needs.</P>
    </DIV>
    <DIV>
      <H3>Efficiency in Administration</H3>
      <P>Teachers can automate grading and administrative tasks, allowing them to focus on what truly matters—engaging with students and enhancing their learning experiences.</P>
    </DIV>
  </BULLETS>
  <IMG query="collage of diverse students using AI software, showing personalized learning experiences and teacher-student interactions" />
</SECTION>

<SECTION layout="right">
  <H2>Challenges and Ethical Concerns</H2>
  <ICONS>
    <DIV>
      <ICON query="warning sign" />
      <H3>Data Privacy</H3>
      <P>How can we ensure that student data is protected while leveraging AI technologies?</P>
    </DIV>
    <DIV>
      <ICON query="scale" />
      <H3>Equity in Access</H3>
      <P>Ensuring all students, regardless of background, have access to AI tools is essential for equitable education.</P>
    </DIV>
    <DIV>
      <ICON query="question mark" />
      <H3>Bias in Algorithms</H3>
      <P>How do we address the potential biases present in AI algorithms that could affect student assessment and opportunities?</P>
    </DIV>
  </ICONS>
  <IMG query="conceptual image of ethical dilemmas in AI education, featuring a digital scale balancing books and data privacy symbols" />
</SECTION>

<SECTION layout="vertical">
  <H2>Future Trends in AI-Based Learning</H2>
  <CYCLE>
    <DIV>
      <H3>Adaptive Learning Systems</H3>
      <P>Future AI will further enhance adaptive learning systems that evolve based on real-time data.</P>
    </DIV>
    <DIV>
      <H3>Virtual Reality Integration</H3>
      <P>AI will be integrated with VR to create immersive learning experiences that go beyond traditional classrooms.</P>
    </DIV>
    <DIV>
      <H3>Global Learning Networks</H3>
      <P>AI will facilitate collaboration across borders, allowing students to learn from global experts in real-time.</P>
    </DIV>
  </CYCLE>
  <IMG query="vision of future classrooms with VR headsets, diverse students collaborating globally through technology" />
</SECTION>

<SECTION layout="left">
  <H2>Conclusion and Call to Action</H2>
  <P>As we embrace AI in education, it’s vital to advocate for ethical practices and equitable access. Join us in shaping a future where technology empowers every learner.</P>
  <BULLETS>
    <DIV>
      <H3>Get Involved</H3>
      <P>Support initiatives that promote AI literacy and ethical standards in educational technology.</P>
    </DIV>
    <DIV>
      <H3>Stay Informed</H3>
      <P>Follow industry trends and engage in discussions about the future of AI in education.</P>
    </DIV>
  </BULLETS>
  <IMG query="inspiring image of diverse educators and students collaborating in a technology-rich learning environment, symbolizing hope and innovation" />
</SECTION>

</PRESENTATION>
```

## 模拟生成大纲，toDataStreamResponse的格式
```
import { LangChainAdapter } from "ai";
import { NextResponse } from "next/server";
import { ChatOpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";
import { RunnableSequence } from "@langchain/core/runnables";
import { StringOutputParser } from "@langchain/core/output_parsers";

interface SlidesRequest {
  title: string; // Presentation title
  outline: string[]; // Array of main topics with markdown content
  language: string; // Language to use for the slides
  tone: string; // Style for image queries (optional)
}

// Helper function to convert an async string iterator to a ReadableStream
function iteratorToStream(iterator: AsyncGenerator<string>): ReadableStream<string> {
  return new ReadableStream({
    async pull(controller) {
      const { value, done } = await iterator.next();
      if (done) {
        controller.close();
      } else {
        controller.enqueue(value);
      }
    },
  });
}
const example_ppt = `
\`\`\`xml
<PRESENTATION>

<SECTION layout="vertical">
  <H1>AI in Education</H1>
  <P>Discover how artificial intelligence is transforming the educational landscape, enhancing learning experiences, and preparing students for a tech-driven future.</P>
  <IMG query="students engaging with AI technology in a modern classroom setting, utilizing tablets and interactive screens" />
</SECTION>

<SECTION layout="left">
  <H2>Benefits for Teachers and Students</H2>
  <BULLETS>
    <DIV>
      <H3>Personalized Learning</H3>
      <P>AI systems analyze student performance data to tailor educational content, ensuring that each learner receives customized support aligned with their unique needs.</P>
    </DIV>
    <DIV>
      <H3>Efficiency in Administration</H3>
      <P>Teachers can automate grading and administrative tasks, allowing them to focus on what truly matters—engaging with students and enhancing their learning experiences.</P>
    </DIV>
  </BULLETS>
  <IMG query="collage of diverse students using AI software, showing personalized learning experiences and teacher-student interactions" />
</SECTION>

<SECTION layout="right">
  <H2>Challenges and Ethical Concerns</H2>
  <ICONS>
    <DIV>
      <ICON query="warning sign" />
      <H3>Data Privacy</H3>
      <P>How can we ensure that student data is protected while leveraging AI technologies?</P>
    </DIV>
    <DIV>
      <ICON query="scale" />
      <H3>Equity in Access</H3>
      <P>Ensuring all students, regardless of background, have access to AI tools is essential for equitable education.</P>
    </DIV>
    <DIV>
      <ICON query="question mark" />
      <H3>Bias in Algorithms</H3>
      <P>How do we address the potential biases present in AI algorithms that could affect student assessment and opportunities?</P>
    </DIV>
  </ICONS>
  <IMG query="conceptual image of ethical dilemmas in AI education, featuring a digital scale balancing books and data privacy symbols" />
</SECTION>

<SECTION layout="vertical">
  <H2>Future Trends in AI-Based Learning</H2>
  <CYCLE>
    <DIV>
      <H3>Adaptive Learning Systems</H3>
      <P>Future AI will further enhance adaptive learning systems that evolve based on real-time data.</P>
    </DIV>
    <DIV>
      <H3>Virtual Reality Integration</H3>
      <P>AI will be integrated with VR to create immersive learning experiences that go beyond traditional classrooms.</P>
    </DIV>
    <DIV>
      <H3>Global Learning Networks</H3>
      <P>AI will facilitate collaboration across borders, allowing students to learn from global experts in real-time.</P>
    </DIV>
  </CYCLE>
  <IMG query="vision of future classrooms with VR headsets, diverse students collaborating globally through technology" />
</SECTION>

<SECTION layout="left">
  <H2>Conclusion and Call to Action</H2>
  <P>As we embrace AI in education, it’s vital to advocate for ethical practices and equitable access. Join us in shaping a future where technology empowers every learner.</P>
  <BULLETS>
    <DIV>
      <H3>Get Involved</H3>
      <P>Support initiatives that promote AI literacy and ethical standards in educational technology.</P>
    </DIV>
    <DIV>
      <H3>Stay Informed</H3>
      <P>Follow industry trends and engage in discussions about the future of AI in education.</P>
    </DIV>
  </BULLETS>
  <IMG query="inspiring image of diverse educators and students collaborating in a technology-rich learning environment, symbolizing hope and innovation" />
</SECTION>

</PRESENTATION>
\`\`\`
`

// Example generator for a custom text stream
async function* customTextStream() {
    //逐行读取example_ppt
    const lines = example_ppt.split('\n');
    for (const line of lines) {
      yield line;
      await new Promise(resolve => setTimeout(resolve, 500)); // Simulate async work
    }
}


export async function POST(req: Request) {
  try {
    const { title, outline, language, tone } =
      (await req.json()) as SlidesRequest;

    if (!title || !outline || !Array.isArray(outline) || !language) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 },
      );
    }
    const stream = iteratorToStream(customTextStream());
    return LangChainAdapter.toDataStreamResponse(stream);

  } catch (error) {
    console.error("Error in presentation generation:", error);
    return NextResponse.json(
      { error: "Failed to generate presentation slides" },
      { status: 500 },
    );
  }
}

```

## 解析模型的返回数据流
src/components/presentation/utils/parser.ts中的函数parseChunk