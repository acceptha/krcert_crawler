import abc


class SenderBase:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_last_notice(self):
        pass

    @abc.abstractmethod
    def send_notice(self, content):
        pass
