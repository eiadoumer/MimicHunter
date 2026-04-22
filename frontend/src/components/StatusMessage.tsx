type Props = {
  error?: string | null;
  loading?: boolean;
};

export default function StatusMessage({ error, loading }: Props) {
  if (loading) return null;
  if (error) return <div className="alert">{error}</div>;
  return null;
}
