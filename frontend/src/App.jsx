import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { getCapitals, getHealth, updateCapital } from './services/api'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix default marker icon for Leaflet + Vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

function App() {
  const [capitals, setCapitals] = useState([])
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState(null)
  const [expanded, setExpanded] = useState({})
  const [search, setSearch] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [capitalsData, healthData] = await Promise.all([
          getCapitals(),
          getHealth()
        ])
        const sorted = capitalsData.sort((a, b) => a.name.localeCompare(b.name))
        setCapitals(sorted)
        setHealth(healthData)
      } catch (err) {
        setError('Failed to connect to API')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const toggleExpanded = (id) => {
    setExpanded(prev => ({ ...prev, [id]: !prev[id] }))
  }

  const toggleActive = async (e, city) => {
    e.stopPropagation()
    try {
      const updated = await updateCapital(city.id, { active: !city.active })
      setCapitals(prev =>
        prev.map(c => c.id === city.id ? { ...c, active: updated.active } : c)
      )
    } catch (err) {
      console.error('Failed to update city:', err)
    }
  }

  const filteredCapitals = capitals.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase())
  )

  if (loading) return (
    <div style={{display:'flex', alignItems:'center', justifyContent:'center', minHeight:'100vh', background:'#0a0e1a'}}>
      <p style={{color:'#00d4ff', fontFamily:'JetBrains Mono', fontSize:'1.2rem'}}>⟳ LOADING COMMAND CENTER...</p>
    </div>
  )

  if (error) return (
    <div style={{display:'flex', alignItems:'center', justifyContent:'center', minHeight:'100vh', background:'#0a0e1a'}}>
      <p style={{color:'#ff6b35', fontFamily:'JetBrains Mono'}}>⚠ {error}</p>
    </div>
  )

  return (
    <div style={{background:'#0a0e1a', minHeight:'100vh', padding:'2rem', fontFamily:'JetBrains Mono'}}>

      {/* HEADER */}
      <div style={{borderBottom:'2px solid #2e3f70', paddingBottom:'1rem', marginBottom:'2rem'}}>
        <h1 style={{color:'#00d4ff', fontSize:'2rem', fontFamily:'Rajdhani', letterSpacing:'4px', fontWeight:700}}>
          ◈ GPS/GIS CAPITAL CITIES — COMMAND CENTER
        </h1>
        <p style={{color:'#8899bb', fontSize:'0.8rem', marginTop:'0.3rem'}}>
          STATUS: {health?.status?.toUpperCase()} &nbsp;|&nbsp;
          DB: {health?.database} &nbsp;|&nbsp;
          CITIES LOADED: {capitals.length}
        </p>
      </div>

      {/* MAP */}
      <div style={{border:'1px solid #2e3f70', borderRadius:'8px', overflow:'hidden', marginBottom:'2rem', height:'400px'}}>
        <MapContainer center={[30, 60]} zoom={2} style={{height:'100%', width:'100%', background:'#0a0e1a'}}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; OpenStreetMap contributors'
          />
          {capitals.filter(c => c.active).map((city) => (
            <Marker
              key={city.id}
              position={[city.latitude, city.longitude]}
              eventHandlers={{ click: () => setSelected(city) }}
            >
              <Popup>
                <div style={{fontFamily:'JetBrains Mono', fontSize:'0.85rem'}}>
                  <strong>{city.name}</strong><br/>
                  {city.country}<br/>
                  {city.latitude}°, {city.longitude}°
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* SEARCH */}
      <div style={{marginBottom:'1.5rem'}}>
        <input
          type="text"
          placeholder="⌕ SEARCH CITIES..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{
            width:'100%', boxSizing:'border-box',
            background:'#0f1628', border:'1px solid #2e3f70',
            borderRadius:'6px', padding:'0.75rem 1rem',
            color:'#00d4ff', fontFamily:'JetBrains Mono', fontSize:'0.9rem',
            outline:'none',
          }}
        />
      </div>

      {/* CITY CARDS */}
      <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(280px, 1fr))', gap:'1.5rem'}}>
        {filteredCapitals.map((city) => (
          <div key={city.id}
            style={{
              background: selected?.id === city.id ? '#1a2240' : '#0f1628',
              border: `1px solid ${selected?.id === city.id ? '#00d4ff' : '#2e3f70'}`,
              borderRadius:'8px',
              overflow:'hidden',
              transition:'all 0.2s',
            }}>

            {/* CARD HEADER — always visible, click to expand */}
            <div
              onClick={() => { setSelected(city); toggleExpanded(city.id) }}
              style={{
                display:'flex', justifyContent:'space-between', alignItems:'center',
                padding:'1rem 1.5rem', cursor:'pointer',
              }}>
              <div>
                <h2 style={{color:'#00d4ff', fontSize:'1.4rem', fontFamily:'Rajdhani', fontWeight:700, margin:0}}>
                  {city.name}
                </h2>
                <p style={{color:'#aabbd4', fontSize:'0.85rem', margin:0}}>{city.country}</p>
              </div>
              <div style={{display:'flex', alignItems:'center', gap:'0.5rem'}}>
                {/* ACTIVE/PASSIVE TOGGLE */}
                <button
                  onClick={(e) => toggleActive(e, city)}
                  style={{
                    background: city.active ? '#0a1f0a' : '#1f0a0a',
                    color: city.active ? '#39ff14' : '#ff6b35',
                    fontSize:'0.7rem', padding:'0.2rem 0.6rem',
                    borderRadius:'4px',
                    border: `1px solid ${city.active ? '#39ff14' : '#ff6b35'}`,
                    cursor:'pointer', fontFamily:'JetBrains Mono',
                  }}>
                  {city.active ? 'ACTIVE' : 'PASSIVE'}
                </button>
                {/* EXPAND ARROW */}
                <span style={{color:'#2e3f70', fontSize:'0.9rem'}}>
                  {expanded[city.id] ? '▲' : '▼'}
                </span>
              </div>
            </div>

            {/* CARD BODY — only visible when expanded */}
            {expanded[city.id] && (
              <div style={{padding:'0 1.5rem 1.5rem', borderTop:'1px solid #1a2240'}}>
                <div style={{marginTop:'1rem'}}>
                  <p style={{color:'#8899bb', fontSize:'0.75rem', margin:0}}>COORDINATES</p>
                  <p style={{color:'#c8d6e8', fontSize:'0.85rem', marginTop:'0.3rem'}}>
                    LAT: {city.latitude}° &nbsp; LON: {city.longitude}°
                  </p>
                </div>
                {city.remarks && (
                  <div style={{marginTop:'0.8rem'}}>
                    <p style={{color:'#8899bb', fontSize:'0.75rem', margin:0}}>REMARKS</p>
                    <p style={{color:'#c8d6e8', fontSize:'0.8rem', marginTop:'0.2rem'}}>{city.remarks}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* FOOTER */}
      <div style={{marginTop:'2rem', borderTop:'1px solid #1a2240', paddingTop:'1rem'}}>
        <p style={{color:'#2e3f70', fontSize:'0.75rem', textAlign:'center'}}>
          GPS/GIS DEVOPS PROJECT — BACKEND: localhost:5000 — FRONTEND: localhost:5173
        </p>
      </div>

    </div>
  )
}

export default App