/**
 * 中文属性名支持。
 *
 * Obsidian 的「笔记属性」里如果写的是中文键（标题、描述、日期…），
 * Quartz 是不认识的。这个插件在解析阶段把它们复制成对应的英文键，
 * 这样在 Obsidian 里怎么写都行，站点照常取到 title / description / tags…
 *
 * 规则：英文键优先，如果英文键已经有值，中文键不会覆盖它。
 */

const MAP = {
  标题: "title",
  描述: "description",
  摘要: "description",
  日期: "date",
  标签: "tags",
  别名: "aliases",
  导航: "nav",
  导航顺序: "navOrder",
  导航名称: "navLabel",
  上级: "parent",
}

export const CnProps = () => ({
  name: "CnProps",
  markdownPlugins() {
    return [
      () => (tree, file) => {
        const fm = file?.data?.frontmatter
        if (!fm || typeof fm !== "object") return
        for (const [cn, en] of Object.entries(MAP)) {
          const value = fm[cn]
          if (value === undefined || value === null) continue
          // 中文键优先：只要写了中文键，就以它为准（英文键会被覆盖）
          fm[en] = value
        }
      },
    ]
  },
})
