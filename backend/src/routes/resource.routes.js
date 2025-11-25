import express from "express";
import Resource from "../models/resource.model.js";
import { auth } from "../middlware/auth.js";

const router = express.Router();

router.post("/", auth, async (req, res) => {
  try {
    const payload = { ...req.body, user: req.user.id };
    const resource = await Resource.create(payload);
    res.json(resource);
  } catch (err) { res.status(500).json({ error: err.message }); }
});

router.get("/", auth, async (req, res) => {
  try {
    const resources = await Resource.find({ user: req.user.id }).sort({ createdAt:-1 });
    res.json(resources);
  } catch (err) { res.status(500).json({ error: err.message }); }
});

export default router;
