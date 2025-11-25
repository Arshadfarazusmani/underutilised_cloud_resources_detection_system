import mongoose from "mongoose";

const resourceSchema = new mongoose.Schema(
  {
    user: { 
      type: mongoose.Schema.Types.ObjectId, 
      ref: "User",
      required: true
    },

    resource_id: { 
      type: String, 
      required: true 
    },

    resource_type: { 
      type: String, 
      required: true 
    },

    cpu_utilization: { 
      type: Number, 
      required: true 
    },

    memory_utilization: { 
      type: Number, 
      required: true 
    },

    disk_io: { 
      type: Number, 
      required: true 
    },

    network_io: { 
      type: Number, 
      required: true 
    },

    last_access_days_ago: { 
      type: Number, 
      required: true 
    },

    provisioned_cpu_cores: { 
      type: Number, 
      required: true 
    },

    provisioned_capacity_gb: { 
      type: Number, 
      required: true 
    }
  },
  { timestamps: true }
);

export default mongoose.model("Resource", resourceSchema);
