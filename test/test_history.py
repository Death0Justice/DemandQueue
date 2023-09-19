from ..demand_queue import DemandQueue
import pytest

class TestHistory():
    
    def setup(self):
        self.demand_queue = DemandQueue()
        self.test_tuple = ["我", "以撒小蓝人", "2023-9-12 15:08"]
        self.bad_tuple = ["我", "az百变怪", "2023-12-12"]
    
    def test_push(self):
        pre_len = len(self.demand_queue.history)
        self.demand_queue.name.setText(self.test_tuple[0])
        self.demand_queue.desc.setText(self.test_tuple[1])
        self.demand_queue.date.setText(self.test_tuple[2])
        self.demand_queue.push_queue()
        assert len(self.demand_queue.history) == pre_len + 1
        assert self.demand_queue.history[0] == ["我", "以撒小蓝人", "2023-9-12 15:08"]
    
    def test_append(self):
        pre_len = len(self.demand_queue.history)
        self.demand_queue.name.setText(self.test_tuple[0])
        self.demand_queue.desc.setText(self.test_tuple[1])
        self.demand_queue.date.setText(self.test_tuple[2])
        self.demand_queue.append_queue()
        assert len(self.demand_queue.history) == pre_len + 1
        assert self.demand_queue.history[-1] == ["我", "以撒小蓝人", "2023-9-12 15:08"]
    
    def test_insert(self):
        row = 5
        pre_len = len(self.demand_queue.history)
        self.demand_queue.name.setText(self.test_tuple[0])
        self.demand_queue.desc.setText(self.test_tuple[1])
        self.demand_queue.date.setText(self.test_tuple[2])
        self.demand_queue.insert_place.setText(row)
        self.demand_queue.insert_queue()
        assert len(self.demand_queue.history) == pre_len + 1
        assert self.demand_queue.history[4] == ["我", "以撒小蓝人", "2023-9-12 15:08"]
    
    def test_pop(self):
        assert self.demand_queue.history[0] == ["小蓝人", "亚伯伦禁主动回溯线", "2023-9-9 15:08"]
        pre_len = len(self.demand_queue.history)
        self.demand_queue.pop_queue()
        assert len(self.demand_queue.history) == pre_len - 1
        assert self.demand_queue.history[0] == ["老板", "埃里克金佛埃及而我i范吉奥i恶杰佛爱好奥i金佛改建为欧冠i骄傲沃尔覅骄傲地说哦啊的空间佛奥尔加拉孔金瓯覅几哦啊科技骄傲的咖啡机奥恩科举附魔埃里克大家发哦了肯定就发哦恩科举佛ask的减肥操", "2023-2-1 15:08"]
    
    def test_quick_action_single(self):
        assert not self.demand_queue.name.toPlainText()
        assert not self.demand_queue.desc.toPlainText()
        assert not self.demand_queue.date.toPlainText()