import logging
import os
from typing import Any, Dict

import boto3
import cfnresponse

logger = logging.getLogger()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    guardrail_id = os.getenv("GUARDRAIL_ID")

    if event["RequestType"] == "Create":
        response = create_grver(guardrail_id)
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {"Response": "Success"})
    if event["RequestType"] == "Update":
        print("No action needed for update")
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {"Response": "Success"})
    if event["RequestType"] == "Delete":
        print("No action needed for delete")
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {"Response": "Success"})

    return response


def create_grver(guardrail_id: str | None) -> Dict[str, Any]:
    b = boto3.client(
        service_name="bedrock",
    )

    response = b.create_guardrail_version(
        guardrailIdentifier=guardrail_id,
    )

    return response
