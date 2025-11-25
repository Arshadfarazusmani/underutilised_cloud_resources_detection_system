import React, { useEffect, useState } from "react";
import API from "../services/api";

export default function Dashboard() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const load = async () => {
      const r = await API.get("/predict/history");
      setHistory(r.data);
    };
    load();
  }, []);

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Dashboard</h2>

      <table className="w-full border">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-2">Resource</th>
            <th className="p-2">Status</th>
            <th className="p-2">Timestamp</th>
          </tr>
        </thead>

        <tbody>
          {history.map((row) => (
            <tr key={row._id} className="border-t">
              <td className="p-2">{row.resource_snapshot.resource_id}</td>
              <td className="p-2">{row.status}</td>
              <td className="p-2">{new Date(row.createdAt).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
