import random
import ast

class smart_farm:
    def __init__(self, total_working_day, target_production, failure_rate, 
                 growth_days_required,
                 soil_range, humidity_range, temp_range,
                  adjust_interval):
        self.working_hours = int(total_working_day) * 24
        self.target_production = float(target_production)
        self.failure_rate = float(failure_rate)

        self.growth_days_required = float(growth_days_required)*24

        self.adjust_interval = float(adjust_interval)

        self.soil_min, self.soil_max = ast.literal_eval(soil_range)
        self.humidity_min, self.humidity_max = ast.literal_eval(humidity_range)
        self.temp_min, self.temp_max = ast.literal_eval(temp_range)

        self.time = 0
        self.interval_growth_hours = 0
        self.daily_growth = 0
        self.total_produced = 0

        self.production_log = []
        self.adjustment_effort = {"soil": 0, "humidity": 0, "temp": 0}
        self.adjust_log = []
        self.fail_log = []

        self.reset_environment()

    def reset_environment(self):
        self.soil = random.uniform(30, 70)
        self.humidity = random.uniform(30, 70)
        self.temp = random.uniform(10, 35)

    def run_condition(self):
        if self.total_produced >= self.target_production\
            or self.time >= self.working_hours:
            return False, False    
        else:
            is_failure = random.random() < self.failure_rate
            return True, is_failure

    def run(self):
        if self.time % self.adjust_interval == 0:
            self.adjust()  # 1. 조정은 run에서만
        self.evaluate_growth()   # 2. 조건 평가 및 생산 조건 누적
        self.step_environment()  # 3. 환경 악화
        self.time += 1           # 4. 시간 증가


    def run_fail(self):
        self.evaluate_growth()   # 1. 실패 조건에서도 평가 로직은 동일
        self.step_environment()  # 2. 환경 악화
        self.time += 1           # 3. 시간 증가


    def evaluate_growth(self):
        is_opt = self.is_optimal()
        
        if is_opt:
            self.interval_growth_hours += 1  # 1시간 단위로 누적

        if self.interval_growth_hours >= self.growth_days_required:
            self.total_produced += 1
            self.interval_growth_hours = 0

        # 로그 기록
        self.production_log.append({
            "time": self.time,
            "is_optimal": is_opt,
            "soil": self.soil,
            "humidity": self.humidity,
            "temp": self.temp,
            "produced": self.total_produced
        })

        warning = " 🚨 비정상" if not is_opt else ""
        day = self.time // 24
        hour = self.time % 24
        print(f"Day {day} / Hour {hour}: "
            f"Soil={self.soil:.1f}, Humidity={self.humidity:.1f}, Temp={self.temp:.1f}, "
            f"Produced={self.total_produced:.0f}{warning}")


    def is_optimal(self):
        return (self.soil_min <= self.soil <= self.soil_max and
                self.humidity_min <= self.humidity <= self.humidity_max and
                self.temp_min <= self.temp <= self.temp_max)

    def adjust(self):
        def adjust_val(val, min_val, max_val, step, key):
            before = val
            if val < min_val:
                val += step
            elif val > max_val:
                val -= step
            # 조정된 경우 카운트
            if before != val:
                self.adjustment_effort[key] += 1
            return val

        self.soil = adjust_val(self.soil, self.soil_min, self.soil_max, 5, "soil")
        self.humidity = adjust_val(self.humidity, self.humidity_min, self.humidity_max, 4, "humidity")
        self.temp = adjust_val(self.temp, self.temp_min, self.temp_max, 2, "temp")

    def step_environment(self):
        self.soil -= 0.05
        self.humidity -= 0.05
        self.temp -= 0.05

    def final_replacement_report(self):

        total_adjust = sum(self.adjustment_effort.values())
        
        if total_adjust == 0:
            reason = "→ 전체 기간 동안 환경 조정이 필요 없었습니다."
            problem = "없음"
        else:
            problem = max(self.adjustment_effort.items(), key=lambda x: x[1])[0]
            reasons = {
                "soil": "→ 땅습기 조정이 자주 필요했습니다.",
                "humidity": "→ 습도 조건이 자주 벗어났습니다.",
                "temp": "→ 온도 조정이 가장 많았습니다."
            }
            reason = reasons[problem]

        return (
            f"\n✅ 최종 보고:\n"
            f"- 목표 생산량: {self.target_production}\n"
            f"- 실제 생산량: {self.total_produced}\n"
            f"- 조절 횟수: 땅습기({self.adjustment_effort['soil']}), "
            f"습도({self.adjustment_effort['humidity']}), "
            f"온도({self.adjustment_effort['temp']})\n"
            f"- 가장 잦은 문제 요인: {problem} {reason}"
        )
