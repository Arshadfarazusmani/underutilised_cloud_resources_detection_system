import dotenv from "dotenv";
dotenv.config({
    path:".env"
});


import { api_error } from "../util/api_error.js";
import { asyncHandler } from "../util/asyncHandler.js";
import jwt from "jsonwebtoken";
import { User } from "../models/user.model.js";


export const verifyJWT = asyncHandler(async(req, res, next) => { // Corrected 'resizeBy' to 'res'
    try {
        // Attempt to get token from cookies first, then from Authorization header
        // Ensure "Bearer " is correctly replaced (with a space after Bearer)
        const token = req.cookies?.accessToken || req.header("Authorization")?.replace("Bearer ", "");
        
        console.log("Extracted Token:", token); // Uncomment for debugging: check what token is received

        if (!token) {
            throw new api_error(401, "Unauthorized request: Access Token missing");
        }

        // Verify the token using the secret from environment variables
        // This is the line where "jwt malformed" error typically occurs if the token is invalid
        const decoded_Token =   jwt.verify(token, process.env.ACCESS_TOKEN_SECRET);
        
        console.log("Decoded Token Payload:", decoded_Token); // Uncomment for debugging: check decoded payload

   
        const user_id= decoded_Token.id

        console.log(user_id);
        

        // Find the user based on the _id from the decoded token
        // Select to exclude password and refreshToken for security
        const user = await User.findById(user_id).select("-password -refreshToken");

       

        if (!user) {
            // This case handles a valid token but an invalid/non-existent user ID
            throw new api_error(401, "Invalid Access Token: User associated with token not found");
        }

        // Attach the found user object to the request for subsequent middleware/controllers
        req.user = user;
        next(); // Pass control to the next middleware or route handler

    } catch (error) {
        // Log the actual error for server-side debugging
        console.error("JWT Verification Error:", error); 

        // Customize error message based on the type of JWT error
        if (error.name === "TokenExpiredError") {
            throw new api_error(401, "Access Token expired");
        } else if (error.name === "JsonWebTokenError") {
            // This catches "jwt malformed", "invalid signature", etc.
            throw new api_error(401, "Invalid access token");
        } else {
            // Catch any other unexpected errors
            throw new api_error(401, error?.message || "Authentication failed");
        }
    }
});

export const auth = (req, res, next) => {
  const token = req.headers["authorization"]?.split(" ")[1];
  if (!token) return res.status(401).json({ msg: "No token provided" });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ msg: "Invalid token" });
  }
};