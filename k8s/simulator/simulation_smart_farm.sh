#!/bin/bash

set -e
echo "# 기존의 시뮬레이션 데이터를 초기화합니다."

DELETE_OUTPUT=$(kubectl delete -f yaml/smart_farm.yaml 2>&1) || true

if echo "$DELETE_OUTPUT" | grep -q "NotFound"; then
  echo "# 기존 데이터 없음."
else
  echo "# 데이터 초기화 성공."
fi

sleep 3

echo "# 스마트팜 시뮬레이션 준비 중..."

APPLY=$(kubectl apply -f yaml/smart_farm.yaml 2>&1) || true

APPLY_OUTPUT=$(kubectl apply -f yaml/smart_farm.yaml 2>&1) || true

if echo "$APPLY_OUTPUT" | grep -q "Error"; then
  echo "# 시뮬레이션 수행 과정에서 오류가 발생했습니다."
else
 sleep 7

 echo "# 스마트팜 시뮬레이션 수행 중."

 echo "# 시뮬레이션 결과."
 echo ""
 kubectl logs -n abs smart-farm-simulator
fi
