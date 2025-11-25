import dotenv from "dotenv";
dotenv.config({
    path:".env"
})

import { app } from "./app.js";
import { DB_connect} from "./db/db.js";


const PORT= process.env.PORT


DB_connect().then(()=>{
    app.listen(PORT,()=>{
        console.log("server is running on ",PORT)
    })

}).catch((error)=>{
    console.log("Database connection error !!!",error)

})