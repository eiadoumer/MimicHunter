type Props = {
  files: File[];
  onFilesSelected: (files: File[]) => void;
  disabled?: boolean;
};

export default function FileUploader({ files, onFilesSelected, disabled }: Props) {
  return (
    <section className="card">
      <h2 className="section-title">Upload Documents</h2>
      <p className="section-subtitle">Upload at least two UTF-8 .txt files.</p>
      <label className={`upload-zone ${disabled ? "upload-zone--disabled" : ""}`}>
        <input
          type="file"
          accept=".txt,text/plain"
          multiple
          disabled={disabled}
          onChange={(e) => onFilesSelected(Array.from(e.target.files || []))}
        />
        <span className="upload-zone__title">Choose files</span>
        <span className="upload-zone__hint">or drag and drop .txt files</span>
      </label>
      {files.length > 0 && (
        <ul className="file-list">
          {files.map((f) => (
            <li key={f.name} className="file-list__item">
              <span className="file-list__name">{f.name}</span>
              <span className="file-list__meta">{(f.size / 1024).toFixed(1)} KB</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
