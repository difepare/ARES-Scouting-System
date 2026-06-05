import { useEffect, useState } from 'react'
import axios from 'axios'

function Bundesliga() {
    const [partidos, setPartidos] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        //axios.get('http://localhost:8000/api/bundesliga')
        axios.get('http://localhost:8000/api/ligas/bundesliga')
            .then(res => {
                console.log('Datos recibidos:', res.data)
                setPartidos(res.data)
                setLoading(false)
            })
            .catch(err => {
                console.error('Error:', err)
                setError(err.message)
                setLoading(false)
            })
    }, [])

    if (loading) return <div className="p-6 text-center">Cargando partidos de la Bundesliga...</div>
    if (error) return <div className="p-6 text-center text-red-600">Error: {error}</div>
    if (partidos.length === 0) return <div className="p-6 text-center">No hay partidos disponibles para la Bundesliga.</div>

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6 text-gray-800">🇩🇪 Bundesliga - Predicciones ARES</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {partidos.map(p => (
                    <div key={p.id} className="bg-white rounded-xl shadow-md overflow-hidden border-l-4 border-green-500">
                        <div className="p-4">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-semibold text-gray-500">{p.fecha?.slice(0, 10)}</span>
                                <span className={`text-xs px-2 py-1 rounded-full ${p.estado === 'Pendiente' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100'}`}>
                                    {p.estado}
                                </span>
                            </div>
                            <div className="flex justify-between items-center text-center font-bold">
                                <div className="w-2/5 text-right">{p.local}</div>
                                <div className="w-1/5 text-gray-500 text-sm">VS</div>
                                <div className="w-2/5 text-left">{p.visitante}</div>
                            </div>
                            <div className="mt-3 bg-gray-50 rounded-lg p-2 text-center">
                                <div className="flex justify-between text-xs font-mono">
                                    <span className="text-blue-600">{p.prob_local}%</span>
                                    <span className="text-gray-500">Empate {p.prob_empate}%</span>
                                    <span className="text-red-600">{p.prob_visitante}%</span>
                                </div>
                                <p className="text-xs text-gray-500 mt-1">xG: {p.xG_local} - {p.xG_visitante}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Bundesliga