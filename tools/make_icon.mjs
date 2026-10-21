// 用站点 logo 生成 Quartz 的站点图标（quartz/static/icon.png）
import sharp from "sharp"
import fs from "node:fs"

const src = "content/attachments/logo.svg"
const out = "quartz/static/icon.png"

if (!fs.existsSync(src)) {
  console.error(`找不到 ${src}`)
  process.exit(1)
}

await sharp(src, { density: 512 })
  .resize(512, 512, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } })
  .png()
  .toFile(out)
console.log(`已生成 ${out}`)
