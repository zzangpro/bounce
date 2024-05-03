import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MyNavbar from './components/MyNavbar';
import MyTable from './components/MyTable';
import NewsCreatePage from './components/NewsCreatePage';
import EmailsPage from './components/EmailsPage'; // Import the EmailsPage component
import EmailDetailPage from './components/EmailDetailPage';


import 'bootstrap/scss/bootstrap.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/main.scss';

const App = () => {
  const [newsData, setNewsData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('http://localhost:5000/news');
        if (!response.ok) {
          throw new Error('Something went wrong!');
        }
        const result = await response.json();
        setNewsData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const addNewsItem = async (newsItem) => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/news', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newsItem),
      });
      if (!response.ok) {
        throw new Error('Failed to post news item');
      }
      const result = await response.json();
      setNewsData([...newsData, result]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <Router>
      <div className="App">
        <MyNavbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<MyTable data={newsData} />} />
            <Route path="/create-news" element={<NewsCreatePage addNewsItem={addNewsItem} />} />
            <Route path="/emails" element={<EmailsPage />} /> 
            <Route path="/emails/:id" element={<EmailDetailPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
