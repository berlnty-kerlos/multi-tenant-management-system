import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../../components/Button";
import ConfirmModal from "../../components/ConfirmModal";
import { apiFetchWithRefresh } from "../../lib/api";

export default function TaskItem({ task, refreshTasks }) {
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleDelete = async () => {
    try {
      await apiFetchWithRefresh(`/tasks/${task.id}`, { method: "DELETE" });
      setConfirmDelete(false);
      refreshTasks();
    } catch (err) {
      setError(err.message || "Failed to delete task");
    }
  };

  const handleEdit = () => {
    navigate("/tasks/new", { state: { task } });
  };

  return (
    <div
      className="bg-gray-900 p-5 rounded-lg shadow-md hover:shadow-lg 
                 transition-all duration-200 border-l-4 border-[#958AC1] flex justify-between items-start gap-4"
    >
      {/* Left content */}
      <div className="flex-1">
        <h4 className="font-bold text-white text-lg">{task.title}</h4>
        {task.description && (
          <p className="text-gray-300 mt-1">{task.description}</p>
        )}
        <p className="mt-2 text-sm">
          <span className="text-gray-400">Status:</span>{" "}
          <span
            className={`font-semibold px-2 py-0.5 rounded ${
              task.status === "completed"
                ? "bg-[#A6D609]/20 text-[#A6D609]"
                : task.status === "in progress"
                ? "bg-[#958AC1]/20 text-[#958AC1]"
                : "bg-gray-700 text-gray-300"
            }`}
          >
            {task.status}
          </span>
        </p>
      </div>

      {/* Buttons */}
      <div className="flex gap-2 shrink-0">
        <Button
          onClick={handleEdit}
          className="bg-[#958AC1] text-white hover:brightness-110"
        >
          Edit
        </Button>
        <Button
          onClick={() => setConfirmDelete(true)}
          className="bg-red-500 text-white hover:brightness-110"
        >
          Delete
        </Button>
      </div>

      {/* Confirm Delete Modal */}
      {confirmDelete && (
        <ConfirmModal
          title="Confirm Delete"
          message={`Are you sure you want to delete task "${task.title}"?`}
          onConfirm={handleDelete}
          onCancel={() => setConfirmDelete(false)}
        />
      )}

      {error && <p className="text-red-400 mt-2">{error}</p>}
    </div>
  );
}
