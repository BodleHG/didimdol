#!/bin/bash

NAMESPACE="monitor"
LABEL="app=latency-monitor"
LOG_PATH="/tmp/latency.log"

echo "# 클러스터의 latency-monitor 로그 수집 시작"
echo "# Namespace: $NAMESPACE"
echo "# Label selector: $LABEL"
echo ""

PODS=$(kubectl get pods -n $NAMESPACE -l $LABEL -o jsonpath="{.items[*].metadata.name}")

if [ -z "$PODS" ]; then
  echo "⚠️  대상 Pod가 없습니다."
  exit 1
fi

TOTAL_SUM=0
TOTAL_COUNT=0

for pod in $PODS; do
  echo "=========================="
  echo "[Pod] $pod"
  echo "--------------------------"

  LOG=$(kubectl exec -n $NAMESPACE "$pod" -- cat "$LOG_PATH" 2>/dev/null)

  if [ -z "$LOG" ]; then
    echo "🚫 로그 파일 없음 또는 접근 실패"
    continue
  fi

  echo "$LOG"
  echo ""

  # 평균 지연시간 추출
  AVG_LINE=$(echo "$LOG" | grep "\[모든 노드 대상 평균 지연시간\]")
  AVG_VALUE=$(echo "$AVG_LINE" | grep -o '[0-9.]\+')

  if [ -n "$AVG_VALUE" ]; then
    TOTAL_SUM=$(echo "$TOTAL_SUM + $AVG_VALUE" | bc)
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
  fi
done

if [ "$TOTAL_COUNT" -gt 0 ]; then
  CLUSTER_AVG=$(echo "scale=3; $TOTAL_SUM / $TOTAL_COUNT" | bc)
  echo "=========================="
  echo "[클러스터 평균 지연시간] $CLUSTER_AVG ms"
else
  echo "=========================="
  echo "[클러스터 평균 지연시간] 계산 불가 (유효한 데이터 없음)"
fi

