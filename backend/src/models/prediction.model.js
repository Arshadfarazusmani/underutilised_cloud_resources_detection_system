import mongoose from "mongoose";

const predictionSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  resource: { type: mongoose.Schema.Types.ObjectId, ref: "Resource" },
  resource_snapshot: Object,
  prediction: Number,
  status: String
}, { timestamps: true });

export default mongoose.model("Prediction", predictionSchema);
