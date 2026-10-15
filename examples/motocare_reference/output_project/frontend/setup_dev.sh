#!/usr/bin/env bash
set -e
echo "🚀 [Mobile] Cài đặt dependencies và khởi chạy Expo development server..."
if ! command -v node &> /dev/null; then
    echo "❌ Lỗi: Node.js chưa được cài đặt. Vui lòng cài đặt Node.js v18+."
    exit 1
fi
npm install
echo "✔ Cài đặt hoàn tất. Khởi chạy Expo..."
npx expo start
