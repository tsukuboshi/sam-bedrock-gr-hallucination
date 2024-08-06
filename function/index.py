import logging
import os
from typing import Any, Dict

import boto3

logger = logging.getLogger()


def lambda_handler(event: Dict[Any, Any], context: Any) -> Any:
    model_id = os.getenv("MODEL_ID")
    model_region = os.getenv("MODEL_REGION")
    guardrail_id = os.getenv("GUARDRAIL_ID")

    br = boto3.client(
        service_name="bedrock-runtime",
        region_name=model_region,
    )

    with open("src/query.txt", "rt") as file:
        query = file.read()

    with open("src/document.pdf", "rb") as file:
        bs64 = file.read()

    logger.info(f"Query: {query}")

    gr_content = []
    query_content = {"text": {"text": query, "qualifiers": ["query"]}}
    gr_content.append(query_content)

    model_arn = f"arn:aws:bedrock:{model_region}::foundation-model/{model_id}"

    bar = boto3.client(
        service_name="bedrock-agent-runtime",
        region_name=model_region,
    )

    response = bar.retrieve_and_generate(
        input={"text": query},
        retrieveAndGenerateConfiguration={
            "type": "EXTERNAL_SOURCES",
            "externalSourcesConfiguration": {
                "modelArn": model_arn,
                "sources": [
                    {
                        "sourceType": "BYTE_CONTENT",
                        "byteContent": {
                            "contentType": "application/pdf",
                            "data": bs64,
                            "identifier": "document.pdf",
                        },
                    }
                ],
            },
        },
    )

    reference = []
    for citation in response["citations"]:
        for retrievedReference in citation["retrievedReferences"]:
            context = retrievedReference["content"]["text"]
            reference.append(context)

    reference = list(set(reference))
    grounding_source = "\n".join(reference)

    logger.info(f"Grounding Source: {grounding_source}")

    grounding_source_content = {
        "text": {"text": grounding_source, "qualifiers": ["grounding_source"]}
    }
    gr_content.append(grounding_source_content)

    output_control = os.getenv("OUTPUT_CONTROL")
    if output_control == "True":
        logger.info("Output control is enabled")
        with open("src/output.txt", "rt") as file:
            output = file.read()
    else:
        logger.info("Output control is disabled")
        output = response["output"]["text"]

    logger.info(f"Output: {output}")

    output_content = {
        "text": {
            "text": output,
        }
    }
    gr_content.append(output_content)

    guardrail_version = str(os.getenv("GUARDRAIL_VERSION"))

    gr_response = br.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=guardrail_version,
        source="OUTPUT",
        content=gr_content,
    )

    return gr_content, gr_response
