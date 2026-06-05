import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'

function PerfilTalento() {
    const { id } = useParams()
    const [jugador, setJugador] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get(`http://localhost:8000/api/talento/${id}`)
            .then(res => {
                setJugador(res.data)
                setLoading(false)
            })
            .catch(err => {
                console.error('Error:', err)
                setLoading(false)
            })
    }, [id])

    if (loading) return <div className="p-6 text-center">Cargando perfil del talento...</div>
    if (!jugador) return <div className="p-6 text-center">Jugador no encontrado</div>

    // Determinar nivel de recomendación
    let nivelColor = "text-yellow-600"
    let nivelTexto = "Promesa a seguir"
    if (jugador.indice_actual >= 7) {
        nivelColor = "text-green-600"
        nivelTexto = "CRACK MUNDIAL - Fichaje inmediato"
    } else if (jugador.indice_actual >= 5) {
        nivelColor = "text-blue-600"
        nivelTexto = "PROMESA DE ÉLITE - Seguimiento prioritario"
    }

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <Link to="/talentos" className="text-blue-600 hover:underline mb-4 inline-block">← Volver al ranking</Link>

            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
                {/* Cabecera con gradiente */}
                <div className="bg-gradient-to-r from-yellow-500 to-yellow-600 p-6 text-white">
                    <h1 className="text-3xl font-bold">{jugador.nombre}</h1>
                    <p className="mt-1">{jugador.posicion} | {jugador.equipo} | {jugador.edad} años | {jugador.nacionalidad}</p>
                </div>

                {/* Cuerpo del perfil */}
                <div className="p-6">
                    {/* Métricas principales */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <div className="bg-gray-50 p-4 rounded-xl text-center">
                            <p className="text-gray-500 text-sm">Índice ARES</p>
                            <p className="text-4xl font-bold text-blue-600">{jugador.indice_actual}</p>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-xl text-center">
                            <p className="text-gray-500 text-sm">Productividad (G/A por partido)</p>
                            <p className="text-4xl font-bold text-green-600">{jugador.productividad_actual}</p>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-xl text-center">
                            <p className="text-gray-500 text-sm">Proyección ARES</p>
                            <p className="text-4xl font-bold text-purple-600">{jugador.proyeccion}</p>
                        </div>
                    </div>

                    {/* Recomendación */}
                    <div className={`p-4 rounded-xl mb-6 text-center ${nivelColor} bg-opacity-10 bg-yellow-100`}>
                        <p className="font-bold text-lg">{nivelTexto}</p>
                        <p className="text-sm">Basado en su rendimiento actual y evolución reciente</p>
                    </div>

                    {/* Tabla de evolución */}
                    <h2 className="text-xl font-bold mb-3">📊 Evolución por temporada</h2>
                    <div className="overflow-x-auto">
                        <table className="min-w-full bg-white border rounded-xl">
                            <thead className="bg-gray-100">
                                <tr>
                                    <th className="p-2 text-left">Temporada</th>
                                    <th className="p-2 text-left">Partidos</th>
                                    <th className="p-2 text-left">Goles</th>
                                    <th className="p-2 text-left">Asistencias</th>
                                    <th className="p-2 text-left">G/A</th>
                                    <th className="p-2 text-left">Índice</th>
                                </tr>
                            </thead>
                            <tbody>
                                {jugador.evolucion.map((e, idx) => (
                                    <tr key={idx} className="border-t">
                                        <td className="p-2 font-medium">{e.temporada}</td>
                                        <td className="p-2">{e.partidos}</td>
                                        <td className="p-2">{e.goles}</td>
                                        <td className="p-2">{e.asistencias}</td>
                                        <td className="p-2">{e.productividad}</td>
                                        <td className="p-2 font-bold text-blue-600">{e.indice}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Comparativa y nota final */}
                    <div className="mt-6 p-4 bg-gray-50 rounded-xl text-sm text-gray-600">
                        <p className="font-semibold">🔍 Nota del sistema:</p>
                        <p>ARES ha analizado su progresión en las últimas temporadas. Su índice de talento ha sido calculado considerando goles, asistencias, minutos jugados y regularidad.</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PerfilTalento