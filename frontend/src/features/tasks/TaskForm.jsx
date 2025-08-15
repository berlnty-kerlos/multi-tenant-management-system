import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Button from "../../components/Button";
import ErrorMessage from "../../components/ErrorMessage";
import { apiFetchWithRefresh } from "../../lib/api";

export default function TaskForm() {
  const navigate = useNavigate();
  const location = useLocation();
  const task = location.state?.task;
  const projectId = location.state?.projectId; 

  const isEditMode = !!task;

  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [status, setStatus] = useState(task?.status || "todo");
  const [assigneeId, setAssigneeId] = useState(task?.assignee_id || "");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const body = { title, description };
      if (assigneeId && assigneeId.trim() !== "") {
        body.assignee_id = assigneeId;
      }
      if (isEditMode) {
        body.status = status;
        await apiFetchWithRefresh(`/tasks/${task.id}`, {
          method: "PUT",
          body: body,
        });
      } else {
        await apiFetchWithRefresh(`/projects/${projectId}/tasks`, {
          method: "POST",
          body: body,
        });
      }
      navigate(`/projects/${task?.project_id || projectId}`);
    } catch (err) {
      setError(err.message || "Failed to save task");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 px-4">
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-lg bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-700"
    >
      <h2 className="text-2xl font-bold text-purple-400 mb-6">
        {isEditMode ? "Edit Task" : "New Task"}
      </h2>

      {error && <div className="mb-4"><ErrorMessage message={error} /></div>}

      <div className="mb-4">
        <label className="block mb-1 font-medium text-gray-200">Title</label>
        <input
          className="w-full p-2 rounded-lg bg-gray-800 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-purple-400"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          required
        />
      </div>

      <div className="mb-4">
        <label className="block mb-1 font-medium text-gray-200">Description</label>
        <textarea
          className="w-full p-2 rounded-lg bg-gray-800 border border-gray-700 text-white h-32 focus:outline-none focus:ring-2 focus:ring-purple-400"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description"
        />
      </div>

      {isEditMode && (
        <div className="mb-4">
          <label className="block mb-1 font-medium text-gray-200">Status</label>
          <select
            className="w-full p-2 rounded-lg bg-gray-800 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-purple-400"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
        </div>
      )}

      <div className="mb-6">
        <label className="block mb-1 font-medium text-gray-200">Assignee ID</label>
        <input
          className="w-full p-2 rounded-lg bg-gray-800 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-purple-400"
          value={assigneeId}
          onChange={(e) => setAssigneeId(e.target.value)}
          placeholder="Enter assignee ID"
        />
      </div>

      <Button
        type="submit"
        className="bg-purple-600 hover:bg-purple-700 text-white w-full py-2"
      >
        {isEditMode ? "Update Task" : "Create Task"}
      </Button>
    </form>
    </div>
  );
}
