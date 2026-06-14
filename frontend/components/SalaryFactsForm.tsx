export default function SalaryFactsForm({ facts, onChange }: { facts: any, onChange: (f: any) => void }) {
  
  const updateFact = (key: string, value: any) => {
    onChange({ ...facts, [key]: value });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
      <div>
        <label className="block text-slate-700 font-medium mb-1">Weekly Hours</label>
        <input 
          type="number" step="0.5" 
          value={facts.weekly_hours || ''} 
          onChange={(e) => updateFact('weekly_hours', e.target.value ? parseFloat(e.target.value) : undefined)}
          className="w-full border-slate-300 rounded-md shadow-sm p-2 text-slate-700" 
          placeholder="e.g. 37.5"
        />
      </div>
      <div>
        <label className="block text-slate-700 font-medium mb-1">Offered Salary (£)</label>
        <input 
          type="number" 
          value={facts.offered_salary || ''} 
          onChange={(e) => updateFact('offered_salary', e.target.value ? parseFloat(e.target.value) : undefined)}
          className="w-full border-slate-300 rounded-md shadow-sm p-2 text-slate-700" 
          placeholder="e.g. 45000"
        />
      </div>
      <div>
        <label className="block text-slate-700 font-medium mb-1">Applicant Age</label>
        <input 
          type="number" 
          value={facts.applicant_age || ''} 
          onChange={(e) => updateFact('applicant_age', e.target.value ? parseInt(e.target.value) : undefined)}
          className="w-full border-slate-300 rounded-md shadow-sm p-2 text-slate-700" 
        />
      </div>
      <div>
        <label className="block text-slate-700 font-medium mb-1">Work Region</label>
        <select 
          value={facts.work_region || ''} 
          onChange={(e) => updateFact('work_region', e.target.value || undefined)}
          className="w-full border-slate-300 rounded-md shadow-sm p-2 text-slate-700 bg-white"
        >
          <option value="">Unknown</option>
          <option value="England">England</option>
          <option value="Scotland">Scotland</option>
          <option value="Wales">Wales</option>
          <option value="Northern Ireland">Northern Ireland</option>
        </select>
      </div>
      
      <div className="md:col-span-2 space-y-2 pt-2 border-t border-slate-100 mt-2">
        <label className="flex items-center space-x-2 text-slate-700">
          <input type="checkbox" checked={!!facts.is_extension} onChange={(e) => updateFact('is_extension', e.target.checked)} className="rounded text-blue-600 focus:ring-blue-500"/>
          <span>Is Extension application</span>
        </label>
        <label className="flex items-center space-x-2 text-slate-700">
          <input type="checkbox" checked={!!facts.has_student_or_graduate_visa_history} onChange={(e) => updateFact('has_student_or_graduate_visa_history', e.target.checked)} className="rounded text-blue-600 focus:ring-blue-500"/>
          <span>Has Student or Graduate Visa history</span>
        </label>
        <label className="flex items-center space-x-2 text-slate-700">
          <input type="checkbox" checked={!!facts.has_relevant_phd} onChange={(e) => updateFact('has_relevant_phd', e.target.checked)} className="rounded text-blue-600 focus:ring-blue-500"/>
          <span>Has relevant PhD</span>
        </label>
        <label className="flex items-center space-x-2 text-slate-700">
          <input type="checkbox" checked={!!facts.is_health_and_care_route} onChange={(e) => updateFact('is_health_and_care_route', e.target.checked)} className="rounded text-blue-600 focus:ring-blue-500"/>
          <span>Applying under Health and Care Worker Visa</span>
        </label>
      </div>
    </div>
  );
}
