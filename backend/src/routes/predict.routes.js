import express from "express";
import axios from "axios";
import Prediction from "../models/prediction.model.js";
import Resource from "../models/resource.model.js";
import { auth } from "../middlware/auth.js";
import dotenv from "dotenv";

dotenv.config();
const router = express.Router();
const FASTAPI = process.env.FASTAPI_URL || "http://127.0.0.1:8000/predict";

// Call FastAPI and save result
router.post("/", auth, async (req, res) => {
  try {
    // 1) Optionally save resource snapshot
    const resourcePayload = { ...req.body, user: req.user.id };
    const resource = await Resource.create(resourcePayload);

    // 2) Call FastAPI
    const r = await axios.post(FASTAPI, req.body);
    const { prediction, status } = r.data;

    // 3) Save prediction
    const predDoc = await Prediction.create({
      user: req.user.id,
      resource: resource._id,
      resource_snapshot: req.body,
      prediction,
      status
    });

    res.json({ prediction, status, predictionId: predDoc._id });
  } catch (err) {
    console.error("predict error:", err.response?.data || err.message);
    res.status(500).json({ error: err.response?.data || err.message });
  }
});

// Get history
router.get("/history", auth, async (req, res) => {
  try {
    const history = await Prediction.find({ user: req.user.id })
      .populate("resource")
      .sort({ createdAt: -1 });
    res.json(history);
  } catch (err) { res.status(500).json({ error: err.message }); }
});

export default router;
