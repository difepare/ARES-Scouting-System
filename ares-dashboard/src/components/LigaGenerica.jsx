import { useEffect, useState } from 'react'
import axios from 'axios'

// Mapeo de colores fijos para cada liga
const coloresLiga = {
    brasileirao: "border-green-500",
    argentina: "border-sky-500",
    eredivisie: "border-orange-500",
    premier: "border-blue-500",
    laliga: "border-yellow-500",
    bundesliga: "border-red-500",
    champions: "border-purple-500",
    seriea: "border-indigo-500",
    ligue1: "border-pink-500"
}

function LigaGenerica({ titulo, endpoint, icono }) {
    const [partidos, setPartidos] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        axios.get(`http://localhost:8000/api/ligas/${endpoint}`)
            .then(res => {
                setPartidos(res.data)
                setLoading(false)
            })
            .catch(err => {
                console.error(`Error cargando ${titulo}:`, err)
                setError(err.message)
                setLoading(false)
            })
    }, [endpoint, titulo])

    if (loading) return <div className="p-6 text-center">Cargando {titulo}...</div>
    if (error) return <div className="p-6 text-center text-red-600">Error: {error}</div>
    if (partidos.length === 0) return <div className="p-6 text-center">No hay partidos disponibles para {titulo}.</div>

    const colorBorde = coloresLiga[endpoint] || "border-gray-500"

    return (
        <div className="p-6">
            <div className="flex items-center gap-3 mb-6">
                <span className="text-4xl">{icono}</span>
                <h1 className="text-3xl font-bold text-gray-800">{titulo} - Predicciones ARES</h1>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {partidos.map(p => (
                    <div key={p.id} className={`bg-white rounded-2xl shadow-lg overflow-hidden border-l-8 ${colorBorde} hover:shadow-xl transition-all duration-300`}>
                        <div className="p-4">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-semibold text-gray-500">{p.fecha?.slice(0, 10)}</span>
                                <span className="text-xs px-2 py-1 rounded-full bg-gray-100">{p.estado || 'Pendiente'}</span>
                            </div>
                            <div className="flex justify-between items-center text-center font-bold">
                                <div className="w-2/5 text-right">{p.local}</div>
                                <div className="w-1/5 text-gray-500 text-sm">VS</div>
                                <div className="w-2/5 text-left">{p.visitante}</div>
                            </div>
                            <div className="mt-3 bg-gray-50 rounded-lg p-2 text-center">
                                <div className="flex justify-between text-xs font-mono">
                                    <span className="text-blue-600">{p.prob_local || 33}%</span>
                                    <span className="text-gray-500">Empate {p.prob_empate || 33}%</span>
                                    <span className="text-red-600">{p.prob_visitante || 34}%</span>
                                </div>
                                <p className="text-xs text-gray-500 mt-1">xG: {p.xG_local || 1.2} - {p.xG_visitante || 1.2}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default LigaGenerica