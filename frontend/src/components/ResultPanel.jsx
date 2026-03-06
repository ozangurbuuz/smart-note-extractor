function ResultPanel({ result, loading }) {
  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow">Processing your file...</div>
    );
  }

  if (!result) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow">
        Results will appear here after you submit a file.
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow">
      <h2 className="text-xl font-semibold">Summary</h2>
      <p className="mt-2 leading-relaxed text-slate-700">{result.summary}</p>

      <h3 className="mt-6 text-lg font-semibold">Bullet Notes</h3>
      <ul className="mt-2 list-disc space-y-1 pl-5 text-slate-700">
        {result.notes.map((note, index) => (
          <li key={`${note}-${index}`}>{note}</li>
        ))}
      </ul>

      <h3 className="mt-6 text-lg font-semibold">Keywords</h3>
      <div className="mt-2 flex flex-wrap gap-2">
        {result.keywords.map((keyword, index) => (
          <span
            key={`${keyword}-${index}`}
            className="rounded-full bg-brand-soft px-3 py-1 text-sm font-medium text-brand-deep"
          >
            {keyword}
          </span>
        ))}
      </div>
    </div>
  );
}

export default ResultPanel;
