from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def handle_sku(self,skuList):
        pass