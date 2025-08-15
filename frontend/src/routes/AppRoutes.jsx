import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from '../features/auth/Login';
import Register from '../features/auth/Register';
import ProjectList from '../features/projects/ProjectList';
import ProjectDetail from '../features/projects/ProjectDetail';
import ProjectForm from '../features/projects/ProjectForm'
import TasktForm from '../features/tasks/TaskForm'
import { useAuth } from '../features/auth/authContext';
import Loader from '../components/Loader'

export default function AppRoutes() {
  const { token, loading } = useAuth();

  if (loading) {
   
    return <Loader />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={!token ? <Login /> : <Navigate to="/projects" />}
        />
        <Route
          path="/register"
          element={!token ? <Register /> : <Navigate to="/projects" />}
        />

         {/* Projects */}        
        <Route
          path="/projects"
          element={token ? <ProjectList /> : <Navigate to="/login" />}
        />
         <Route
          path="/projects/new"
           element={token ? <ProjectForm/> : <Navigate to="/login" />}
        />
        
        <Route
          path="/projects/:id"
          element={token ? <ProjectDetail /> : <Navigate to="/login" />}
        />
       
         <Route
          path="/projects/edit"
           element={token ? <ProjectForm /> : <Navigate to="/login" />}  />
        
          {/* Tasks */}
          <Route
            path="/tasks/new"
            element={token ? <TasktForm /> : <Navigate to="/login" />} 
          />
          <Route
            path="/tasks/edit"
            element={token ? <TasktForm /> : <Navigate to="/login" />} 
          />
        <Route
          path="*"
          element={<Navigate to={"/login"} />}
        /> 
      </Routes>
    </BrowserRouter>
 );
}