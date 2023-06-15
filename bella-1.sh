curl -X POST \
    -H "Authorization: Token $REPLICATE_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
            "input": {
                "instance_prompt": "a cby dog",
                "class_prompt": "photograph of a yorkie dog, 4k hd, high detail photograph, sharp lens, realistic, highly detailed, fur",
                "instance_data": "https://bella-content-bucket.s3.us-west-2.amazonaws.com/group+1.zip",
                "max_train_steps": 4000
            },
            "model": "tostangs/cby1",
            "trainer_version": "d5e058608f43886b9620a8fbb1501853b8cbae4f45c857a014011c86ee614ffb",
            "webhook_completed": "https://eopwey8aar9pi68.m.pipedream.net"
        }' \
    https://dreambooth-api-experimental.replicate.com/v1/trainings
