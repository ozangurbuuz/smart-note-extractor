import { useState } from "react";

function FileUploadForm({ onSubmit, loading }) {
  const [file, setFile] = useState(null);
  const [summaryType, setSummaryType] = useState("balanced");
  const [summaryLength, setSummaryLength] = useState("medium");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!file) {
      return;
    }

    onSubmit({ file, summaryType, summaryLength });
  };

  return (
    <form className="grid gap-4" onSubmit={handleSubmit}>
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700" htmlFor="file-input">
          File Upload (PDF or TXT)
        </label>
        <input
          id="file-input"
          type="file"
          accept=".pdf,.txt"
          className="block w-full rounded-lg border border-slate-300 bg-slate-50 p-2 text-sm"
          onChange={(event) => setFile(event.target.files?.[0] || null)}
          disabled={loading}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700" htmlFor="summary-type">
            Summary Type
          </label>
          <select
            id="summary-type"
            className="w-full rounded-lg border border-slate-300 bg-white p-2 text-sm"
            value={summaryType}
            onChange={(event) => setSummaryType(event.target.value)}
            disabled={loading}
          >
            <option value="balanced">Balanced</option>
            <option value="keywords_first">Keywords First</option>
          </select>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700" htmlFor="summary-length">
            Summary Length
          </label>
          <select
            id="summary-length"
            className="w-full rounded-lg border border-slate-300 bg-white p-2 text-sm"
            value={summaryLength}
            onChange={(event) => setSummaryLength(event.target.value)}
            disabled={loading}
          >
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={loading || !file}
        className="rounded-lg bg-brand-accent px-4 py-2 font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Processing..." : "Generate Notes"}
      </button>
    </form>
  );
}

export default FileUploadForm;
