import { useEffect, useState } from 'react'
import axios from 'axios'
import { FiActivity, FiUsers, FiDollarSign, FiTv } from 'react-icons/fi'

function Home() {
    const [stats, setStats] = useState({ partidos: 0, jugadores: 0, ofertas: 0 })
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        Promise.all([
            axios.get('http://localhost:8000/api/partidos_ares'),
            axios.get('http://localhost:8000/api/jugadores'),
            axios.get('http://localhost:8000/api/ofertas')
        ]).then(([p, j, o]) => {
            setStats({
                partidos: p.data?.length || 0,
                jugadores: j.data?.length || 0,
                ofertas: o.data?.length || 0
            })
            setLoading(false)
        }).catch(err => {
            console.error('Error:', err)
            setLoading(false)
        })
    }, [])

    if (loading) return <div className="p-6 text-center">Cargando Dashboard...</div>

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6 text-gray-800">📊 Dashboard ARES</h1>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-blue-100 p-6 rounded-xl shadow">
                    <div className="flex items-center gap-3">
                        <FiTv className="text-blue-600 text-2xl" />
                        <h3 className="text-lg font-semibold">Partidos Analizados</h3>
                    </div>
                    <p className="text-4xl font-bold mt-2">{stats.partidos}</p>
                </div>
                <div className="bg-green-100 p-6 rounded-xl shadow">
                    <div className="flex items-center gap-3">
                        <FiUsers className="text-green-600 text-2xl" />
                        <h3 className="text-lg font-semibold">Jugadores en Base</h3>
                    </div>
                    <p className="text-4xl font-bold mt-2">{stats.jugadores}</p>
                </div>
                <div className="bg-yellow-100 p-6 rounded-xl shadow">
                    <div className="flex items-center gap-3">
                        <FiDollarSign className="text-yellow-600 text-2xl" />
                        <h3 className="text-lg font-semibold">Ofertas Simuladas</h3>
                    </div>
                    <p className="text-4xl font-bold mt-2">{stats.ofertas}</p>
                </div>
            </div>
        </div>
    )
}

export default Home