// /api/newsAPI.js
const BASE_URL = 'http://localhost:5000';

export const addNews = async (newsData) => {
  const response = await fetch(BASE_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newsData),
  });
  return response.json();
};

export const fetchNews = async () => {
  const response = await fetch(BASE_URL);
  const data = await response.json();
  return data;
};
