import { useEffect, useState } from 'react'
import axios from 'axios'

function Ofertas() {
    const [ofertas, setOfertas] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get('http://localhost:8000/api/ofertas')
            .then(res => {
                setOfertas(res.data)
                setLoading(false)
            })
            .catch(err => {
                console.error('Error:', err)
                setLoading(false)
            })
    }, [])

    if (loading) return <div className="p-6 text-center">Cargando ofertas...</div>

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6 text-gray-800">💰 Ofertas de Fichaje - Mercado de Transferencias</h1>
            <div className="bg-white rounded-xl shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Jugador</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Origen</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Destino</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto (€)</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {ofertas.map((o, idx) => (
                            <tr key={idx} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap font-medium">{o.jugador}</td>
                                <td className="px-6 py-4 whitespace-nowrap">{o.origen}</td>
                                <td className="px-6 py-4 whitespace-nowrap">{o.destino}</td>
                                <td className="px-6 py-4 whitespace-nowrap">€{o.monto?.toLocaleString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default Ofertas