import { useEffect, useState } from 'react'
import axios from 'axios'
import { FiCalendar } from 'react-icons/fi'

function Knockout() {
    const [partidos, setPartidos] = useState([])

    useEffect(() => {
        axios.get('http://localhost:8000/api/knockout/predictions')
            .then(res => setPartidos(res.data))
            .catch(err => console.error(err))
    }, [])

    return (
        <div className="p-6">
            <div className="flex items-center gap-3 mb-6">
                <span className="text-4xl">🏆</span>
                <h1 className="text-3xl font-bold text-gray-800">Fase Final - Camino a la Gloria</h1>
            </div>
            <p className="mb-6 text-gray-600">ARES ha calculado los cruces y predice a los ganadores de cada eliminatoria.</p>

            <div className="space-y-8">
                {['Octavos', 'Cuartos', 'Semis', 'Final', 'Tercer Lugar'].map(ronda => (
                    <div key={ronda}>
                        <h2 className="text-2xl font-bold mb-4 text-center text-gray-700 border-b pb-2">{ronda} de Final</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                            {partidos.filter(p => p.ronda === ronda).map(p => (
                                <div key={p.id} className="bg-white rounded-xl shadow-lg overflow-hidden border-t-4 border-yellow-500">
                                    <div className="p-4 text-center">
                                        <div className="flex justify-between items-center font-bold">
                                            <span className="text-lg">{p.local}</span>
                                            <span className="text-gray-500 text-sm">VS</span>
                                            <span className="text-lg">{p.visitante}</span>
                                        </div>
                                        <div className="mt-3 flex justify-between text-xs font-mono">
                                            <span className="text-blue-600">{p.prob_local}%</span>
                                            <span className="text-gray-500">|</span>
                                            <span className="text-red-600">{p.prob_visitante}%</span>
                                        </div>
                                        <div className="mt-2 text-sm font-semibold text-green-700 bg-green-50 rounded-full py-1 px-2 inline-block">
                                            🏆 ARES predice: {p.ganador_predicho}
                                        </div>
                                        <div className="mt-2 text-xs text-gray-400 flex items-center justify-center gap-1">
                                            <FiCalendar /> {p.fecha || 'Fecha por confirmar'}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Knockout