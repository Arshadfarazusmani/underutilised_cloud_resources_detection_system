import dotenv from "dotenv";
dotenv.config({
    path:".env"
})
import axios from "axios";

import { app } from "./app.js";
import { connectDB } from "./db/db.js";


const PORT= process.env.PORT
const FASTAPI_URL = "http://127.0.0.1:8000/predict";



connectDB().then(()=>{


    app.post("/api/predict", async (req, res) => {
  try {
    const response = await axios.post(FASTAPI_URL, req.body);
    res.json(response.data);
  } catch (error) {
    console.error("Error:", error.response?.data || error.message);
    res.status(500).json({ error: "Prediction failed" });
  }
});

app.listen(5000, () => {
  console.log("Node server running on http://localhost:5000");
});
}).catch((error)=>{
    console.log("Database connection error !!!",error)

})