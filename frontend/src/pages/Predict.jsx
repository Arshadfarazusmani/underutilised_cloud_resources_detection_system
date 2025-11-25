import React, { useState } from "react";
import API from "../services/api";

export default function Predict() {
  const [form, setForm] = useState({
    resource_id: "",
    resource_type: "VM",
    cpu_utilization: "",
    memory_utilization: "",
    disk_io: "",
    network_io: "",
    last_access_days_ago: "",
    provisioned_cpu_cores: "",
    provisioned_capacity_gb: "",
  });

  const [result, setResult] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    const r = await API.post("/predict", form);
    setResult(r.data);
  };

  return (
    <div className="p-8 max-w-lg mx-auto">
      <h2 className="text-xl font-bold mb-4">Predict Resource Status</h2>

      <form onSubmit={submit}>
        {Object.keys(form).map((field) => (
          <input
            key={field}
            className="border p-2 w-full mb-3"
            placeholder={field}
            onChange={(e) =>
              setForm({ ...form, [field]: e.target.value })
            }
          />
        ))}

        <button className="bg-green-700 text-white px-4 py-2 w-full">
          Predict
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 bg-gray-100">
          <h3 className="font-bold">Prediction Result:</h3>
          <p>Status: {result.status}</p>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
