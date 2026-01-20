import { Upload, Database, Brain, ShieldCheck } from "lucide-react";

export default function Landing({ onUpload }) {
  return (
    <div className="flex-1 flex items-center justify-center px-6">
      <div className="max-w-5xl w-full grid grid-cols-1 md:grid-cols-2 gap-10">
        
        {/* LEFT */}
        <div className="space-y-6">
          <h1 className="text-4xl font-bold leading-tight">
            Grounded AI Support System
          </h1>

          <p className="text-slate-300 text-lg">
            A production-style Retrieval-Augmented Generation (RAG) system that
            answers questions strictly from your documentation — no hallucinations.
          </p>

          <div className="space-y-4 text-sm">
            <Step icon={<Upload />} text="Upload internal documentation" />
            <Step icon={<Database />} text="Chunking & vector indexing" />
            <Step icon={<Brain />} text="Semantic retrieval + LLM reasoning" />
            <Step icon={<ShieldCheck />} text="Grounded answers with confidence & sources" />
          </div>

          <button
            onClick={onUpload}
            className="mt-4 inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 transition px-6 py-3 rounded-lg font-medium"
          >
            <Upload size={18} />
            Upload Documentation
          </button>
        </div>

        {/* RIGHT */}
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
          <h3 className="font-semibold mb-4">What this project demonstrates</h3>
          <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
            <li>Document ingestion & preprocessing</li>
            <li>Vector search over embedded chunks</li>
            <li>Context-limited LLM responses</li>
            <li>Confidence scoring & escalation logic</li>
            <li>Backend-driven UI state</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

function Step({ icon, text }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-indigo-400">{icon}</span>
      <span>{text}</span>
    </div>
  );
}
