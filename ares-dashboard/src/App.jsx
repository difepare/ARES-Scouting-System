import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { FiActivity, FiUsers, FiDollarSign, FiTv, FiGlobe, FiStar } from 'react-icons/fi'

// Importar componentes
import Home from './pages/Home'
import Partidos from './pages/Partidos'
import Jugadores from './pages/Jugadores'
import Ofertas from './pages/Ofertas'
import Talentos from './pages/Talentos'
import Mundial from './pages/Mundial'
import Knockout from './pages/Knockout'
import Bundesliga from './pages/Bundesliga'
import Champions from './pages/Champions'
import SerieA from './pages/SerieA'
import Ligue1 from './pages/Ligue1'
import PerfilTalento from './pages/PerfilTalento'

function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar fijo */}
        <div className="w-64 bg-gradient-to-b from-gray-900 to-gray-800 text-white flex flex-col">
          <div className="p-4 text-xl font-bold border-b border-gray-700">⚽ ARES</div>
          <nav className="flex-1 mt-4">
            <Link to="/" className="flex items-center gap-3 p-3 hover:bg-gray-800"><FiActivity /> Dashboard</Link>
            <Link to="/partidos" className="flex items-center gap-3 p-3 hover:bg-gray-800"><FiTv /> Partidos</Link>
            <Link to="/jugadores" className="flex items-center gap-3 p-3 hover:bg-gray-800"><FiUsers /> Jugadores</Link>
            <Link to="/ofertas" className="flex items-center gap-3 p-3 hover:bg-gray-800"><FiDollarSign /> Ofertas</Link>
            <Link to="/talentos" className="flex items-center gap-3 p-3 hover:bg-gray-800"><FiStar /> Talento Joven</Link>
            <Link to="/mundial" className="flex items-center gap-3 p-3 hover:bg-gray-800"><FiGlobe /> Mundial 2026</Link>
            <Link to="/knockout" className="flex items-center gap-3 p-3 hover:bg-gray-800"><span className="text-xl">🏆</span> Fase Final</Link>
            <Link to="/bundesliga" className="flex items-center gap-3 p-3 hover:bg-gray-800"><span className="text-xl">🇩🇪</span> Bundesliga</Link>
            <Link to="/champions" className="flex items-center gap-3 p-3 hover:bg-gray-800"><span className="text-xl">🏆</span> Champions</Link>
            <Link to="/seriea" className="flex items-center gap-3 p-3 hover:bg-gray-800"><span className="text-xl">🇮🇹</span> Serie A</Link>
            <Link to="/ligue1" className="flex items-center gap-3 p-3 hover:bg-gray-800"><span className="text-xl">🇫🇷</span> Ligue 1</Link>
          </nav>
        </div>

        {/* Contenido principal */}
        <div className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/partidos" element={<Partidos />} />
            <Route path="/jugadores" element={<Jugadores />} />
            <Route path="/ofertas" element={<Ofertas />} />
            <Route path="/talentos" element={<Talentos />} />
            <Route path="/talento/:id" element={<PerfilTalento />} />
            <Route path="/mundial" element={<Mundial />} />
            <Route path="/knockout" element={<Knockout />} />
            <Route path="/bundesliga" element={<Bundesliga />} />
            <Route path="/champions" element={<Champions />} />
            <Route path="/seriea" element={<SerieA />} />
            <Route path="/ligue1" element={<Ligue1 />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App