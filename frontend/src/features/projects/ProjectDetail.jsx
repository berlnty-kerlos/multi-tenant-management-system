import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import ConfirmModal from "../../components/ConfirmModal";
import TaskList from "../tasks/TaskList";
import { apiFetchWithRefresh } from "../../lib/api";

export default function ProjectDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchProject() {
      try {
        const data = await apiFetchWithRefresh(`/projects/${id}`);
        setProject(data);
      } catch (err) {
        setError(err.message || "Failed to fetch project");
      }
    }
    fetchProject();
  }, [id]);

  useEffect(() => {
    async function fetchTasks() {
      try {
        const data = await apiFetchWithRefresh(`/projects/${id}/tasks`);
        setTasks(data);
      } catch (err) {
        setError(err.message || "Failed to fetch tasks");
      }
    }
    fetchTasks();
  }, [id]);

  const handleDelete = async () => {
    try {
      await apiFetchWithRefresh(`/projects/${id}`, { method: "DELETE" });
      setConfirmDelete(false);
      navigate("/projects", { replace: true });
    } catch (err) {
      setError(err.message || "Failed to delete project");
    }
  };

  const handleEdit = () => {
    navigate("/projects/edit", { state: { project } });
  };

  if (!project) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
        Loading project...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 px-4 py-8 flex justify-center">
      <div className="w-full max-w-4xl bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-700">
        {error && (
          <div className="bg-red-500 text-white p-3 rounded mb-4">{error}</div>
        )}

        <h1 className="text-3xl font-bold text-purple-300">{project.name}</h1>

        {project.description && (
          <p className="mt-3 text-gray-300">{project.description}</p>
        )}

        <p className="text-gray-400 mt-1 text-sm">
          Created: {new Date(project.created_at).toLocaleDateString()}
        </p>

        <div className="flex gap-4 mt-6">
          <button
            onClick={handleEdit}
            className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg transition"
          >
            Edit
          </button>
          <button
            onClick={() => setConfirmDelete(true)}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
          >
            Delete
          </button>
        </div>

        {confirmDelete && (
          <ConfirmModal
            title="Confirm Delete"
            message="Are you sure you want to delete this project?"
            onConfirm={handleDelete}
            onCancel={() => setConfirmDelete(false)}
          />
        )}

        <div className="mt-10">
          <h2 className="text-xl font-semibold text-purple-300 mb-4">Tasks</h2>
          <TaskList
            tasks={tasks}
            projectId={id}
            refreshTasks={async () => {
              const updated = await apiFetchWithRefresh(`/projects/${id}/tasks`);
              setTasks(updated);
            }}
          />
        </div>
      </div>
    </div>
  );
}
