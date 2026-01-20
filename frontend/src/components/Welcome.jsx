import React from "react";
import { Upload, Brain, FileText, ShieldCheck } from "lucide-react";

export default function Welcome({ onUpload }) {
  return (
    <div className="h-full flex items-center justify-center">
      <div className="max-w-xl bg-slate-800 border border-slate-700 rounded-xl p-8 space-y-6">
        <h1 className="text-2xl font-bold text-white">
          Grounded AI Support System
        </h1>

        <p className="text-slate-300">
          AidBot is a Retrieval-Augmented Generation (RAG) system that answers
          questions strictly from uploaded documentation.
        </p>

        <div className="space-y-3 text-sm text-slate-300">
          <div className="flex gap-2">
            <FileText size={16} /> Upload documentation (.txt / .md)
          </div>
          <div className="flex gap-2">
            <Brain size={16} /> Documents are chunked & indexed
          </div>
          <div className="flex gap-2">
            <ShieldCheck size={16} /> Answers are grounded with confidence scoring
          </div>
        </div>

        <button
          onClick={onUpload}
          className="mt-4 w-full bg-indigo-600 hover:bg-indigo-500 py-2 rounded"
        >
          <Upload size={16} className="inline mr-2" />
          Upload your first document
        </button>
      </div>
    </div>
  );
}
