import { RouteResult } from '../lib/types';

function RouteCard({ route, isStandard }: { route: RouteResult, isStandard?: boolean }) {
  const isPassed = route.status === 'applicable';
  const needsInfo = route.status === 'needs_more_information' || route.status === 'source_check_required';
  const isBlocked = route.status === 'not_applicable' || route.status === 'salary_too_low';

  const badgeColor = isPassed ? 'bg-green-100 text-green-800 border-green-200' :
                     needsInfo ? 'bg-amber-100 text-amber-800 border-amber-200' :
                     'bg-red-100 text-red-800 border-red-200';

  return (
    <div className={`p-5 rounded-xl border ${isStandard ? 'border-blue-200 bg-blue-50/50' : 'border-slate-200 bg-white'} shadow-sm`}>
      <div className="flex justify-between items-start mb-3">
        <h4 className={`font-semibold ${isStandard ? 'text-blue-900' : 'text-slate-800'}`}>{route.route_label}</h4>
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${badgeColor}`}>
          {route.status.replace(/_/g, ' ').toUpperCase()}
        </span>
      </div>
      
      {route.required_salary && (
        <div className="mb-3">
          <span className="text-slate-500 text-sm">Required Salary: </span>
          <span className="font-bold text-slate-800">£{route.required_salary.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
        </div>
      )}

      {route.calculation_steps && route.calculation_steps.length > 0 && (
        <div className="text-xs text-slate-600 bg-slate-50 p-3 rounded mb-3 border border-slate-100">
          <ul className="list-disc pl-4 space-y-1">
            {route.calculation_steps.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}

      {route.missing_facts && route.missing_facts.length > 0 && (
        <div className="text-xs text-amber-700 mt-2 flex items-start">
          <span className="mr-1">⚠️</span>
          <span>Missing: {route.missing_facts.join(', ')}</span>
        </div>
      )}
      
      {route.blocking_reasons && route.blocking_reasons.length > 0 && (
        <div className="text-xs text-red-600 mt-2 flex items-start">
          <span className="mr-1">❌</span>
          <span>{route.blocking_reasons.join(' ')}</span>
        </div>
      )}
    </div>
  );
}

export default function SalaryRoutePanel({ evaluation }: { evaluation: any }) {
  if (!evaluation) return null;

  return (
    <div className="space-y-6">
      {evaluation.standard_route && (
        <div>
          <h3 className="text-lg font-bold text-slate-800 mb-3">Standard Route</h3>
          <RouteCard route={evaluation.standard_route} isStandard={true} />
        </div>
      )}

      {evaluation.possible_lower_routes?.length > 0 && (
        <div>
          <h3 className="text-lg font-bold text-slate-800 mb-3">Possible Lower Routes</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {evaluation.possible_lower_routes.map((r: any, i: number) => (
              <RouteCard key={i} route={r} />
            ))}
          </div>
        </div>
      )}

      {evaluation.routes_needing_more_information?.length > 0 && (
        <div>
          <h3 className="text-lg font-bold text-slate-800 mb-3">Routes Needing Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {evaluation.routes_needing_more_information.map((r: any, i: number) => (
              <RouteCard key={i} route={r} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
