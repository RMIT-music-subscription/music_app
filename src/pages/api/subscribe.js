import decodeJwtAndCheckExpiration from "@/lib/tokenVerification";
import axios from "axios";
import { json } from "stream/consumers";
import { config } from "@/lib/constant";

export default async function handler(req, res) {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({ error: "Unauthorized: No token provided" });
    }

    // Extract the token after "Bearer "
    const token = authHeader.split(" ")[1];

    const email = await decodeJwtAndCheckExpiration(token);
    let response = null;
    if (req.method === "POST") {
      response = await axios.post(`${config.url}/subscribe`, {
        email,
        music_id: req.body.music_id,
      });
    } else if (req.method === "DELETE") {
      response = await axios.delete(`${config.url}/unsubscribe`, {
        data: {
          email,
          music_id: req.body.music_id,
        },
      });
    } else {
      return res.status(400).json({ error: "Not Allowed" });
    }

    return res.status(response.data.statusCode).send(response.data.body);
  } catch (error) {
    console.error("Error:", error);
    return res
      .status(500)
      .json({ error: error.message || "Internal Server Error" });
  }
}
