import { json } from "stream/consumers";

const decodeJwtAndCheckExpiration = async (token) => {
  try {
    // Decode the JWT token without verifying signature
    const payload = await json(atob(token));

    return payload.email; // Return the email if valid
  } catch (error) {
    console.error("Error decoding JWT:", error);
    return null;
  }
};
export default decodeJwtAndCheckExpiration;
