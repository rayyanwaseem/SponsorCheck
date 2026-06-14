export default function EvidencePanel({ evidence }: { evidence: string[] }) {
  if (!evidence || evidence.length === 0) return null;

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm mt-6">
      <h3 className="text-lg font-bold text-slate-800 mb-4">Evidence from Job Description</h3>
      <ul className="space-y-2">
        {evidence.map((item, i) => (
          <li key={i} className="flex items-start text-sm text-slate-700">
            <span className="text-blue-500 mr-2">•</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
