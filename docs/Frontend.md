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

## 根据图片是否是背景图片对图片进行展示, 背景图片，那么样式是object-cover，如果不是背景图片，那么样式是contain，即缩放显示，显示全图
src/components/presentation/editor/native-elements/root-image.tsx
                <PopoverTrigger asChild>
                  <div
                    className="relative h-full"
                    tabIndex={0}
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowDeletePopover(true);
                    }}
                    onDoubleClick={handleImageDoubleClick}
                  >
                    {/*  eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={imageUrl ?? image.url}
                      alt={image.alt}
                      className={`h-full w-full ${image.background ? "object-cover" : "object-contain"}`}
                      style={{
                        height: image.background !== true && image.alt ? "calc(100% - 32px)" : "100%",
                        // 32px 用于说明文字实际高度调整
                      }}
                      onError={(e) => {
                        console.error(
                          "Image failed to load:",
                          e,
                          imageUrl ?? image.url
                        );
                        // Optionally set a fallback image or show an error state
                      }}  
                    />
                    {/* 非背景图片时显示说明文字 */}
                    {image.background !== true && image.alt && (
                      <div
                        style={{
                          position: "absolute",
                          left: "50%",
                          bottom: 0,
                          transform: "translateX(-50%)",
                          background: "rgba(0,0,0,0.6)",
                          color: "#fff",
                          padding: "2px 8px",
                          borderRadius: "6px 6px 0 0",
                          fontSize: "0.85rem",
                          whiteSpace: "pre-line",
                          maxWidth: "90%",
                          textAlign: "center",
                        }}
                      >
                        {image.alt}
                      </div>
                    )}
                  </div>
                </PopoverTrigger>


## PPT页的唯一性，避免遗漏和重复，目前是使用的generateSectionIdentifier函数，使用的是h1Node的内容作为key，我们新加大模型输出<SECTION layout="left" | "right" | "vertical" page_number=x>，page_number作为唯一key，那样可以覆盖已有PPT，方便PPT_checker更新PPT内容
  private generateSectionIdentifier(sectionNode: XMLNode): string {
    // 优先使用 page_number 作为唯一标识
    if (sectionNode.attributes && sectionNode.attributes.page_number) {
      return `page_number-${sectionNode.attributes.page_number}`;
    }
