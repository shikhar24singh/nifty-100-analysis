from loguru import logger

logger.add(
    "logs/project.log",
    rotation="1 MB",
    level="INFO"
)

logger.info("Logger initialized")