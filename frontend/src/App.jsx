import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { getCapitals, getHealth } from './services/api'
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

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [capitalsData, healthData] = await Promise.all([
          getCapitals(),
          getHealth()
        ])
        setCapitals(capitalsData)
        setHealth(healthData)
      } catch (err) {
        setError('Failed to connect to API')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

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
        <MapContainer
          center={[30, 60]}
          zoom={2}
          style={{height:'100%', width:'100%', background:'#0a0e1a'}}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; OpenStreetMap contributors'
          />
          {capitals.map((city) => (
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

      {/* CITY CARDS */}
      <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(280px, 1fr))', gap:'1.5rem'}}>
        {capitals.map((city) => (
          <div key={city.id}
            onClick={() => setSelected(city)}
            style={{
              background: selected?.id === city.id ? '#1a2240' : '#0f1628',
              border: `1px solid ${selected?.id === city.id ? '#00d4ff' : '#2e3f70'}`,
              borderRadius:'8px',
              padding:'1.5rem',
              cursor:'pointer',
              transition:'all 0.2s',
            }}>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'flex-start'}}>
              <div>
                <h2 style={{color:'#00d4ff', fontSize:'1.4rem', fontFamily:'Rajdhani', fontWeight:700}}>
                  {city.name}
                </h2>
                <p style={{color:'#aabbd4', fontSize:'0.85rem'}}>{city.country}</p>
              </div>
              <span style={{
                background:'#1a2240', color:'#39ff14', fontSize:'0.7rem',
                padding:'0.2rem 0.6rem', borderRadius:'4px', border:'1px solid #39ff14'
              }}>ACTIVE</span>
            </div>
            <div style={{marginTop:'1rem', borderTop:'1px solid #1a2240', paddingTop:'1rem'}}>
              <p style={{color:'#8899bb', fontSize:'0.75rem'}}>COORDINATES</p>
              <p style={{color:'#c8d6e8', fontSize:'0.85rem', marginTop:'0.3rem'}}>
                LAT: {city.latitude}° &nbsp; LON: {city.longitude}°
              </p>
            </div>
            {city.remarks && (
              <div style={{marginTop:'0.8rem'}}>
                <p style={{color:'#8899bb', fontSize:'0.75rem'}}>REMARKS</p>
                <p style={{color:'#c8d6e8', fontSize:'0.8rem', marginTop:'0.2rem'}}>{city.remarks}</p>
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