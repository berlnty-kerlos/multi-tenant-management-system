import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../../components/Button";
import TaskItem from "./TaskItem";
import { apiFetchWithRefresh } from "../../lib/api";

export default function TaskList({ projectId }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const res = await apiFetchWithRefresh(`/projects/${projectId}/tasks`);
      setTasks(res);
    } catch (err) {
      setError(err.message || "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [projectId]);

  const handleAddTask = () => {
    navigate("/tasks/new", { state: { projectId } });
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold text-gray-800">Tasks</h2>
        <Button
          onClick={handleAddTask}
          className="bg-green-500 text-white shadow hover:scale-[1.02]"
        >
          + Add Task
        </Button>
      </div>

      {/* Status */}
      {loading && <p className="text-gray-500">Loading tasks...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {/* Task Items */}
      {!loading && !error && (
        <div >
          {tasks.length > 0 ? (
            tasks.map((task) => (
              <div
                key={task.id}
                className="p-2 rounded-lg shadow-sm hover:shadow-md transition"
              >
                <TaskItem task={task} refreshTasks={fetchTasks} />
              </div>
            ))
          ) : (
            <p className="text-gray-500 italic">
              No tasks yet. Click "Add Task" to create one.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
