#!/bin/bash
# Run this file (only once) to obtain the secrets to set in the GitHub repo

az login > /dev/null

SUBSCRIPTION_ID=$(az account show --query id -o tsv)

SP_OUTPUT=$(az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/$SUBSCRIPTION_ID" --query "{appId: appId, password: password, tenantId: tenant}" -o json)

echo "$SP_OUTPUT" | jq -r --arg sub_id "${SUBSCRIPTION_ID}" '. + {subscriptionId: $sub_id} | "\nARM_CLIENT_ID=\(.appId)\nARM_CLIENT_SECRET=\(.password)\nARM_TENANT_ID=\(.tenantId)\nARM_SUBSCRIPTION_ID=\(.subscriptionId)"'
