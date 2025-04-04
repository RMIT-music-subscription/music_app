import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { S3Client } from "@aws-sdk/client-s3";

const ACCESS_KEY = "ASIA2EYXJCO5GZVZRB65";
const SECRET_KEY = "LpsbzuuvJz6ERJ2zXOBaNWemAu5nEFhNF4U7Sq7v";
const SESSION_TOKEN =
  "IQoJb3JpZ2luX2VjEJD//////////wEaCXVzLXdlc3QtMiJHMEUCIEQUJF3NM2h6t31iqe4DeYWDzBLJ2APdelrpz5OEHli9AiEApwdDxDKYOlEWCKOeoiNCtRJEab69ZuO0fZjbRB8qVTMqvwII+f//////////ARAAGgw2OTc0NDQxNDQwNTgiDMR0y17Z0V7EVra93yqTAnp0MV/kxnoXHorVZBoIY2qZEkKODZfMl+OkQCqjt615mU/g2IVOq5A/Rffhjcw595TTpi3XkDkG5IZe/01SISldhoMtycTVb2zejFrCPB6+V4uQXrBa7dGzEDbgiUAvroYQA7R0roCOOAiyvl2AjWmf0dOUFBcK3ZN7ipWpfaOnK4ul6EGb4CS5+dQISG6aM9ExpUYu6dQF9jjNQdbG0b2QEeY1Xqp6By29HnqgqsyxDywrHSktYrEEAgaIA7663hFyX8CKgVZNhwpaLbM3ZbhBiVeCJOh//Hfn8BIh9H2IocsyN5ZJu20l+hJckZ1PoeaZ9ck8mtH9kdgxllq2Gt1N5z1fRHrzDK/KImWHGKBDrCNpMM3IvL8GOp0BKPDkMjY9rgXbLlDAF4LTZrXkaB2I5vm5KZbRLOI9CYxCaCv20OWeF8zVqkxpnxS6CebV6dCYHRmH9jzQhKBex6nDJei9QmI4HRqDybK/qPj8PngHsn9rvv83yF/O3gAWKfovL6LA3Nyw2rE1BZofgfMYsweIIIZWG34okMcQCZyWtXUGZ0nKSuDqt0eqV8rhr98qUl2qUN23hz0QCg==";
const REGION = "us-east-1";
const AWS_S3 = "music-rmit-asv";
const LOGIN_TABLE = "login";
const MUSIC_TABLE = "music";
const SUBSCRIBE_TABLE = "subscribe";

const dynamoDbClient = new DynamoDBClient({
  region: REGION,
  credentials: {
    accessKeyId: ACCESS_KEY,
    secretAccessKey: SECRET_KEY,
    sessionToken: SESSION_TOKEN,
  },
});

const s3Client = new S3Client({
  region: REGION,
  credentials: {
    accessKeyId: ACCESS_KEY,
    secretAccessKey: SECRET_KEY,
    sessionToken: SESSION_TOKEN,
  },
});

export {
  dynamoDbClient,
  s3Client,
  AWS_S3,
  LOGIN_TABLE,
  MUSIC_TABLE,
  SUBSCRIBE_TABLE,
};
