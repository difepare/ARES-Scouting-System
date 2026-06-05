import { useEffect, useState } from 'react'
import axios from 'axios'
import { FiGlobe, FiBarChart2 } from 'react-icons/fi'

function Mundial() {
    const [partidos, setPartidos] = useState([])
    const [loading, setLoading] = useState(true)
    const [grupos, setGrupos] = useState({})

    useEffect(() => {
        axios.get('http://localhost:8000/api/worldcup/predictions')
            .then(res => { 
                setPartidos(res.data)
                
                // Agrupar por grupo
                const grouped = {}
                res.data.forEach(p => {
                    if (!grouped[p.grupo]) grouped[p.grupo] = []
                    grouped[p.grupo].push(p)
                })
                setGrupos(grouped)
                setLoading(false)
            })
            .catch(err => { 
                console.error(err)
                setLoading(false)
            })
    }, [])

    if (loading) return <div className="p-6 text-center">Cargando el futuro del Mundial...</div>

    return (
        <div className="p-6">
            <div className="flex items-center gap-3 mb-6">
                <FiGlobe className="text-4xl text-green-600" />
                <h1 className="text-3xl font-bold text-gray-800">🌍 Mundial USA 2026 - Predicciones ARES</h1>
            </div>
            <p className="mb-6 text-gray-600">Basado en Ranking FIFA y análisis de rendimiento. ¡Prepárate para la locura del fútbol!</p>

            {/* Mostrar partidos por grupo */}
            {Object.keys(grupos).map(grupo => (
                <div key={grupo} className="mb-10">
                    <h2 className="text-2xl font-bold mb-4 text-blue-700 border-l-4 border-blue-600 pl-3">
                        {grupo}
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {grupos[grupo].map(p => (
                            <div key={p.id} className="bg-white rounded-xl shadow-md overflow-hidden border-l-4 border-green-500 hover:shadow-lg transition">
                                <div className="p-4">
                                    <div className="flex justify-between items-center mb-3">
                                        <span className="text-sm font-semibold text-gray-500">Partido #{p.id}</span>
                                        <span className="flex items-center gap-1 text-xs bg-gray-100 px-2 py-1 rounded-full">
                                            <FiBarChart2 /> Análisis ARES
                                        </span>
                                    </div>
                                    <div className="flex justify-between items-center text-center font-bold">
                                        <div className="w-2/5 text-right">{p.local}</div>
                                        <div className="w-1/5 text-gray-500 text-sm">VS</div>
                                        <div className="w-2/5 text-left">{p.visitante}</div>
                                    </div>
                                    <div className="mt-3 bg-gray-50 rounded-lg p-2 text-center">
                                        <div className="flex justify-between text-xs font-mono">
                                            <span className="text-blue-600 font-bold">{p.prob_local}%</span>
                                            <span className="text-gray-500">Empate {p.prob_empate}%</span>
                                            <span className="text-red-600 font-bold">{p.prob_visitante}%</span>
                                        </div>
                                        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                                            <div className="bg-blue-600 h-2 rounded-l-full" style={{ width: `${p.prob_local}%` }}></div>
                                        </div>
                                        <p className="text-xs text-gray-500 mt-2 italic">{p.recomendacion}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    )
}

export default Mundial