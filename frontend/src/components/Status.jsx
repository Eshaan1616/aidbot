import React, { useEffect, useState } from "react";
import { Activity, CheckCircle, AlertTriangle } from "lucide-react";

export default function Status({ baseUrl }) {
  const [ok, setOk] = useState(false);

  useEffect(() => {
    fetch(`${baseUrl}/health`)
      .then(res => setOk(res.ok))
      .catch(() => setOk(false));
  }, []);

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-xl font-bold flex gap-2">
        <Activity /> System Status
      </h2>

      <div className="flex items-center gap-2">
        {ok ? (
          <>
            <CheckCircle className="text-green-400" />
            Backend API healthy
          </>
        ) : (
          <>
            <AlertTriangle className="text-red-400" />
            Backend unreachable
          </>
        )}
      </div>

      <div className="text-sm text-slate-400 mt-4">
        <p>✔ Vector-based retrieval</p>
        <p>✔ Grounded generation</p>
        <p>✔ Confidence scoring</p>
        <p>✔ Escalation detection</p>
      </div>
    </div>
  );
}
