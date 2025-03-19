import threading
import time

class PeriodicExecutor:
    def __init__(self, functions, interval):
        """
        Initialize the periodic executor.
        
        :param functions: List of functions to call periodically.
        :param interval: Time in seconds between function calls.
        """
        self.functions = functions
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None

    def start(self, timeout=None):
        """
        Start the periodic execution.
        
        :param timeout: Timeout in seconds, after which the periodic execution will stop automatically.
                        If None, the execution will run indefinitely until `stop()` is called.
        """
        def run():
            start_time = time.time()
            while not self._stop_event.is_set():
                for func in self.functions:
                    func()
                time.sleep(self.interval)
                if timeout is not None and (time.time() - start_time) >= timeout:
                    self.stop()

        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=run)
            self._thread.start()

    def stop(self):
        """Stop the periodic execution."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()
            self._thread = None


# Example Usage:
if __name__ == "__main__":
    def task1():
        print("Task 1 executed.")

    def task2():
        print("Task 2 executed.")

    # Initialize the PeriodicExecutor with a list of functions and an interval of 2 seconds.
    executor = PeriodicExecutor([task1, task2], interval=2)

    # Start the periodic execution with a timeout of 10 seconds.
    # executor.start(timeout=10)

    # Alternatively, start it indefinitely until `stop()` is called:
    executor.start()

    # To manually stop after some time:
    time.sleep(5)
    executor.stop()
