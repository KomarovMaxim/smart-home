
import { useState, useEffect } from "react";
import DeviceList from "./DeviceList.jsx";
import "./App.css";

function App() {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/devices")
      .then((res) => res.json())
      .then((data) => setDevices(Object.values(data)));
  }, []);

  return (
    <div>
      <h1>Умный дом</h1>
      <DeviceList devices={devices} />
    </div>
  );
}

export default App;
