export default function AnswerCard({ answer, confidence, sources }) {
    return (
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-4 space-y-3">
        <p className="text-slate-100">{answer}</p>
  
        <div className="flex items-center justify-between text-xs">
          <span
            className={`px-2 py-1 rounded border ${
              confidence === "high"
                ? "border-green-700 text-green-400 bg-green-900/30"
                : "border-orange-700 text-orange-400 bg-orange-900/30"
            }`}
          >
            Confidence: {confidence}
          </span>
  
          {sources?.length > 0 && (
            <span className="text-slate-400">
              Sources: {sources.join(", ")}
            </span>
          )}
        </div>
      </div>
    );
  }
  