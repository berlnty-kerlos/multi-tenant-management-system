import Button from "./Button";

export default function ConfirmModal({ title, message, onConfirm, onCancel }) {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50 backdrop-blur-sm">
      <div className="bg-gray-800 p-6 rounded-xl shadow-lg w-96 border border-gray-700">
        <h2 className="text-2xl font-bold text-purple-300 mb-4">{title}</h2>
        <p className="text-gray-300">{message}</p>
        <div className="mt-6 flex justify-end gap-4">
          <button
            onClick={onCancel}
            className="bg-gray-600 hover:bg-gray-500 text-white px-4 py-2 rounded-lg transition"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
