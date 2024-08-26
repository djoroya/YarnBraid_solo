import { useState,useEffect } from 'react'
import './App.css'
import Table from 'react-bootstrap/Table';
import "bootswatch/dist/lux/bootstrap.min.css";


// load simulation from backend
const API = "http://127.0.0.1:5000"
const getSimulation = async () => {
  const response = await fetch(`${API}/simulations`)
  const data = await response.json()
  return data
}


const deleteSimulation = async (simulation_path) => {
  const response = await fetch(`${API}/simulations/${simulation_path}`, {
    method: 'DELETE',
  })
  const data = await response.json()
  return data
}


function copiarTexto(texto) {
  // El texto que deseas copiar
  // Usar la API del portapapeles para copiar el texto
  navigator.clipboard.writeText(texto)
}

function App() {
  
  const [simulations, setSimulations] = useState([])
  const [showall, setShowall] = useState(false)
  const [selected_simulation, setSelected_simulation] = useState("all")
  const fetchSimulations = async () => {
    const simulations = await getSimulation()
    console.log(simulations)
    setSimulations(simulations)
  }
  useEffect(() => {
    fetchSimulations()
  }, [])
  
  const unique_simulation = simulations.map((simulation) => {
    return simulation.function.name
  }
  )
  const unique_simulation_set = new Set(unique_simulation)


  const fcn_showall = (simulation) => {
    const has_parent = simulation.settings_step ? simulation.settings_step.has_parent : false
    if (!has_parent) {
      return (
        <tr key={simulation.simulation_path}>
          <td>{simulation.function.name}</td>
          <td>{simulation.simulation_path}</td>
          <td>{ JSON.stringify(simulation.settings_step)}</td>
          <td>
            
            <button
            onClick={async () => {
              await deleteSimulation(simulation.simulation_path)
              fetchSimulations()
            }
            }
            >
              Delete
            </button>
             
            <button
            onClick={() => {
              copiarTexto(simulation.simulation_path_abs)
            }
            }
            >
              Copy Path
            </button>

          </td>
        </tr>
      )
    } 
    if (showall){
      return (
        <tr key={simulation.simulation_path}>
          <td>{simulation.function.name}</td>
          <td>{simulation.simulation_path}</td>
          <td>{ JSON.stringify(simulation.settings_step)}</td>
          <td>Delete</td>
        </tr>
      )
    }}

  const simulation_component = simulations.map((simulation) => {

    if (selected_simulation === "all") {
      return fcn_showall(simulation)
    } else {
      console.log(simulation.function.name)
      if (simulation.function.name === selected_simulation) {
      return fcn_showall(simulation)
      }
    }
  }
  )


  return(
    <div className="App">
      <button onClick={() => setShowall(!showall)}> {showall ? "Hide all" : "Show all"} </button>
      {/* Selector: Type of simulation */}
      <select 
      name="select"
      onChange={(e) => setSelected_simulation(e.target.value)}
      >
        <option value="all">All</option>
        {[...unique_simulation_set].map((simulation) => {
          return(
            <option 
            value={simulation} 
            key={simulation}
            >
            {simulation}</option>
          )
        })}
      </select>

        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Type of Simulation</th>
              <th>Time</th>
              <th>Result</th>
              <th>actions</th>
            </tr>
          </thead>
          <tbody>
            {simulation_component}
          </tbody>
        </Table>
    </div>
  )
} 

export default App
