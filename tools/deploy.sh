#!/usr/bin/env bash
# 首次部署：推到 GitHub 并给出后续步骤
# 前提：已在 GitHub 建好空仓库 YYJ-lin/YYJKnowledgebase（不要初始化 README）
set -euo pipefail

cd "$(dirname "$0")/.."

REPO="git@github.com:YYJ-lin/YYJKnowledgebase.git"
BRANCH="$(git branch --show-current)"

echo "==> 检查远端仓库是否存在"
if ! git ls-remote "$REPO" >/dev/null 2>&1; then
  cat <<'EOF'
✗ 远端仓库还访问不到：git@github.com:YYJ-lin/YYJKnowledgebase.git

请先在 GitHub 建一个空仓库（不要勾选 README / .gitignore / license），然后重跑本脚本：

  1. https://github.com/new  ->  Repository name: YYJKnowledgebase
  2. 建好后执行: git push -u origin v5
  3. 仓库 Settings -> Pages -> Source 选 "GitHub Actions"
EOF
  exit 1
fi

echo "==> 推送 $BRANCH 到 $REPO"
git push -u origin "$BRANCH"

cat <<'EOF'

==> 推送完成。剩下两步在 GitHub 网页上：
    1. 仓库 Settings -> Pages -> Source 选 "GitHub Actions"
    2. Actions 里等 "Deploy 云屿集 to GitHub Pages" 跑完

线上地址: https://yyj-lin.github.io/YYJKnowledgebase/
若仓库名或域名变了，改 quartz.config.yaml 里的 baseUrl 再推一次即可。
EOF
