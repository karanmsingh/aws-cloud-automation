import argparse
import json
import logging
import sys
from typing import Any, Dict, List, Optional
import boto3
from botocore.exceptions import BotoCoreError, ClientError


# =====================================================================
# 1. Structured Logging Setup
# =====================================================================
class JSONFormatter(logging.Formatter):
    """Formats log records as structured JSON for operational observability."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_data.update(record.extra)
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


def setup_logger(verbose: bool = False) -> logging.Logger:
    logger = logging.getLogger("aws_ops")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    logger.handlers = []  # Clear default handlers
    logger.addHandler(handler)
    return logger


# =====================================================================
# 2. Operational Automation Class
# =====================================================================
class AWSOpsManager:
    """Manages AWS operational tasks with error handling and dry-run safety."""

    def __init__(
        self,
        region: str = "us-east-1",
        dry_run: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        self.region = region
        self.dry_run = dry_run
        self.logger = logger or logging.getLogger("aws_ops")
        
        # Initialize boto3 clients/resources safely
        try:
            self.session = boto3.Session(region_name=self.region)
            self.ec2_client = self.session.client("ec2")
        except (BotoCoreError, ClientError) as e:
            self.logger.error(
                f"Failed to initialize AWS session: {e}",
                extra={"extra": {"region": self.region}},
            )
            raise

    def stop_instances_by_tag(
        self, tag_key: str, tag_value: str
    ) -> List[str]:
        """Finds and stops instances matching specific tags. Supports dry-run."""
        log_extra = {"extra": {"tag_key": tag_key, "tag_value": tag_value, "dry_run": self.dry_run}}
        self.logger.info("Starting instance cleanup process", extra=log_extra)

        # Step 1: Query Target Resources
        try:
            response = self.ec2_client.describe_instances(
                Filters=[
                    {"Name": f"tag:{tag_key}", "Values": [tag_value]},
                    {"Name": "instance-state-name", "Values": ["running"]},
                ]
            )
        except ClientError as err:
            self.logger.error(f"Failed to query EC2 instances: {err}", extra=log_extra)
            return []

        # Extract Instance IDs
        instance_ids = [
            instance["InstanceId"]
            for reservation in response.get("Reservations", [])
            for instance in reservation.get("Instances", [])
        ]

        if not instance_ids:
            self.logger.info("No matching running instances found", extra=log_extra)
            return []

        log_extra["extra"]["target_instances"] = instance_ids

        # Step 2: Execute Action or Perform Dry-Run
        if self.dry_run:
            self.logger.info(
                f"[DRY-RUN] Would stop {len(instance_ids)} instances: {instance_ids}",
                extra=log_extra,
            )
            return instance_ids

        try:
            self.logger.info(
                f"Executing stop request for instances: {instance_ids}",
                extra=log_extra,
            )
            self.ec2_client.stop_instances(InstanceIds=instance_ids)
            self.logger.info("Stop signal successfully sent", extra=log_extra)
            return instance_ids

        except ClientError as err:
            self.logger.error(
                f"AWS ClientError during stop execution: {err.response['Error']['Message']}",
                extra=log_extra,
            )
            return []
        except BotoCoreError as err:
            self.logger.error(f"SDK error encountered: {err}", extra=log_extra)
            return []


# =====================================================================
# 3. CLI Entrypoint
# =====================================================================
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Operational tooling script for AWS automation tasks."
    )
    parser.add_argument(
        "--region", default="us-east-1", help="AWS region (default: us-east-1)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute actions directly (default is Dry-Run mode)",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable DEBUG log level"
    )
    parser.add_argument(
        "--tag-key", default="Environment", help="Tag key to match"
    )
    parser.add_argument(
        "--tag-value", default="Dev", help="Tag value to match"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logger = setup_logger(verbose=args.verbose)

    # Invert execute flag so default state is safe (dry_run=True)
    is_dry_run = not args.execute

    if is_dry_run:
        logger.info("Running in SAFE mode (Dry-Run enabled). Pass --execute to run changes.")

    try:
        manager = AWSOpsManager(
            region=args.region,
            dry_run=is_dry_run,
            logger=logger,
        )
        manager.stop_instances_by_tag(
            tag_key=args.tag_key,
            tag_value=args.tag_value,
        )
    except Exception as e:
        logger.critical(f"Unhandled operational failure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
