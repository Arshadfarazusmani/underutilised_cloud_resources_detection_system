import { asyncHandler } from "../util/asyncHandler.js";
import jwt from "jsonwebtoken";
import { User } from "../models/user.model.js";
import dotenv from "dotenv";
dotenv.config({
    path:".env"
}); 
import { api_error } from "../util/api_error.js";
import { api_response } from "../util/api-response.js";

// Function to generate Access and Refresh Tokens

const generateAccessTokenAndRefreshToken = async(user_id)=>{
    console.log("Attempting to generate tokens for user_id:", user_id); // Log the ID being used

    const user = await User.findById(user_id); // This is the line that fetches the user

    // --- ADD THIS CHECK ---
    if (!user) {
        console.error("ERROR: User not found with ID:", user_id); // Crucial log
        throw new api_error(404, "User not found for token generation.");
    }
    // --- END ADDED CHECK ---

    console.log("User found:", user.name, user.email); // Confirm user object is retrieved

    const accessToken= user.generateAccessToken(); // Ensure it's called as a function
    const refreshToken= user.generateRefreshToken(); // Ensure it's called as a function

    user.refreshToken=refreshToken;

    await user.save({validateBeforeSave:false});


    

    return {accessToken , refreshToken};
};
 

// register controller

const register_controller= asyncHandler(async (req,res)=>{
    const {name,email,password}= req.body;

    // check for all fields
    if(!name|| !email || !password){
    throw new api_error(400,"Please fill all the fields");}

    // check if user already exists

    const existedUser = await User.findOne({ email });


    if(existedUser){
        throw new api_error(409,"User already exists")};

    const user = await User.create({    
        name,
        email,
        password
    });

    const createduser =await User.findById(user._id).select("-password -refreshToken");

    if(!createduser){
    throw new api_error(500,"User creation failed");



}

res.status(201).json(new api_response(200,"User created successfully",createduser));

});


// logout controller

const login_Controller= asyncHandler(async (req,res)=>{
    const {email,password}= req.body;

    // check for all fields
    if(!email || !password){
    throw new api_error(400,"Please fill all the fields");} 
    const user = await User.findOne({email});   
    if(!user){
        throw new api_error(404,"User not found");
    }   
    
    const is_password_Valid = await user.comparePassword(password);

    if(!is_password_Valid){
        throw new api_error(401,"Invalid credentials (incorrect password)");
    }

    const {accessToken,refreshToken} = await generateAccessTokenAndRefreshToken(user._id);

    const loggedIn_User = await User.findById(user._id).select("-password -refreshToken");
    
     const options = {
        httpOnly: true,
        secure: false // Set to true in production if using HTTPS
        // sameSite: 'None' // Consider adding this for cross-site cookie handling if needed
    };


     // Send cookies and JSON response
    return res.status(200)
        .cookie("accessToken", accessToken, options)
        .cookie("refreshToken", refreshToken, options)
        .json(
            new api_response(
                200,
                {
                    user: loggedIn_User, // Use the plain JavaScript object directly
                    accessToken,
                    refreshToken
                },
                "User logged in successfully!!"
            )
        );
});

const logOutUser=asyncHandler(async(req, res )=>{
    await User.findByIdAndUpdate(
        req.user._id,
        {
            $unset: {
                refreshToken: 1 // this removes the field from document
            }
        },
        {
            new: true
        }
    )

    const options = {
        httpOnly: true,
        secure: false
    }

    return res
    .status(200)
    .clearCookie("accessToken", options)
    .clearCookie("refreshToken", options)
    .json(new api_response(200, {}, "User logged Out"))




});


const refreshAccessToken= asyncHandler( async (req , res)=>{
    try {
        const incomming_RefreshToken=req.cookies.refreshToken|| req.body.refreshToken
    
        if (!incomming_RefreshToken) {
            throw new api_error(401,"unauthorised request ")
            
        }
    
        const decoded_Token= jwt.verify(incomming_RefreshToken,process.env.REFRESH_TOKEN_SECRET)
    
        const user_id= decoded_Token.id
    
        const user = await User.findById(user_id)
    
        if(!user){
            throw new api_error(401,"Invalid refreshToken")
        }
    
        const user_refreshToken=user.refreshToken
    
        if (incomming_RefreshToken !== user_refreshToken) {
    
            throw new api_error(401,"Token Expired or used");
            
            
        }

        const options = {
            httpOnly: true,
            secure: false
        }
    
        const {accessToken, newRefreshToken} = await generateAccessAndRefereshTokens(user._id)
    
        return res
        .status(200)
        .cookie("accessToken", accessToken, options)
        .cookie("refreshToken", newRefreshToken, options)
        .json(
            new api_response(
                200, 
                {accessToken, refreshToken: newRefreshToken},
                "Access token refreshed"
            )
        )
    
    } catch (error) {

        throw new api_error(401, error?.message || "Invalid refresh token")
        
    }



});


export {register_controller, login_Controller , logOutUser  , refreshAccessToken};