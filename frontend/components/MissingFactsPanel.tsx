export default function MissingFactsPanel({ questions }: { questions: string[] }) {
  if (!questions || questions.length === 0) return null;

  return (
    <div className="bg-amber-50 border-l-4 border-amber-400 p-5 rounded-r-lg mt-6 shadow-sm">
      <div className="flex">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-amber-400" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-bold text-amber-800">Missing Information</h3>
          <div className="mt-2 text-sm text-amber-700">
            <p className="mb-2">We need more facts to evaluate some lower salary routes:</p>
            <ul className="list-disc pl-5 space-y-1">
              {questions.map((q, i) => <li key={i}>{q}</li>)}
            </ul>
          </div>
          <div className="mt-4 text-xs text-amber-800 opacity-80">
            Some salary routes depend on facts that cannot be confirmed from the job description alone, such as visa history, Certificate of Sponsorship date, applicant age, PhD status, UK region, national pay scale, or whether a healthcare, education or shortage route applies. Please check the latest GOV.UK Skilled Worker guidance.
          </div>
        </div>
      </div>
    </div>
  );
}
