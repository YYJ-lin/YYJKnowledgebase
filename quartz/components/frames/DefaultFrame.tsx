import { PageFrame, PageFrameProps } from "./types"
import HeaderConstructor from "../Header"

const Header = HeaderConstructor()

/**
 * The default page frame — three-column layout with a full-width top bar,
 * left sidebar, center content (breadcrumbs + body + afterBody), and right
 * sidebar, followed by a footer.
 *
 * 与上游的区别：header 位置的组件被抽到 #quartz-body 的根层级（.topbar），
 * 并让 grid 的 grid-header 区域横跨所有列，从而做出通栏导航条；
 * 原来的 .page-header 只保留 beforeBody（面包屑、标题、元信息）。
 */
export const DefaultFrame: PageFrame = {
  name: "default",
  render({
    componentData,
    header,
    beforeBody,
    pageBody: Content,
    afterBody,
    left,
    right,
    footer,
  }: PageFrameProps) {
    return (
      <>
        {header.length > 0 && (
          <div class="topbar">
            <div class="topbar-inner">
              <Header {...componentData}>
                {header.map((HeaderComponent) => (
                  <HeaderComponent {...componentData} />
                ))}
              </Header>
            </div>
          </div>
        )}
        <div class="left sidebar">
          {left.map((BodyComponent) => (
            <BodyComponent {...componentData} />
          ))}
        </div>
        <div class="center">
          <div class="page-header">
            <div class="popover-hint">
              {beforeBody.map((BodyComponent) => (
                <BodyComponent {...componentData} />
              ))}
            </div>
          </div>
          <Content {...componentData} />
          <hr />
          <div class="page-footer">
            {afterBody.map((BodyComponent) => (
              <BodyComponent {...componentData} />
            ))}
          </div>
        </div>
        <div class="right sidebar">
          {right.map((BodyComponent) => (
            <BodyComponent {...componentData} />
          ))}
        </div>
        {footer.map((FooterComponent) => (
          <FooterComponent {...componentData} />
        ))}
      </>
    )
  },
}
