from pyevsim import BehaviorModelExecutor, Infinite, SysMessage

class Mode_Select(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, dy_class):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.insert_state("Done",1)


        self.insert_input_port("start")
        self.insert_output_port("mode_out")

        self.dy_class = dy_class

 
    def ext_trans(self, port, msg):
        if port == "start":
            self._cur_state = "Generate"


    def output(self):
        if self._cur_state == "Generate":
            print(
                f"-----------------------------------\n"
                f"--------- Simulation Start --------\n"
                f"-----------------------------------"
            )
            self._cur_state = "Done"

        if self._cur_state == "Done":
            msg = SysMessage(self.get_name(), "done")
            msg.insert(self.dy_class)
            return msg

    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Done"
        elif self._cur_state == "Done":
            self._cur_state = "Wait"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"
    
