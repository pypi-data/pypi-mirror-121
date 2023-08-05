from threading import Lock

from adoniram.exception.ProcessorNameConflictError import ProcessorNameConflictError
from adoniram.exception.ProcessorNotRegisteredError import ProcessorNotRegisteredError
from adoniram.exception.ProcessorRegistrationLocked import ProcessorRegistrationLocked


class ProcessorRegistration:
    def __init__(self):
        self.__processor_dict = {}
        self.__lock = Lock()
        self.__distributor_server_should_stop = False

    def stop_distributor_server(self):
        if self.__lock.acquire(blocking=True, timeout=5):
            self.__distributor_server_should_stop = True
            self.__lock.release()
        else:
            raise ProcessorRegistrationLocked()

    def should_distributor_server_stop(self):
        return self.__distributor_server_should_stop

    def register(self, name: str, host, port):
        if self.__lock.acquire(blocking=True, timeout=5):

            processor_name_conflict = False
            try:
                _ = self.__processor_dict[name]
                processor_name_conflict = True
            except KeyError:
                self.__processor_dict[name] = {
                    'host': host,
                    'port': port,
                    'processing_tasks': {},
                }

            self.__lock.release()

            if processor_name_conflict:
                raise ProcessorNameConflictError(name)
        else:
            raise ProcessorRegistrationLocked()

    def unregister(self, name: str):
        if self.__lock.acquire(blocking=True, timeout=5):
            processor_not_registered = False
            try:
                x = self.__processor_dict[name]

                if len(x['processing_tasks']):
                    # todo let the `processing_task`s dead
                    pass

                del self.__processor_dict[name]
            except KeyError:
                processor_not_registered = True

            self.__lock.release()

            if processor_not_registered:
                raise ProcessorNotRegisteredError(name)
        else:
            raise ProcessorRegistrationLocked()
