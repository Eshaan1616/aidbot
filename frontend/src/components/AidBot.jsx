import React, { useState, useRef, useEffect } from "react";
import {
  Upload,
  Send,
  FileText,
  Activity,
  MessageSquare,
  LayoutDashboard,
} from "lucide-react";

import Documents from "./Documents";
import Status from "./Status";
import Landing from "./Landing";
import SystemOverview from "./SystemOverview";
import AnswerCard from "./AnswerCard";

export default function AidBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // 🔹 Single source of truth for backend state
  const [documents, setDocuments] = useState({
    loaded: false,
    total_documents: 0,
    total_chunks: 0,
    sources: [],
  });

  // 🔹 Default to Overview (important)
  const [activeView, setActiveView] = useState("overview");

  const fileInputRef = useRef(null);

  const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const API_URL = `${BASE_URL}/api`;

  // ---------- LOAD DOCUMENT STATUS ----------
  useEffect(() => {
    fetch(`${API_URL}/documents`)
      .then((res) => res.json())
      .then((data) =>
        setDocuments({
          loaded: true,
          total_documents: data.total_documents ?? 0,
          total_chunks: data.total_chunks ?? 0,
          sources: data.sources ?? [],
        })
      )
      .catch(() =>
        setDocuments((d) => ({
          ...d,
          loaded: true,
        }))
      );
  }, []);

  // ---------- UPLOAD ----------
  const upload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const fd = new FormData();
    fd.append("file", file);

    fetch(`${API_URL}/upload`, {
      method: "POST",
      body: fd,
    }).then(() => {
      fetch(`${API_URL}/documents`)
        .then((res) => res.json())
        .then((data) =>
          setDocuments({
            loaded: true,
            total_documents: data.total_documents ?? 0,
            total_chunks: data.total_chunks ?? 0,
            sources: data.sources ?? [],
          })
        );
    });
  };

  // ---------- CHAT ----------
  const ask = async () => {
    if (!input.trim()) return;

    const q = input;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: q }]);

    const res = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: q,
        conversation_history: [],
      }),
    });

    const data = await res.json();
    setMessages((m) => [...m, { role: "assistant", ...data }]);
  };

  return (
    <div className="flex h-screen bg-slate-900 text-white">
      {/* ---------- SIDEBAR ---------- */}
      <div className="w-64 border-r border-slate-700 p-4 space-y-2">
        <h1 className="text-xl font-bold mb-2">AidBot</h1>

        <button onClick={() => setActiveView("overview")} className="flex gap-2">
          <LayoutDashboard size={16} /> Overview
        </button>

        <button onClick={() => setActiveView("chat")} className="flex gap-2">
          <MessageSquare size={16} /> Chat
        </button>

        <button onClick={() => setActiveView("documents")} className="flex gap-2">
          <FileText size={16} /> Documents
        </button>

        <button onClick={() => setActiveView("status")} className="flex gap-2">
          <Activity size={16} /> Status
        </button>

        <button
          onClick={() => fileInputRef.current.click()}
          className="mt-6 bg-indigo-600 py-2 rounded"
        >
          <Upload size={16} className="inline mr-1" />
          Upload
        </button>

        <input type="file" ref={fileInputRef} hidden onChange={upload} />
      </div>

      {/* ---------- MAIN ---------- */}
      <div className="flex-1 flex flex-col">
        {activeView === "overview" && (
          <>
            <Landing onUpload={() => fileInputRef.current.click()} />
            {documents.loaded && documents.total_documents > 0 && (
              <SystemOverview documents={documents} />
            )}
          </>
        )}

        {activeView === "documents" && <Documents apiUrl={API_URL} />}
        {activeView === "status" && <Status baseUrl={BASE_URL} />}

        {activeView === "chat" && (
          <>
            <div className="flex-1 p-6 space-y-4 overflow-y-auto">
              {messages.length === 0 && (
                <div className="text-slate-400 text-center">
                  Ask a question grounded in uploaded documentation.
                </div>
              )}

              {messages.map((m, i) =>
                m.role === "assistant" ? (
                  <AnswerCard key={i} {...m} />
                ) : (
                  <div key={i} className="text-right">
                    {m.content}
                  </div>
                )
              )}
            </div>

            <div className="border-t border-slate-700 p-4 flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && ask()}
                className="flex-1 bg-slate-800 p-2 rounded"
                placeholder="Ask a grounded question…"
                disabled={!documents.loaded || documents.total_documents === 0}
              />
              <button
                onClick={ask}
                className="bg-indigo-600 px-4 rounded"
                disabled={!documents.loaded || documents.total_documents === 0}
              >
                <Send size={16} />
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
