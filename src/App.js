import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MyNavbar from './components/MyNavbar';
import MyTable from './components/MyTable';
import NewsCreatePage from './components/NewsCreatePage';
import 'bootstrap/scss/bootstrap.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/main.scss';

const App = () => {
  const [newsData, setNewsData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:3000/news');
      const result = await response.json();
      setNewsData(result);
    };

    fetchData();
  }, []);

  const addNewsItem = async (newsItem) => {
    const response = await fetch('http://localhost:3000/news', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newsItem),
    });
    const result = await response.json();
    setNewsData([...newsData, result]);
  };

  return (
    <Router>
      <div className="App">
        <MyNavbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<MyTable data={newsData} />} />
            <Route path="/create-news" element={<NewsCreatePage addNewsItem={addNewsItem} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
