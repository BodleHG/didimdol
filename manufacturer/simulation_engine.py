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
        self.send.register_engine("Scenario", "REAL_TIME", 1)
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
        load_dotenv(dotenv_path="manufacturer.env")

        TYPE = os.getenv('TYPE')
        WORKING_TIME = os.getenv('WORKING_TIME')
        TARGET_PRODUCTION = os.getenv('TARGET_PRODUCTION')
        FAILURE_RATE = os.getenv('FAILURE_RATE')
        DEFAULT_PRODUCTION_RATE = os.getenv('DEFAULT_PRODUCTION_RATE')
        CHECK_PRODUCTION_RATE = os.getenv('CHECK_PRODUCTION_RATE')
        SIMULATION_TIME_STEP = os.getenv('SIMULATION_TIME_STEP')
        ACCUMULATED_DEFECT_RATE = os.getenv('ACCUMULATED_DEFECT_RATE')

        print(
            f"*✅ Simulation Init\n"
            f"- 업종 : {TYPE}\n"
            f"- 총 작업시간 : {WORKING_TIME}h\n"
            f"- 목표 생산량 : {TARGET_PRODUCTION}\n"
            f"- 작업 실패율 : {FAILURE_RATE}\n"
            f"- 시간당 기본 생산량 : {DEFAULT_PRODUCTION_RATE}\n"
            f"- 시간당 최소 생산량 : {CHECK_PRODUCTION_RATE}\n"
            f"- 시뮬레이션 주기 : {SIMULATION_TIME_STEP}\n"
            f"- 누적 불량율 : {ACCUMULATED_DEFECT_RATE}"
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
        return input_class(WORKING_TIME, TARGET_PRODUCTION, FAILURE_RATE,
                           DEFAULT_PRODUCTION_RATE, CHECK_PRODUCTION_RATE, SIMULATION_TIME_STEP,
                            ACCUMULATED_DEFECT_RATE )


ScenarioManager()