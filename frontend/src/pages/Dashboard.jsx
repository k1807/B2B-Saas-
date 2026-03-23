import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { products, sales, predictions } from '../api/client'

export default function Dashboard() {
  const [productCount, setProductCount] = useState(0)
  const [recentSales, setRecentSales] = useState([])
  const [demandData, setDemandData] = useState(null)

  useEffect(() => {
    products.list().then((p) => setProductCount(p.length))
    sales.list('?limit=5').then(setRecentSales).catch(() => setRecentSales([]))
  }, [])

  useEffect(() => {
    predictions.demand()
      .then(setDemandData)
      .catch(() => setDemandData(null))
  }, [])

  const totalRevenue = recentSales.reduce((s, x) => s + (x.total_amount || 0), 0)

  const chartData = demandData?.predictions?.map((p) => ({
    date: p.date.slice(5),
    demand: p.predicted_demand,
    fullDate: p.date,
  })) || []

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
          <h2 className="text-slate-600 font-medium mb-1">Products</h2>
          <p className="text-3xl font-bold text-slate-800">{productCount}</p>
          <Link to="/products" className="mt-2 inline-block text-blue-600 text-sm font-medium hover:underline">
            Manage products →
          </Link>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
          <h2 className="text-slate-600 font-medium mb-1">Recent sales (last 5)</h2>
          <p className="text-3xl font-bold text-slate-800">${totalRevenue.toFixed(2)}</p>
          <Link to="/sales" className="mt-2 inline-block text-blue-600 text-sm font-medium hover:underline">
            View all sales →
          </Link>
        </div>
      </div>

      {/* Demand Prediction Section */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800">Demand Prediction</h2>
          <p className="text-sm text-slate-500 mt-0.5">AI-powered forecast for the next 7 days</p>
        </div>
        <div className="p-6">
          {demandData?.message && (
            <div className={`mb-4 p-4 rounded-lg ${
              demandData.trend === 'increasing' ? 'bg-emerald-50 border border-emerald-200' :
              demandData.trend === 'decreasing' ? 'bg-amber-50 border border-amber-200' :
              'bg-slate-50 border border-slate-200'
            }`}>
              <p className={`font-medium ${
                demandData.trend === 'increasing' ? 'text-emerald-800' :
                demandData.trend === 'decreasing' ? 'text-amber-800' :
                'text-slate-700'
              }`}>
                {demandData.message}
              </p>
            </div>
          )}
          {chartData.length > 0 ? (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="date" tick={{ fontSize: 12 }} stroke="#64748b" />
                  <YAxis tick={{ fontSize: 12 }} stroke="#64748b" />
                  <Tooltip
                    formatter={(v) => [Number(v).toFixed(1), 'Predicted demand']}
                    contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="demand"
                    stroke="#2563eb"
                    strokeWidth={2}
                    dot={{ fill: '#2563eb', r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="py-12 text-center text-slate-500">
              <p>Not enough sales data yet.</p>
              <p className="text-sm mt-1">Record sales to see demand predictions.</p>
              <Link to="/sales" className="mt-3 inline-block text-blue-600 text-sm font-medium hover:underline">
                Record a sale →
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Recent Sales Table */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <h2 className="px-6 py-4 font-semibold text-slate-800 border-b border-slate-200">Recent sales</h2>
        {recentSales.length === 0 ? (
          <p className="p-6 text-slate-500">No sales yet. Record a sale from the Sales page.</p>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="bg-slate-50 text-left text-sm text-slate-600">
                <th className="px-6 py-3">Product ID</th>
                <th className="px-6 py-3">Qty</th>
                <th className="px-6 py-3">Amount</th>
                <th className="px-6 py-3">Date</th>
              </tr>
            </thead>
            <tbody>
              {recentSales.map((s) => (
                <tr key={s.id} className="border-t border-slate-100">
                  <td className="px-6 py-4">{s.product_id}</td>
                  <td className="px-6 py-4">{s.quantity_sold}</td>
                  <td className="px-6 py-4">${s.total_amount.toFixed(2)}</td>
                  <td className="px-6 py-4">{s.sale_date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
