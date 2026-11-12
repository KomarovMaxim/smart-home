
function DeviceList({ devices }) {
  return (
    <ul>
      {devices.map((device) => (
        <li key={device.id}>
          {device.name} — {device.status}
        </li>
      ))}
    </ul>
  );
}

export default DeviceList;
