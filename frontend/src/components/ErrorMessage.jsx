export default function ErrorMessage({ message }) {
  return (
    <div className="bg-red-900 text-red-200 p-3 rounded-lg border border-red-700 shadow-sm">
      {message}
    </div>
  );
}
