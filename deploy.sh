#!/bin/bash

# 커밋 메시지가 입력되지 않으면 기본값으로 "upgrade"를 사용
COMMIT_MSG=${1:-upgrade}

echo "📦 Git 자동 업로드를 시작합니다..."

git add .
git commit -m "$COMMIT_MSG"
git push

echo "✅ 성공적으로 GitHub에 코드가 업로드(Push) 되었습니다!"
