from abc import ABC, abstractmethod

class ILeaveValidator(ABC):
    @abstractmethod
    def validate_leave_request(self):
        pass
    
    
class ILeaveLimitValidator(ABC):
    @abstractmethod
    def validate(self):
        pass
    

class ILeaveOverlapValidator(ABC):
    @abstractmethod
    def validate(self):
        pass
    

class ILeaveCreator(ABC):
    @abstractmethod
    def create_leave(self):
        pass
    

class ILeaveFactory(ABC):
    @abstractmethod
    def handle_leave_request(self):
        pass