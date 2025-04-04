import { json } from "stream/consumers";
import { GetObjectCommand } from "@aws-sdk/client-s3";
import { QueryCommand, ScanCommand } from "@aws-sdk/lib-dynamodb";
import {
  dynamoDbClient,
  s3Client,
  AWS_S3,
  MUSIC_TABLE,
} from "@/lib/awsConnect";

import decodeJwtAndCheckExpiration from "@/lib/tokenVerification";

// Query Music from DynamoDB
// const queryMusic = async (query) => {
//   const { title, year, artist, album } = query;

//   if (!title && !year && !artist && !album) {
//     throw new Error("At least one field must be provided for the query.");
//   }

//   let filterExpression = [];
//   let expressionAttributeValues = {};

//   if (title) {
//     filterExpression.push("title = :title");
//     expressionAttributeValues[":title"] = title;
//   }
//   if (year) {
//     filterExpression.push("year = :year");
//     expressionAttributeValues[":year"] = Number(year);
//   }
//   if (artist) {
//     filterExpression.push("artist = :artist");
//     expressionAttributeValues[":artist"] = artist;
//   }
//   if (album) {
//     filterExpression.push("album = :album");
//     expressionAttributeValues[":album"] = album;
//   }

//   const params = {
//     TableName: MUSIC_TABLE,
//     FilterExpression: filterExpression.join(" AND "),
//     ExpressionAttributeValues: expressionAttributeValues,
//   };
//   console.log(params, ":: params");
//   try {
//     if (!dynamoDbClient) throw new Error("DynamoDB client is not initialized");

//     const command = new ScanCommand(params);
//     const data = await dynamoDbClient.send(command);

//     return data.Items ?? [];
//   } catch (error) {
//     console.error("Error querying dynamoDbClient:", error);
//     throw new Error("Database query failed");
//   }
// };

const queryMusic = async (query) => {
  const { title, year, artist, album } = query;

  if (!title && !year && !artist && !album) {
    throw new Error("At least one field must be provided for the query.");
  }

  let params = { TableName: MUSIC_TABLE };

  if (title && artist) {
    params.IndexName = "TitleIndex";
    params.KeyConditionExpression = "title = :title";
    params.ExpressionAttributeValues = { ":title": title };
  } else if (artist) {
    // Use ArtistIndex (artist = HASH)
    params.IndexName = "ArtistIndex";
    params.KeyConditionExpression = "artist = :artist";
    params.ExpressionAttributeValues = { ":artist": artist };
  } else if (album) {
    // Use AlbumIndex (album = HASH)
    params.IndexName = "AlbumIndex";
    params.KeyConditionExpression = "album = :album";
    params.ExpressionAttributeValues = { ":album": album };
  } else if (year) {
    // Use YearIndex (year = HASH)
    params.IndexName = "YearIndex";
    params.KeyConditionExpression = "year = :year";
    params.ExpressionAttributeValues = { ":year": Number(year) };
  } else {
    // Fallback to Scan (not recommended)
    let filterExpression = [];
    let expressionAttributeValues = {};

    if (title) {
      filterExpression.push("title = :title");
      expressionAttributeValues[":title"] = title;
    }
    if (year) {
      filterExpression.push("year = :year");
      expressionAttributeValues[":year"] = Number(year);
    }
    if (artist) {
      filterExpression.push("artist = :artist");
      expressionAttributeValues[":artist"] = artist;
    }
    if (album) {
      filterExpression.push("album = :album");
      expressionAttributeValues[":album"] = album;
    }

    params.FilterExpression = filterExpression.join(" AND ");
    params.ExpressionAttributeValues = expressionAttributeValues;
  }

  console.log(params, ":: params");
  try {
    if (!dynamoDbClient) throw new Error("DynamoDB client is not initialized");

    const command = new QueryCommand(params);
    const data = await dynamoDbClient.send(command);

    return data.Items ?? [];
  } catch (error) {
    console.error("Error querying dynamoDbClient:", error);
    throw new Error("Database query failed");
  }
};

// Download and Convert Image to Base64
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

// Convert DynamoDB Response to Music List
const musicResponseSearch = async (musicData) => {
  const musicList = await Promise.all(
    musicData.map(async (music) => {
      console.log(music);
      const imgBase64 = await downloadAndConvertToBase64(music.img_url);

      return {
        music_id: music.music_id,
        artist: music.artist,
        title: music.title,
        year: music.year,
        album: music.album,
        img_url: imgBase64,
      };
    })
  );

  return musicList;
};

// Main Lambda Handler
export default async function handler(req, res) {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({ error: "Unauthorized: No token provided" });
    }

    // Extract the token after "Bearer "
    const token = authHeader.split(" ")[1];

    await decodeJwtAndCheckExpiration(token);
    const query = req.query || {};

    const musicData = await queryMusic(query);
    const musicResponse = await musicResponseSearch(musicData);

    return res.status(200).json(musicResponse);
  } catch (error) {
    console.error("Error:", error);
    return res
      .status(500)
      .json({ error: error.message || "Internal Server Error" });
  }
}
