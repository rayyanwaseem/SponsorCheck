export default function ProviderSettings({
  provider, setProvider,
  llmBaseUrl, setLlmBaseUrl,
  llmApiKey, setLlmApiKey,
  llmModel, setLlmModel
}: any) {
  return (
    <div className="space-y-4 text-sm">
      <div>
        <label className="block text-slate-700 font-medium mb-1">Provider</label>
        <select 
          value={provider} 
          onChange={(e) => setProvider(e.target.value)}
          className="w-full border-slate-300 rounded-md shadow-sm p-2 bg-white text-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        >
          <option value="rule_based">Rule Based (Fast, No AI)</option>
          <option value="openai_compatible">OpenAI Compatible (Ollama/LM Studio)</option>
        </select>
      </div>

      {provider === 'openai_compatible' && (
        <div className="space-y-3 pt-3 border-t border-slate-100">
          <div>
            <label className="block text-slate-700 mb-1">Base URL</label>
            <input 
              type="text" 
              value={llmBaseUrl} 
              onChange={(e) => setLlmBaseUrl(e.target.value)}
              className="w-full border-slate-300 rounded-md shadow-sm p-2 text-slate-700" 
            />
          </div>
          <div>
            <label className="block text-slate-700 mb-1">Model Name</label>
            <input 
              type="text" 
              value={llmModel} 
              onChange={(e) => setLlmModel(e.target.value)}
              className="w-full border-slate-300 rounded-md shadow-sm p-2 text-slate-700" 
            />
          </div>
          <div>
            <label className="block text-slate-700 mb-1">API Key</label>
            <input 
              type="password" 
              value={llmApiKey} 
              onChange={(e) => setLlmApiKey(e.target.value)}
              className="w-full border-slate-300 rounded-md shadow-sm p-2 text-slate-700" 
            />
          </div>
        </div>
      )}
    </div>
  );
}
