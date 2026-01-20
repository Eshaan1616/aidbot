import { Database, FileText, Activity } from "lucide-react";

export default function SystemOverview({ documents }) {
  return (
    <div className="bg-slate-800 border-b border-slate-700 px-6 py-3 flex gap-8 text-sm">
      
      <Metric
        icon={<FileText size={16} />}
        label="Documents"
        value={documents.total_documents}
      />

      <Metric
        icon={<Database size={16} />}
        label="Chunks Indexed"
        value={documents.total_chunks}
      />

      <Metric
        icon={<Activity size={16} />}
        label="Retrieval Mode"
        value="Grounded"
      />
    </div>
  );
}

function Metric({ icon, label, value }) {
  return (
    <div className="flex items-center gap-2 text-slate-300">
      <span className="text-indigo-400">{icon}</span>
      <span className="font-medium">{label}:</span>
      <span className="text-white">{value}</span>
    </div>
  );
}
