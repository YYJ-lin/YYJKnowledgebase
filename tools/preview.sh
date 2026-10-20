#!/usr/bin/env bash
# 构建 + 同步到本地预览目录 + 重启预览服务
# 用法: ./tools/preview.sh
set -euo pipefail

cd "$(dirname "$0")/.."
export PATH="$HOME/.local/node/bin:$PATH"

echo "==> 构建"
npx quartz build "$@"

echo "==> 同步到 /tmp/preview"
rm -rf /tmp/preview/YYJKnowledge-base.new
cp -r public /tmp/preview/YYJKnowledge-base.new
rm -rf /tmp/preview/YYJKnowledge-base
mv /tmp/preview/YYJKnowledge-base.new /tmp/preview/YYJKnowledge-base

echo "==> 重启预览服务"
systemctl --user restart yyj-quartz-preview

echo "预览地址: http://192.168.1.102:8095/YYJKnowledge-base/"
