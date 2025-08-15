import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetchWithRefresh } from "../../lib/api";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import Button from "../../components/Button";

export default function ProjectList() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true);
      setError(null);

      try {
        const res = await apiFetchWithRefresh("/projects", { method: "GET" });
        setProjects(res);
      } catch (err) {
        setError(err.message || "Failed to fetch projects");
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 px-6 py-10">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
        <h1 className="text-3xl font-bold text-purple-300">Projects</h1>
        <button
          onClick={() => navigate("/projects/new")}
          className="mt-4 md:mt-0 bg-purple-500 text-white px-5 py-2 rounded-lg hover:bg-purple-600 transition"
        >
          Add New Project
        </button>
      </div>

      {loading && <Loader />}
      {error && <ErrorMessage message={error} />}

      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.length === 0 && (
            <p className="text-gray-400">No projects found.</p>
          )}

          {projects.map((project) => (
            <div
              key={project.id}
              className="bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-purple-400/40 hover:scale-[1.02] transition cursor-pointer"
              onClick={() => navigate(`/projects/${project.id}`)}
            >
              <h2 className="text-xl font-semibold text-white">
                {project.name}
              </h2>

              {project.description && (
                <>
                  <p className="text-gray-400 text-sm font-medium mt-3">
                    Description:
                  </p>
                  <p className="text-gray-300">{project.description}</p>
                </>
              )}

              <p className="text-gray-400 text-sm font-medium mt-3">
                Created at:
              </p>
              <p className="text-gray-500 text-sm">
                {new Date(project.created_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
