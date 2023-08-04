def handler(event, context):
    if "authorization" in event["headers"]:
        return {
            "principalId": "anonymous",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": event["routeArn"],
                    },
                ],
            },
            "context": {
                "username": "fnascimento@gmail.com",
                "token": "blablabla"
            }
        }

    return {
        "principalId": "anonymous",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Deny",
                    "Resource": event["routeArn"],
                },
            ],
        },
    }
