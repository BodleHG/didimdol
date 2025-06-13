from pyevsim import BehaviorModelExecutor, Infinite, SysMessage

class Select(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.insert_state("Done",1)

        self.insert_input_port("start")


    def ext_trans(self, port, msg):
        if port == "start":
            print(
                f"-----------------------------------\n"
                f"--------- Simulation Done ---------\n"
                f"-----------------------------------"
            )
            self.class_msg = msg.retrieve()[0]
            print(self.class_msg.final_replacement_report())

            self._cur_state = "Generate"


    def output(self):
        if self._cur_state == "Generate":
            self._cur_state = "Wait"


    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Wait"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"
