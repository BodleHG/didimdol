from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite

from model_create import Create
from model_select import Select

from mode_select import Mode_Select

from dotenv import load_dotenv
import importlib.util
import os

class ScenarioManager():
    def __init__(self) -> None:

        self.instance_class = self.class_import()

        self.Register_Engine()

    def Register_Engine(self):
        self.send = SystemSimulator()
        sim_mode = os.getenv("SIM_MODE", "REAL_TIME")
        self.send.register_engine("Scenario", sim_mode, 1)
        self.send_model = self.send.get_engine("Scenario")

        self.Insert_Port()

    def Insert_Port(self):
        self.send_model.insert_input_port("start")

        self.Mode_Select_m = Mode_Select(0, Infinite, "Mode_Select_m", "Scenario", self.instance_class) 
        self.Create_m = Create(0, Infinite, "Create_m", "Scenario") 
        self.Select_m = Select(0, Infinite, "Select_m", "Scenario") 

        self.Register_Entity()

    def Register_Entity(self):
        self.send_model.register_entity(self.Mode_Select_m)
        self.send_model.register_entity(self.Create_m)
        self.send_model.register_entity(self.Select_m)
        
        self.Copuling_Relation()

    def Copuling_Relation(self):

        self.send_model.coupling_relation(None, "start", self.Mode_Select_m, "start")
        self.send_model.coupling_relation(self.Mode_Select_m ,"done" , self.Create_m, "start")
        self.send_model.coupling_relation(self.Create_m ,"simulationDone" , self.Select_m, "start")

        self.start()


    def start(self):

        self.send_model.insert_external_event("start", "start")
        self.send_model.simulate()

    def stop(self):
        self.send.stop()
        


    def class_import(self):

        TYPE = os.getenv('TYPE', "smart_farm")
        TOTAL_DAY = os.getenv('TOTAL_DAY', 3)
        TARGET_PRODUCTION = os.getenv('TARGET_PRODUCTION', 50)
        FAILURE_RATE = os.getenv('FAILURE_RATE', 0.1)

        GROWTH_DAYS_REQUIRED = os.getenv('GROWTH_DAYS_REQUIRED', 0.8)

        SOIL_RANGE = os.getenv('SOIL_RANGE', "(40, 60)")
        HUMIDITY_RANGE = os.getenv('HUMIDITY_RANGE', "(50, 70)")
        TEMP_RANGE = os.getenv('TEMP_RANGE', "(18, 26)")

        ADJUST_INTERVAL = os.getenv('ADJUST_INTERVAL', 1)


        print(
            f"*✅ Simulation Init\n"
            f"- 업종 : {TYPE}\n"
            f"- 총 작업일 : {TOTAL_DAY}h\n"
            f"- 목표 생산량 : {TARGET_PRODUCTION}\n"
            f"- 작업 실패율 : {FAILURE_RATE}\n"
            f"- 작물 생성 시간(일) : {GROWTH_DAYS_REQUIRED}\n"
            f"- 땅습기의 정상 범위 : {SOIL_RANGE}\n"
            f"- 습도의 정상 범위 : {HUMIDITY_RANGE}\n"
            f"- 온도의 정상 범위 : {TEMP_RANGE}\n"
            f"- 환경 조절 간격 : {ADJUST_INTERVAL}"
        )
        print("-"*25)

        inputs_folder = 'scenarios'

        type_file = f"{TYPE}.py"
        type_path = os.path.join(inputs_folder, type_file)

        if not os.path.isfile(type_path):
            raise FileNotFoundError(f"{type_file} 파일이 inputs 폴더에 없습니다.")
        
        print(f"TYPE Class Load ...")
        spec = importlib.util.spec_from_file_location(TYPE, type_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        try:
            input_class = getattr(module, TYPE)
        except AttributeError:
            raise ImportError(f"{TYPE} 모듈에 {TYPE} 클래스가 없습니다.")
        
        print(f"TYPE Class Instantiate")
        return input_class(TOTAL_DAY,TARGET_PRODUCTION,FAILURE_RATE,
                           GROWTH_DAYS_REQUIRED,
                           SOIL_RANGE,HUMIDITY_RANGE,TEMP_RANGE,
                           ADJUST_INTERVAL)

if __name__ == "__main__":
    nodename = os.getenv("NODE_NAME", "default")
    print(f" # Current Node : {nodename}")
    ScenarioManager()