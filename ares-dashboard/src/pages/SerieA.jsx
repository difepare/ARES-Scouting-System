import { useEffect, useState } from 'react'
import axios from 'axios'

function SerieA() {
    const [partidos, setPartidos] = useState([])

    useEffect(() => {
        axios.get('http://localhost:8000/api/ligas/seriea')
            .then(res => setPartidos(res.data))
            .catch(err => console.error(err))
    }, [])

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6">🇮🇹 Serie A - Predicciones ARES</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {partidos.map(p => (
                    <div key={p.id} className="bg-white rounded-xl shadow-md p-4 border-l-4 border-blue-600">
                        <div className="flex justify-between text-sm text-gray-500 mb-2">
                            <span>{p.fecha?.slice(0, 10)}</span>
                            <span>{p.estado}</span>
                        </div>
                        <div className="flex justify-between font-bold text-center">
                            <div className="w-2/5 text-right">{p.local}</div>
                            <div className="w-1/5 text-gray-500">VS</div>
                            <div className="w-2/5 text-left">{p.visitante}</div>
                        </div>
                        <div className="mt-3 bg-gray-50 rounded p-2 text-center text-sm">
                            <span className="text-blue-600">{p.prob_local}%</span> | 
                            <span className="text-gray-500"> Empate {p.prob_empate}%</span> | 
                            <span className="text-red-600">{p.prob_visitante}%</span>
                            <div className="text-xs text-gray-400 mt-1">xG: {p.xG_local} - {p.xG_visitante}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
export default SerieA