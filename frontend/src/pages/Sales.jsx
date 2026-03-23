import { useState, useEffect } from 'react'
import { products as productsApi, sales as salesApi } from '../api/client'

export default function Sales() {
  const [productItems, setProductItems] = useState([])
  const [salesList, setSalesList] = useState([])
  const [loading, setLoading] = useState(true)
  const [showRecord, setShowRecord] = useState(false)
  const [form, setForm] = useState({ product_id: '', quantity_sold: 1, sale_date: new Date().toISOString().slice(0, 10) })
  const [error, setError] = useState('')

  function load() {
    setLoading(true)
    Promise.all([productsApi.list(), salesApi.list()])
      .then(([p, s]) => {
        setProductItems(p)
        setSalesList(s)
      })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  async function handleRecord(e) {
    e.preventDefault()
    setError('')
    if (!form.product_id) {
      setError('Select a product')
      return
    }
    try {
      await salesApi.create({
        product_id: +form.product_id,
        quantity_sold: +form.quantity_sold,
        sale_date: form.sale_date,
      })
      setShowRecord(false)
      setForm({ product_id: '', quantity_sold: 1, sale_date: new Date().toISOString().slice(0, 10) })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Sales</h1>
        <button
          onClick={() => { setShowRecord(true); setError(''); setForm({ product_id: productItems[0]?.id || '', quantity_sold: 1, sale_date: new Date().toISOString().slice(0, 10) }) }}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Record sale
        </button>
      </div>

      {showRecord && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
            <h2 className="text-xl font-bold mb-4">Record sale</h2>
            {error && <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>}
            <form onSubmit={handleRecord} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Product</label>
                <select
                  value={form.product_id}
                  onChange={(e) => setForm({ ...form, product_id: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg"
                  required
                >
                  <option value="">Select product</option>
                  {productItems.map((p) => (
                    <option key={p.id} value={p.id}>{p.name} (SKU: {p.sku}, Stock: {p.quantity})</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Quantity</label>
                <input
                  type="number"
                  min="1"
                  value={form.quantity_sold}
                  onChange={(e) => setForm({ ...form, quantity_sold: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Date</label>
                <input
                  type="date"
                  value={form.sale_date}
                  onChange={(e) => setForm({ ...form, sale_date: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg"
                />
              </div>
              <div className="flex gap-3 pt-2">
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  Record
                </button>
                <button type="button" onClick={() => setShowRecord(false)} className="px-4 py-2 border rounded-lg hover:bg-slate-50">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {loading ? (
        <p className="text-slate-500">Loading...</p>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          {salesList.length === 0 ? (
            <p className="p-8 text-slate-500 text-center">No sales yet. Record your first sale.</p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="bg-slate-50 text-left text-sm text-slate-600">
                  <th className="px-6 py-3">ID</th>
                  <th className="px-6 py-3">Product ID</th>
                  <th className="px-6 py-3">Quantity</th>
                  <th className="px-6 py-3">Amount</th>
                  <th className="px-6 py-3">Date</th>
                </tr>
              </thead>
              <tbody>
                {salesList.map((s) => (
                  <tr key={s.id} className="border-t border-slate-100">
                    <td className="px-6 py-4">{s.id}</td>
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
      )}
    </div>
  )
}
