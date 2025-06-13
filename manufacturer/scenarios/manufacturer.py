import random
import time

class manufacturer:
    def __init__(self, working_hours, target_production, failure_rate, 
                 default_production_rate, check_production_rate, simulation_time_step, accumulated_defect_rate):
        self.working_hours = float(working_hours)
        self.target_production = float(target_production)
        self.failure_rate = float(failure_rate)

        self.production_rate = float(default_production_rate)
        self.check_production_rate = float(check_production_rate)

        self.time_step = float(simulation_time_step)

        self.total_produced = 0
        self.total_defects = 0
        self.production_log = []

        self.accumulated_failure_penalty = 0
        self.accumulated_defect_rate = float(accumulated_defect_rate)

        self.first_replacement_hour = None  # 처음 교체 경고가 발생한 시점 저장

        self.production_time = 0

    def run_condition(self):
        if self.total_produced >= self.target_production\
            or self.production_time >= self.working_hours:
            return False, False    
        else:
            is_failure = random.random() < self.failure_rate
            return True, is_failure

    def run(self):
        self.production_time += self.time_step  # 시간 경과 반영

        # 고장 패널티 반영된 생산속도
        effective_rate = self.production_rate * (1 - self.accumulated_failure_penalty)
        effective_rate = max(effective_rate, 0)

        # 생산 및 결함 계산
        produced = effective_rate * self.time_step
        defects = produced * self.accumulated_defect_rate

        self.total_produced += produced
        self.total_defects += defects

        # 교체 필요 판단
        needs_replacement = (
            effective_rate <= self.check_production_rate or
            self.accumulated_defect_rate >= 0.3
        )

        if needs_replacement and self.first_replacement_hour is None:
            self.first_replacement_hour = self.production_time

        # 로그 기록
        entry = {
            "hour": self.production_time,
            "is_failure": False,
            "effective_rate": effective_rate,
            "defect_rate": self.accumulated_defect_rate,
            "produced": produced,
            "defects": defects,
            "total_produced": self.total_produced,
            "total_defects": self.total_defects,
            "needs_replacement": needs_replacement
        }
        warning = " 🚨 [교체 필요]" if entry["needs_replacement"] else ""
        print(f"Hour {entry['hour']}: Produced {entry['produced']:.1f} units, "
            f"Defect Rate: {entry['defect_rate']:.2f}, "
            f"Effective Rate: {entry['effective_rate']:.1f}, "
            f"Total Produced: {entry['total_produced']:.1f}{warning}")
        self.production_log.append(entry)

    def run_fail(self):
        self.production_time += self.time_step  # 시간 경과 반영

        # 패널티 및 불량률 증가
        self.accumulated_failure_penalty += 0.1
        self.accumulated_defect_rate += 0.05

        # 고장 반영된 생산속도
        effective_rate = self.production_rate * (1 - self.accumulated_failure_penalty)
        effective_rate = max(effective_rate, 0)

        # 생산 및 결함 계산
        produced = effective_rate * self.time_step
        defects = produced * self.accumulated_defect_rate

        self.total_produced += produced
        self.total_defects += defects

        # 교체 필요 판단
        needs_replacement = (
            effective_rate <= self.check_production_rate or
            self.accumulated_defect_rate >= 0.3
        )

        if needs_replacement and self.first_replacement_hour is None:
            self.first_replacement_hour = self.production_time

        # 로그 기록
        entry = {
            "hour": self.production_time,
            "is_failure": True,
            "effective_rate": effective_rate,
            "defect_rate": self.accumulated_defect_rate,
            "produced": produced,
            "defects": defects,
            "total_produced": self.total_produced,
            "total_defects": self.total_defects,
            "needs_replacement": needs_replacement
        }
        warning = " 🚨 [교체 필요]" if entry["needs_replacement"] else ""
        print(f"Hour {entry['hour']}: Produced {entry['produced']:.1f} units, "
            f"Defect Rate: {entry['defect_rate']:.2f}, "
            f"Effective Rate: {entry['effective_rate']:.1f}, "
            f"Total Produced: {entry['total_produced']:.1f}{warning}")
        self.production_log.append(entry)
        

    def final_replacement_report(self):
        last_entry = self.production_log[-1]
        if self.first_replacement_hour is not None:
            # 해당 시점의 entry를 가져옴
            reason_entry = self.production_log[self.first_replacement_hour]
            defect_reason = reason_entry['defect_rate'] >= 0.3
            speed_reason = reason_entry['effective_rate'] <= self.production_rate * 0.5

            if defect_reason and speed_reason:
                reason_text = "불량률과 생산속도 모두 기준치를 초과"
            elif defect_reason:
                reason_text = "불량률이 기준치(0.30)를 초과"
            elif speed_reason:
                reason_text = f"생산속도가 기준치({self.production_rate * 0.5:.1f})개/h 이하로 하락"
            else:
                reason_text = "원인 불명 (논리 오류)"  # 이론상 발생하지 않음

            return (
                f"\n✅ 최종 보고:\n"
                f"- 목표 생산량: {self.target_production}개\n"
                f"- 실제 생산량: {last_entry['total_produced']:.0f}개\n"
                f"- 누적 불량률: {last_entry['defect_rate']:.2f}\n"
                f"- 최종 생산속도: {last_entry['effective_rate']:.2f}개/h\n"
                f"- 교체 판단 시점: Hour {self.first_replacement_hour}\n"
                f"👉 원인: {reason_text}\n"
                f"→ 기계 교체를 권장합니다."
            )
        else:
            return (
                f"\n✅ 최종 보고:\n"
                f"- 목표 생산량: {self.target_production}개\n"
                f"- 실제 생산량: {last_entry['total_produced']:.0f}개\n"
                f"- 누적 불량률: {last_entry['defect_rate']:.2f}\n"
                f"- 최종 생산속도: {last_entry['effective_rate']:.2f}개/h\n"
                f"→ 기계는 전체 기간 동안 정상 작동하였으며 교체는 필요하지 않습니다."
            )