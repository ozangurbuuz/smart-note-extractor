import { useState } from "react";
import FileUploadForm from "./components/FileUploadForm";
import ResultPanel from "./components/ResultPanel";
import { summarizeFile } from "./services/api";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async ({ file, summaryType, summaryLength }) => {
    setLoading(true);
    setError("");

    try {
      const response = await summarizeFile({ file, summaryType, summaryLength });
      setResult(response);
    } catch (apiError) {
      setResult(null);
      setError(apiError.message || "Something went wrong while summarizing the file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-5xl px-4 py-10">
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-lg">
        <h1 className="text-3xl font-bold tracking-tight">Smart Note Extractor</h1>
        <p className="mt-2 text-slate-600">
          Upload a PDF or TXT file to generate extractive summary, notes, and keywords.
        </p>

        <div className="mt-6">
          <FileUploadForm onSubmit={handleSubmit} loading={loading} />
        </div>

        {error ? <p className="mt-4 rounded bg-red-50 p-3 text-red-700">{error}</p> : null}
      </section>

      <section className="mt-8">
        <ResultPanel result={result} loading={loading} />
      </section>
    </main>
  );
}

export default App;
