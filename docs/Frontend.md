# 记录生成的原理
Main.tsx -> PresentationSlidesView.tsx (遍历Slides) -> SlideContainer.tsx (渲染单张Slide) ->
  presentation-editor.tsx (使用富文本编辑框架，根据数据渲染标题、图片、自定义图表等具体内容)。

# nextjs调用本机api生成内容
http://localhost:3000/api/presentation/generate

# DetailPanel.tsx的逻辑
1.显示处理中每个Agent的进度，首先src/app/api/presentation/generate/route.ts返回的数据包含metadata和type,并且是流式的返回Json的数据。
2. src/components/presentation/dashboard/PresentationGenerationManager.tsx 写新的函数，generatePresentationStream解析返回的数据const { type, data, metadata } = JSON.parse(line);
3. 根据不同的type类型，判断是否放到setDetailLogs还是parser.parseChunk(data);对xml格式进行解析。
4. DetailLogs数据通过zustand的usePresentationState保存，然后在src/components/presentation/presentation-page/Main.tsx中使用