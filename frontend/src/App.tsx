import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { ProtectedRoute } from './components/ProtectedRoute'
import { AuthProvider } from './contexts/AuthContext'
import { Cadastro } from './pages/Cadastro'
import { EditorCurriculo } from './pages/EditorCurriculo'
import { Login } from './pages/Login'
import { MeusCurriculos } from './pages/MeusCurriculos'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <MeusCurriculos />
              </ProtectedRoute>
            }
          />
          <Route
            path="/novo"
            element={
              <ProtectedRoute>
                <EditorCurriculo />
              </ProtectedRoute>
            }
          />
          <Route
            path="/editar/:id"
            element={
              <ProtectedRoute>
                <EditorCurriculo />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
