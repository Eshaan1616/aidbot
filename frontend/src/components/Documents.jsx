import React, { useEffect, useState } from "react";
import { FileText } from "lucide-react";

export default function Documents({ apiUrl }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${apiUrl}/documents`)
      .then(res => res.json())
      .then(setData)
      .catch(() => {});
  }, []);

  if (!data) return <p className="p-6">Loading documents…</p>;

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-xl font-bold flex gap-2">
        <FileText /> Documents
      </h2>

      <p>Total documents: {data.total_documents}</p>
      <p>Total chunks: {data.total_chunks}</p>

      <ul className="list-disc list-inside text-slate-300">
        {data.sources.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </div>
  );
}
