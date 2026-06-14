import { ClassificationResponse } from '../lib/types';
import SocDecisionCard from './SocDecisionCard';
import CandidateTable from './CandidateTable';
import SalaryRoutePanel from './SalaryRoutePanel';
import MissingFactsPanel from './MissingFactsPanel';
import EvidencePanel from './EvidencePanel';
import ReportDownloadButton from './ReportDownloadButton';
import Disclaimer from './Disclaimer';

export default function ResultsView({ 
  result, 
  onReset 
}: { 
  result: ClassificationResponse, 
  onReset: () => void 
}) {
  return (
    <div className="max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Analysis Results</h2>
        <button 
          onClick={onReset}
          className="px-4 py-2 text-sm font-medium text-slate-600 bg-white border border-slate-300 rounded-md hover:bg-slate-50 transition-colors"
        >
          Start New Check
        </button>
      </div>

      <SocDecisionCard decision={result.decision} />
      
      {result.decision.warning_flags?.length > 0 && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
          <strong>Warnings:</strong>
          <ul className="list-disc pl-5 mt-1">
            {result.decision.warning_flags.map((w, i) => <li key={i}>{w}</li>)}
          </ul>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h3 className="text-xl font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">Salary Evaluation</h3>
          <SalaryRoutePanel evaluation={result.salary_evaluation} />
          <MissingFactsPanel questions={result.salary_evaluation?.missing_questions || []} />
        </div>
        
        <div>
          <h3 className="text-xl font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">SOC Details</h3>
          <CandidateTable candidates={result.candidates} />
          <EvidencePanel evidence={result.decision.evidence_from_jd} />
        </div>
      </div>

      <ReportDownloadButton reportId={result.report_id} />
      
      <div className="mt-12 max-w-3xl mx-auto">
        <Disclaimer />
      </div>
    </div>
  );
}
