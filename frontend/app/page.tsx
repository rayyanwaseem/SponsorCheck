'use client';

import { useState } from 'react';
import { classifyJobDescription } from '../lib/api';
import { ClassificationResponse, ApplicantFacts } from '../lib/types';
import ProviderSettings from '../components/ProviderSettings';
import SalaryFactsForm from '../components/SalaryFactsForm';
import JobDescriptionForm from '../components/JobDescriptionForm';
import Disclaimer from '../components/Disclaimer';
import ResultsView from '../components/ResultsView';

export default function Home() {
  const [jobDescription, setJobDescription] = useState('');
  const [provider, setProvider] = useState('rule_based');
  const [llmBaseUrl, setLlmBaseUrl] = useState('http://localhost:11434/v1');
  const [llmApiKey, setLlmApiKey] = useState('ollama');
  const [llmModel, setLlmModel] = useState('gemma4:e2b');
  const [facts, setFacts] = useState<ApplicantFacts>({});
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<ClassificationResponse | null>(null);

  const handleClassify = async () => {
    if (!jobDescription.trim()) {
      setError("Please provide a job description.");
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await classifyJobDescription(
        jobDescription,
        provider,
        llmBaseUrl,
        llmApiKey,
        llmModel,
        facts
      );
      setResult(response);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return <ResultsView result={result} onReset={() => setResult(null)} />;
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-xl font-semibold mb-4 text-slate-800">1. Job Description</h2>
          <JobDescriptionForm value={jobDescription} onChange={setJobDescription} />
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-xl font-semibold mb-4 text-slate-800">2. Applicant Salary Facts</h2>
          <SalaryFactsForm facts={facts} onChange={setFacts} />
        </div>
      </div>
      
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-xl font-semibold mb-4 text-slate-800">3. Classification Engine</h2>
          <ProviderSettings 
            provider={provider} setProvider={setProvider}
            llmBaseUrl={llmBaseUrl} setLlmBaseUrl={setLlmBaseUrl}
            llmApiKey={llmApiKey} setLlmApiKey={setLlmApiKey}
            llmModel={llmModel} setLlmModel={setLlmModel}
          />
        </div>
        
        <div className="bg-blue-50 p-6 rounded-xl border border-blue-100">
          <Disclaimer />
          <button
            onClick={handleClassify}
            disabled={loading}
            className="mt-6 w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg shadow-sm transition-colors disabled:opacity-70 flex justify-center items-center"
          >
            {loading ? (
              <><span className="animate-spin h-5 w-5 mr-3 border-2 border-white border-t-transparent rounded-full"></span> Analyzing...</>
            ) : "Analyze SOC Code & Salary"}
          </button>
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 text-sm">
              <strong>Error:</strong> {error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
