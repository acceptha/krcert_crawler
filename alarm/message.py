import abc


class MessengerBase:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_last_notice(self):
        pass

    @abc.abstractmethod
    def post_notice(self, text):
        pass
