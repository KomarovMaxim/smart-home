
const API_URL = "http://127.0.0.1:8000";

// Получаем список устройств из FastAPI
export async function getDevices() {
  const response = await fetch(`${API_URL}/devices`);

  if (!response.ok) {
    throw new Error("Не удалось загрузить устройства");
  }

  const data = await response.json();

  return Object.values(data);
}

// Включаем или выключаем устройство
export async function toggleDevice(deviceId) {
  const response = await fetch(
    `${API_URL}/devices/${deviceId}/toggle`,
    {
      method: "POST"
    }
  );

  if (!response.ok) {
    throw new Error("Ошибка переключения устройства");
  }

  return await response.json();
}
