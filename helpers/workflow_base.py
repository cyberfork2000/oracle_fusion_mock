import time
import functools
import logging
from helpers.errors import WorkflowError

# Configure global logger for workflows
logger = logging.getLogger("workflow_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def retry(times=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, times + 1):
                try:
                    logger.info(f"Executing step '{func.__name__}' (Attempt {attempt}/{times})")
                    result = func(*args, **kwargs)
                    logger.info(f"Step '{func.__name__}' succeeded")
                    return result
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Step '{func.__name__}' failed on attempt {attempt}: {e}")
                    if attempt < times:
                        time.sleep(delay)
            # If all attempts fail, raise WorkflowError
            logger.error(f"Step '{func.__name__}' failed after {times} attempts")
            raise WorkflowError(f"Failed after {times} attempts: {last_exception}") from last_exception
        return wrapper
    return decorator


def poll(condition_func, timeout=10, interval=1, error_msg=None):
    """Poll a condition until True or timeout."""
    start = time.time()
    while True:
        try:
            if condition_func():
                logger.info("Polling condition satisfied")
                return True
        except Exception as e:
            logger.warning(f"Polling encountered an exception: {e}")
        if time.time() - start > timeout:
            logger.error(error_msg or "Polling timeout reached")
            raise WorkflowError(error_msg or "Polling timeout reached")
        time.sleep(interval)


class BaseWorkflow:
    """Base class for domain workflows with logging and step reporting."""

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    @retry(times=3, delay=2)
    def execute_step(self, func, *args, **kwargs):
        """Execute a workflow step with retry and logging."""
        logger.info(f"Executing workflow step: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Workflow step '{func.__name__}' completed successfully")
        return result

    def wait_until(self, condition_func, timeout=10, interval=1, error_msg=None):
        """Poll until condition returns True or timeout."""
        logger.info("Starting polling for condition...")
        return poll(condition_func, timeout, interval, error_msg)
