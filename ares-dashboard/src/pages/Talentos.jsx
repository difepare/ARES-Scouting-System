import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

function Talentos() {
    const [talentos, setTalentos] = useState([])  // <-- Array vacío
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get('http://localhost:8000/api/talentos_v2')
            .then(res => {
                setTalentos(res.data)
                setLoading(false)
            })
            .catch(err => {
                console.error('Error:', err)
                setLoading(false)
            })
    }, [])

    if (loading) return <div className="p-6 text-center">Cargando talentos...</div>
    if (!talentos || talentos.length === 0) return <div className="p-6 text-center">No hay talentos disponibles.</div>

    return (
        <div className="p-6">
            <div className="flex items-center gap-3 mb-6">
                <span className="text-4xl">🌟</span>
                <h1 className="text-3xl font-bold text-gray-800">ARES Talento Joven - El Futuro del Fútbol</h1>
            </div>
            <p className="mb-6 text-gray-600">Detección temprana de promesas basada en datos reales. Valores combinados de Transfermarkt y estimación ARES.</p>

            <div className="space-y-4">
                {talentos.map((t) => {
                    let indiceColor = "text-blue-600"
                    if (t.indice_talento >= 7) indiceColor = "text-green-600"
                    else if (t.indice_talento >= 5) indiceColor = "text-blue-600"
                    else indiceColor = "text-gray-600"

                    return (
                        <Link to={`/talento/${t.id}`} key={t.id} className="block">
                            <div className="bg-white rounded-xl shadow-lg overflow-hidden border-l-8 border-yellow-500 card-hover transition-all duration-300 hover:shadow-xl">
                                <div className="p-4">
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <div className="flex items-center gap-2 mb-1">
                                                <h2 className="text-xl font-bold text-gray-800">{t.nombre}</h2>
                                                {t.plus_descripcion && (
                                                    <span className={`text-xs px-2 py-0.5 rounded-full ${t.plus_descripcion.includes('🇧🇷') ? 'bg-green-700' : 'bg-sky-700'} text-white`}>
                                                        {t.plus_descripcion}
                                                    </span>
                                                )}
                                            </div>
                                            <p className="text-gray-500 text-sm">{t.posicion} | {t.equipo} | {t.edad} años | {t.nacionalidad}</p>
                                            <div className="flex items-center gap-3 mt-1">
                                                <p className="text-sm font-semibold text-green-600">
                                                    💰 Valor {t.fuente_valor}: €{t.valor_mercado}M
                                                </p>
                                                {t.transfermarkt_url && t.fuente_valor === "Transfermarkt" && (
                                                    <a href={t.transfermarkt_url} target="_blank" rel="noopener noreferrer" 
                                                       className="text-xs text-blue-500 hover:underline">
                                                        Ver perfil ↗
                                                    </a>
                                                )}
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <span className={`text-2xl font-bold ${indiceColor}`}>{t.indice_talento}</span>
                                            <p className="text-xs text-gray-400">Índice ARES</p>
                                        </div>
                                    </div>

                                    <div className="mt-3 flex flex-wrap gap-2">
                                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">⚽ {t.estadisticas.goles} goles</span>
                                        <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">🅰️ {t.estadisticas.asistencias} asistencias</span>
                                        <span className="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">📊 {t.estadisticas.partidos} partidos</span>
                                        <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">⚡ G/A: {t.estadisticas.productividad}</span>
                                    </div>

                                    <div className="mt-3 p-2 bg-yellow-50 rounded">
                                        <p className="font-semibold text-yellow-800">{t.nivel}</p>
                                        <p className="text-sm text-gray-700">{t.recomendacion}</p>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    )
                })}
            </div>
        </div>
    )
}

export default Talentos