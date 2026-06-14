import { ClassificationResponse } from '../lib/types';

export default function SocDecisionCard({ decision }: { decision: ClassificationResponse['decision'] }) {
  return (
    <div className="bg-gradient-to-br from-blue-900 to-indigo-900 text-white p-8 rounded-2xl shadow-lg mb-6">
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-3xl font-bold mb-1 tracking-tight text-white" style={{ color: 'white' }}>SOC {decision.best_occupation_code}</h2>
          <p className="text-blue-100 text-lg font-medium">Likely Match</p>
        </div>
        <div className="bg-white/20 backdrop-blur-md px-4 py-2 rounded-full border border-white/30 text-sm font-semibold text-white">
          Confidence: {(decision.confidence * 100).toFixed(0)}%
        </div>
      </div>
      <div className="mt-6">
        <h3 className="text-sm uppercase tracking-wider text-blue-200 font-semibold mb-2">Reasoning</h3>
        <p className="text-blue-50 leading-relaxed">{decision.reasoning}</p>
      </div>
      <div className="mt-4 text-xs text-blue-200 opacity-80 flex items-center">
        <span>Method: {decision.classification_method}</span>
      </div>
    </div>
  );
}
