import boto3

class AWS:
    ACCESS_KEY = "ASIA2EYXJCO5HAYZPUHR"
    SECRET_KEY = "yXRZrztVAghLKlp322x799VvsBziHATaIvNBN1Ux"
    SESSION_TOKEN = "IQoJb3JpZ2luX2VjEJ7//////////wEaCXVzLXdlc3QtMiJGMEQCIAzlIfklJvGHxDSyQ/6R2Hi3xzkTG0bFsgH0xv1TBtU2AiAfWgd7rbchVxUyfGlJdRe6A8vVH09ZK/QvT0eHAcBh9Cq/AgiH//////////8BEAAaDDY5NzQ0NDE0NDA1OCIM5t+NVNAOz16IeDjnKpMCAcigJaMO3CSyHrWyhBEsz7QABb8XuMteTNs0NL7vuSHdBrWmGTlgwsuxOCuB7XyyXwGnB1ycJOeHvhnU3QmH9VP3bxqGyEjsJ1rl3qQ42o1pyLl2c6kM4qqKcuF+UZmERNH5zEYcdpCNoJu/6mniEZ9Pd8ahiy/dBbvlfNQ8AQ5MMhF+2BRZLRBWnrqz6z/xJGAQkxz/5zGc1GssTTOwc+DQAY40zHy5sOgiF3r9G6k3uKqBKriBhUUIUk5/1eOOqz2K1591A8+/L6i6fiX3YvGX95C7iUQECdJX3c84FBsH4/wMC3U9/JRoBcZZ3KPunT4zauKvjVegs0/mZuE1QKGAJ+wz/414wsyRJDkZYokSwGAw2ajJwgY6ngHqR7bQVipe6/gCT6zIBQNf6OK6o6lsO698Yqbdrk1Jj3YZcp06U4zIpoU8CPHR+meM9+NyBoNFyKmvj90FMn8xlZXFzC0rzoOpohyjVAuApH7TC9DjZTRnRIlCEi0jVxZ/1AQUNFHLHK3ayXO5jeMITcTNsYJ6zAa7QC2/muiSzbAq3SmILikUEhNMSGHEgmmbMiGuCQvj9lzVkOE/gw=="
    REGION = "us-east-1"
    AWS_S3 = "music-rmit-asv"
    LOGIN_TABLE = "login"
    MUSIC_TABLE = "music"
    SUBSCRIBE_TABLE = "subscribe"

    def aws_connect(service='dynamodb', resource=False):
        if resource:
            return boto3.resource(
                service,
                aws_access_key_id=AWS.ACCESS_KEY,
                aws_secret_access_key=AWS.SECRET_KEY,
                aws_session_token=AWS.SESSION_TOKEN,
                region_name=AWS.REGION
            )
        else:
            return boto3.client(
                service,
                aws_access_key_id=AWS.ACCESS_KEY,
                aws_secret_access_key=AWS.SECRET_KEY,
                aws_session_token=AWS.SESSION_TOKEN,
                region_name=AWS.REGION
            )
