import logging
import os

# Create logs folder automatically
if not os.path.exists("logs"):
    os.makedirs("logs")

# Logger configuration
logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

    datefmt="%H:%M:%S",

    handlers=[

        logging.FileHandler(
            "logs/automation.log",
            mode="a"
        ),

        logging.StreamHandler()
    ]
)

logger = logging.getLogger()