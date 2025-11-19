import dotenv from "dotenv";
dotenv.config({
    path:".env"
})

import mongoose from "mongoose"
import { db_name } from "../constant.js"

const db_uri = process.env.MONGO_URI


const connectDB= async function(){  // function definition 
   try{
    const connectionInstance= await mongoose.connect(`${db_uri}${db_name}`)
    console.log("Database connected successfully to", connectionInstance.connection.name)
   }catch(error){
    
    
    console.log("DB connection Error !!!",error)
    process.exit(1);

   }
};

export{connectDB}