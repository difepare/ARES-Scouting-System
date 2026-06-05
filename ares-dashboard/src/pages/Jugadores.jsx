import { useEffect, useState } from 'react'
import axios from 'axios'

function Jugadores() {
    const [jugadores, setJugadores] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get('http://localhost:8000/api/jugadores')
            .then(res => {
                setJugadores(res.data)
                setLoading(false)
            })
            .catch(err => {
                console.error('Error:', err)
                setLoading(false)
            })
    }, [])

    if (loading) return <div className="p-6 text-center">Cargando jugadores...</div>

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6 text-gray-800">👤 Jugadores - Top Goleadores</h1>
            <div className="bg-white rounded-xl shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Jugador</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Equipo</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Goles</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {jugadores.map((j, idx) => (
                            <tr key={idx} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap font-medium">{j.nombre}</td>
                                <td className="px-6 py-4 whitespace-nowrap">{j.equipo}</td>
                                <td className="px-6 py-4 whitespace-nowrap">{j.goles}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default Jugadores