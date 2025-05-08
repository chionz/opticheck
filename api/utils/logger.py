import logging

'''# Configure the logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("error.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)'''



'''logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Use StreamHandler instead of FileHandler
)

logger = logging.getLogger(__name__)'''


try:
    # Configure the logging
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # Use StreamHandler for environments where FileHandler isn't allowed
            logging.StreamHandler()
        ],
    )

    logger = logging.getLogger(__name__)

except Exception as e:
    print(f"Error setting up logging: {e}")
    pass  # Ignore the error and continue