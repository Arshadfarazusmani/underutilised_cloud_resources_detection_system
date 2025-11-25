// import mongoose from "mongoose";
// import jwt from "jsonwebtoken"
// import bcrypt from "bcrypt" 


// const UserSchema = new mongoose.Schema({
//   name: { type: String, required: true },
//   email: { type: String, required: true, unique: true, index: true },
//   password: { type: String, required: true },
//   refreshToken:{
//         type : String
//     },
// }, { timestamps: true });

// UserSchema.pre("save", async function(next){
//             if(this.isModified("password")){
//                 this.password = await bcrypt.hash(this.password, 10);
//                 return next();
//             }
//             return next();

//            });


//     UserSchema.methods.comparePassword = async function(password){
//                return await bcrypt.compare(password, this.password);
//            };

//    // Generating Accesss Token 

// UserSchema.methods.generateAccessToken = function(){
//     return jwt.sign(
//         {
//             _id:this._id,
//             email:this.email,
//             username:this.username

//         },
//         process.env.ACCESS_TOKEN_SECRET,
//         {
//             "expiresIn":process.env.ACCESS_TOKEN_EXPIRY
//         }
//     )
// }
// // Generating Refresh  Token 

// UserSchema.methods.generateRefreshToken = function(){
//     return jwt.sign(
//         {
//             _id:this._id
//         },
//         process.env.REFRESH_TOKEN_SECRET,
//         {
//             "expiresIn":process.env.REFRESH_TOKEN_EXPIRY
//         }
//     )
// }


// export const User = mongoose.model("User", UserSchema);

// src/models/user.model.js
import mongoose from "mongoose";
import jwt from "jsonwebtoken";
import bcrypt from "bcrypt";

const UserSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true, index: true },
  password: { type: String, required: true },
  refreshToken: { type: String, default: null },
}, { timestamps: true });

// Async middleware — DO NOT accept `next` and DO NOT call next()
UserSchema.pre("save", async function () {
  // `this` is the document
  if (!this.isModified("password")) return;
  const saltRounds = 10;
  this.password = await bcrypt.hash(this.password, saltRounds);
});

UserSchema.methods.comparePassword = async function (password) {
  return bcrypt.compare(password, this.password);
};

// Generating Access Token
UserSchema.methods.generateAccessToken = function () {
  return jwt.sign(
    {
      _id: this._id,
      email: this.email,
      name: this.name
    },
    process.env.ACCESS_TOKEN_SECRET,
    {
      expiresIn: process.env.ACCESS_TOKEN_EXPIRY
    }
  );
};

// Generating Refresh Token
UserSchema.methods.generateRefreshToken = function () {
  return jwt.sign(
    { _id: this._id },
    process.env.REFRESH_TOKEN_SECRET,
    { expiresIn: process.env.REFRESH_TOKEN_EXPIRY }
  );
};

export const User = mongoose.model("User", UserSchema);
