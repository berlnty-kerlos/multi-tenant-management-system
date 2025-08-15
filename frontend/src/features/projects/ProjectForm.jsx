import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { apiFetchWithRefresh } from "../../lib/api";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";

export default function ProjectForm() {
  const navigate = useNavigate();
  const location = useLocation();

  const project = location.state?.project || null;
  const editMode = !!project;

  const [name, setName] = useState(editMode ? project.name : "");
  const [description, setDescription] = useState(editMode ? project.description : "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (editMode) {
      setName(project.name);
      setDescription(project.description || "");
    }
  }, [project, editMode]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (editMode) {
        await apiFetchWithRefresh(`/projects/${project.id}`, {
          method: "PUT",
          body: { name, description },
        });
      } else {
        await apiFetchWithRefresh("/projects", {
          method: "POST",
          body: { name, description },
        });
      }
      navigate("/projects");
    } catch (err) {
      setError(err.message || "Failed to save project");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-lg bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-700"
      >
        <h2 className="text-3xl font-bold text-purple-300 mb-6 text-center">
          {editMode ? "Edit Project" : "New Project"}
        </h2>

        {error && <ErrorMessage message={error} />}

        <label className="block mb-2 font-medium text-gray-300">Project Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full bg-gray-900 text-white border border-gray-600 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />

        <label className="block mb-2 font-medium text-gray-300">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={6}
          className="w-full bg-gray-900 text-white border border-gray-600 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full mt-6 bg-purple-500 text-white py-2 px-4 rounded-lg hover:bg-purple-600 transition disabled:opacity-50"
        >
          {loading ? <Loader /> : editMode ? "Update Project" : "Create Project"}
        </button>
      </form>
    </div>
  );
}
