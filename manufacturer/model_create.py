from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import random


class Create(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)

        self.insert_state("Run",1)
        self.insert_state("Done",1)

        self.insert_input_port("start")
        self.insert_output_port("simulationDone")

 
    def ext_trans(self, port, msg):
        if port == "start":
            self.class_msg = msg.retrieve()[0]
            self._cur_state = "Generate"


    def output(self):
        if self._cur_state == "Generate":
            self._cur_state = "Run"
         

        if self._cur_state == "Run":
            condition_result, is_failure = self.class_msg.run_condition()
            if condition_result and is_failure:
                self.class_msg.run()
                self._cur_state = "Generate"
            elif condition_result == True and is_failure == False:
                self.class_msg.run_fail()
                self._cur_state = "Generate"
            elif condition_result == False and is_failure == False:
                self._cur_state = "Done"
            

        if self._cur_state == "Done":
            
            msg = SysMessage(self.get_name(), "simulationDone")
            msg.insert(self.class_msg)
            return msg


    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Run"

        if self._cur_state == "Run":
            self._cur_state = "Generate"
        elif self._cur_state == "Run":
            self._cur_state = "Done"

        if self._cur_state == "Done":
            self._cur_state = "Wait"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"

        if self._cur_state == "Generate":
            self._cur_state = "Generate"

