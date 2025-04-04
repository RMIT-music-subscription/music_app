import { ScanCommand, BatchGetItemCommand } from "@aws-sdk/client-dynamodb";
import { GetObjectCommand } from "@aws-sdk/client-s3";
import decodeJwtAndCheckExpiration from "@/lib/tokenVerification";
import { Buffer } from "buffer";
import {
  dynamoDbClient,
  s3Client,
  SUBSCRIBE_TABLE,
  MUSIC_TABLE,
  AWS_S3,
} from "@/lib/awsConnect";

// Convert DynamoDB response to a list of music objects
const musicResponse = async (data) => {
  const musicList = await Promise.all(
    data.map(async (music) => {
      const imgBase64 = await downloadAndConvertToBase64(
        `${music.artist.S.replace(/\s+/g, "").toLowerCase()}.jpg`
      );

      return {
        music_id: music.music_id.S,
        artist: music.artist.S,
        title: music.title.S,
        year: music.year.N,
        album: music.album.S,
        img_url: imgBase64,
      };
    })
  );

  return musicList;
};

// Fetch subscribed music for a user
const fetchMusic = async (email) => {
  try {
    // Scan for subscriptions
    const subscriptionResponse = await dynamoDbClient.send(
      new ScanCommand({
        TableName: SUBSCRIBE_TABLE,
        FilterExpression: "user_email = :email",
        ExpressionAttributeValues: { ":email": { S: email } },
      })
    );

    const subscriptionData = subscriptionResponse.Items || [];
    const musicIds = subscriptionData.map((item) => item.music_id.S);

    if (musicIds.length === 0) {
      return { message: "No music subscribed" };
    }

    // Fetch music details using BatchGetItem
    const batchResponse = await dynamoDbClient.send(
      new BatchGetItemCommand({
        RequestItems: {
          [MUSIC_TABLE]: {
            Keys: musicIds.map((music_id) => ({ music_id: { S: music_id } })),
          },
        },
      })
    );
    console.log(batchResponse, ":SUBSCRIBE_TABLE");
    const musicDetails = batchResponse.Responses?.[MUSIC_TABLE] || [];
    const response = await musicResponse(musicDetails);
    console.log(response, ":musicResponse");
    return response;
  } catch (error) {
    console.error("Error fetching music:", error);
    return { error: "Failed to fetch music" };
  }
};

// Download image from S3 and convert to base64
const downloadAndConvertToBase64 = async (imageKey) => {
  try {
    const response = await s3Client.send(
      new GetObjectCommand({
        Bucket: AWS_S3,
        Key: imageKey,
      })
    );

    const imageBuffer = await response.Body.transformToByteArray();
    return Buffer.from(imageBuffer).toString("base64");
  } catch (error) {
    console.error(`Error fetching image (${imageKey}):`, error);
    return null;
  }
};

export default async function handler(req, res) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Unauthorized: No token provided" });
  }

  // Extract the token after "Bearer "
  const token = authHeader.split(" ")[1];
  console.log(token, ":: roeen");
  // Decode JWT and get email
  const email = await decodeJwtAndCheckExpiration(token);

  if (!email) {
    return res.status(401).json({ error: "Unauthorized: Invalid token" });
  }
  const response = await fetchMusic(email);
  return res.status(200).json(response);
}
