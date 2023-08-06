#   -*- coding: utf-8 -*-
#  Copyright (C) 2021 John "Preston" Mille <john@compose-x.io>
#  SPDX-License-Identifier: GPL-2.0

"""
AWS Secrets Lambda function to implement rotation
Based on AWS Function template
https://github.com/aws-samples/aws-secrets-manager-rotation-lambdas/blob/master/SecretsManagerRotationTemplate/lambda_function.py
"""

import json
import logging
import os
from tempfile import TemporaryDirectory

import boto3
from compose_x_common.compose_x_common import keyisset

from ccloud_cli_api.ccloud_cli_api import (
    api_key_exists,
    create_api_key,
    list_available_clusters,
    login,
)
from ccloud_cli_api.tools import replace_string_in_dict_values

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    arn = event["SecretId"]
    token = event["ClientRequestToken"]
    step = event["Step"]

    lambda_session = boto3.session.Session()
    service_client = lambda_session.client("secretsmanager")

    # Make sure the version is staged correctly
    metadata = service_client.describe_secret(SecretId=arn)
    if not metadata["RotationEnabled"]:
        logger.error("Secret %s is not enabled for rotation" % arn)
        raise ValueError("Secret %s is not enabled for rotation" % arn)
    versions = metadata["VersionIdsToStages"]
    if token not in versions:
        logger.error(
            "Secret version %s has no stage for rotation of secret %s." % (token, arn)
        )
        raise ValueError(
            "Secret version %s has no stage for rotation of secret %s." % (token, arn)
        )
    if "AWSCURRENT" in versions[token]:
        logger.info(
            "Secret version %s already set as AWSCURRENT for secret %s." % (token, arn)
        )
        return
    elif "AWSPENDING" not in versions[token]:
        logger.error(
            "Secret version %s not set as AWSPENDING for rotation of secret %s."
            % (token, arn)
        )
        raise ValueError(
            "Secret version %s not set as AWSPENDING for rotation of secret %s."
            % (token, arn)
        )
    temp_dir = TemporaryDirectory()
    if step == "createSecret":
        create_secret(arn, token, lambda_session, temp_dir=temp_dir)

    elif step == "setSecret":
        set_secret(service_client, arn, token)

    elif step == "testSecret":
        test_secret(arn, token, lambda_session, temp_dir=temp_dir)

    elif step == "finishSecret":
        finish_secret(arn, token, lambda_session)

    else:
        raise ValueError("Invalid step parameter")


def login_into_ccloud(lambda_session=None, temp_dir=None):
    if not os.environ.get("MASTER_PASSWORD_ARN", None):
        raise EnvironmentError("MASTER_PASSWORD_ARN is not defined. Cannot login")
    if lambda_session is None:
        lambda_session = boto3.session.Session()
    client = lambda_session.client("secretsmanager")
    master_password = client.get_secret_value(
        SecretId=os.environ.get("MASTER_PASSWORD_ARN")
    )["SecretString"]
    if isinstance(master_password, str):
        master_password = json.loads(master_password)
    login(
        email=master_password["email"],
        password=master_password["password"],
        temp_dir=temp_dir,
    )
    list_available_clusters()


def replace_kafka_credentials(previous_key_details, current_value, sr_key=None):
    new_api_key = create_api_key(
        service_account=previous_key_details["owner"],
        resource=previous_key_details["resource_id"],
    )
    new_value = replace_string_in_dict_values(
        current_value, current_value["SASL_USERNAME"], new_api_key["key"], True
    )
    replace_string_in_dict_values(
        new_value, current_value["SASL_PASSWORD"], new_api_key["secret"]
    )
    if sr_key and bool(os.environ.get("ENABLE_SR_ROTATION", False)):
        new_sr_key = create_api_key(
            service_account=sr_key["owner"], resource=sr_key["resource_id"]
        )
        new_value[
            "SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO"
        ] = f"{new_sr_key['key']}:{new_sr_key['secret']}"

    return new_value


def create_secret(arn, token, session=None, temp_dir=None):
    """
    Create the secret

    This function first checks for the existence of a secret for the passed in token.
    If one does not exist, it will generate a new secret and put it with the passed in token.

    :param str arn: The secret ARN or other identifier
    :param str token: The ClientRequestToken associated with the secret version
    :param boto3.session.Session session:
    :raises: ResourceNotFoundException: If the secret with the specified arn and stage does not exist
    """
    if session is None:
        session = boto3.session.Session()
    service_client = session.client("secretsmanager")

    current_value = service_client.get_secret_value(
        SecretId=arn, VersionStage="AWSCURRENT"
    )["SecretString"]
    if isinstance(current_value, str):
        current_value = json.loads(current_value)
        required_keys = [
            "SASL_USERNAME",
            "SASL_PASSWORD",
        ]
        if (
            "SASL_USERNAME" not in current_value.keys()
            or "SASL_PASSWORD" not in current_value.keys()
        ):
            raise KeyError(
                required_keys, "must be present in secret. Got", current_value.keys()
            )

    try:
        service_client.get_secret_value(
            SecretId=arn, VersionId=token, VersionStage="AWSPENDING"
        )
        logger.info("createSecret: Successfully retrieved secret for %s." % arn)
    except service_client.exceptions.ResourceNotFoundException:
        login_into_ccloud(lambda_session=session, temp_dir=temp_dir)
        previous_key_details = api_key_exists(current_value["SASL_USERNAME"])
        sr_user_info = (
            api_key_exists(
                current_value["SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO"].split(":")[0]
            )
            if keyisset("SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO", current_value)
            else None
        )
        if not previous_key_details:
            raise LookupError(
                f"Failed to find the key {current_value['SASL_USERNAME']}"
            )
        try:
            new_value = replace_kafka_credentials(
                previous_key_details, current_value, sr_user_info
            )
            service_client.put_secret_value(
                SecretId=arn,
                ClientRequestToken=token,
                SecretString=json.dumps(new_value),
                VersionStages=["AWSPENDING"],
            )
            logger.info(
                "createSecret: Successfully put secret for ARN %s and version %s."
                % (arn, token)
            )
        except Exception as error:
            logger.error(
                "createSecret: Failed to create a new secret for ARN %s and version %s."
                % (arn, token)
            )
            logger.error(error)


def set_secret(service_client, arn, token):
    """Set the secret

    This method should set the AWSPENDING secret in the service that the secret belongs to. For example, if the secret is a database
    credential, this method should take the value of the AWSPENDING secret and set the user's password to this value in the database.

    Args:
        service_client (client): The secrets manager service client

        arn (string): The secret ARN or other identifier

        token (string): The ClientRequestToken associated with the secret version

    """
    # This is where the secret should be set in the service
    # raise NotImplementedError
    return


def test_secret(arn, token, lambda_session=None, temp_dir=None):
    """Test the secret

    This method should validate that the AWSPENDING secret works in the service that the secret belongs to. For example, if the secret
    is a database credential, this method should validate that the user can login with the password in AWSPENDING and that the user has
    all of the expected permissions against the database.

    Args:
        service_client (client): The secrets manager service client

        arn (string): The secret ARN or other identifier

        token (string): The ClientRequestToken associated with the secret version

    """
    # This is where the secret should be tested against the service
    # raise NotImplementedError
    if lambda_session is None:
        lambda_session = boto3.session.Session()
    login_into_ccloud(lambda_session=lambda_session, temp_dir=temp_dir)
    service_client = lambda_session.client("secretsmanager")
    temp_secret = service_client.get_secret_value(
        SecretId=arn, VersionId=token, VersionStage="AWSPENDING"
    )["SecretString"]
    if isinstance(temp_secret, str):
        temp_secret = json.loads(temp_secret)
    if not api_key_exists(temp_secret["SASL_USERNAME"]):
        raise LookupError(
            f"Failed to confirm that key {temp_secret['SASL_USERNAME']} exists"
        )
    return


def finish_secret(arn, token, lambda_session=None):
    """Finish the secret

    This method finalizes the rotation process by marking the secret version passed in as the AWSCURRENT secret.

    Args:
        service_client (client): The secrets manager service client

        arn (string): The secret ARN or other identifier

        token (string): The ClientRequestToken associated with the secret version

    Raises:
        ResourceNotFoundException: If the secret with the specified arn does not exist

    """
    # First describe the secret to get the current version
    if lambda_session is None:
        lambda_session = boto3.session.Session()
    service_client = lambda_session.client("secretsmanager")
    metadata = service_client.describe_secret(SecretId=arn)
    current_version = None
    for version in metadata["VersionIdsToStages"]:
        if "AWSCURRENT" in metadata["VersionIdsToStages"][version]:
            if version == token:
                # The correct version is already marked as current, return
                logger.info(
                    "finishSecret: Version %s already marked as AWSCURRENT for %s"
                    % (version, arn)
                )
                return
            current_version = version
            break

    # Finalize by staging the secret version current
    service_client.update_secret_version_stage(
        SecretId=arn,
        VersionStage="AWSCURRENT",
        MoveToVersionId=token,
        RemoveFromVersionId=current_version,
    )
    logger.info(
        "finishSecret: Successfully set AWSCURRENT stage to version %s for secret %s."
        % (token, arn)
    )
