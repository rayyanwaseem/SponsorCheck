export default function JobDescriptionForm({ value, onChange }: { value: string, onChange: (val: string) => void }) {
  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-600">
        Paste the job description below. Include duties, responsibilities, and requirements.
      </p>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={12}
        className="w-full border border-slate-300 rounded-lg shadow-sm p-3 font-mono text-sm text-slate-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        placeholder="e.g. We are looking for a Senior Software Engineer..."
      />
    </div>
  );
}
