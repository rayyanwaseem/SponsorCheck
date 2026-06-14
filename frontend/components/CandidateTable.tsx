import { SocCandidate } from '../lib/types';

export default function CandidateTable({ candidates }: { candidates: SocCandidate[] }) {
  if (!candidates || candidates.length === 0) return null;

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 mt-6">
      <table className="w-full text-sm text-left text-slate-600">
        <thead className="bg-slate-50 text-slate-700 uppercase text-xs">
          <tr>
            <th className="px-4 py-3 font-semibold">Code</th>
            <th className="px-4 py-3 font-semibold">Job Type</th>
            <th className="px-4 py-3 font-semibold text-right">Score</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200 bg-white">
          {candidates.slice(0, 5).map((c, i) => (
            <tr key={i} className="hover:bg-slate-50 transition-colors">
              <td className="px-4 py-3 font-medium text-slate-900">{c.occupation_code}</td>
              <td className="px-4 py-3">{c.job_type}</td>
              <td className="px-4 py-3 text-right">{(c.score * 100).toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
