import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MyNavbar from './components/MyNavbar';
import MyTable from './components/MyTable';
import 'bootstrap/scss/bootstrap.scss';
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CSS 추가
import NewsCreatePage from './components/NewsCreatePage'; // 보도자료 작성 컴포넌트
import './styles/main.scss'; // 애플리케이션의 메인 스타일

const App = () => {
  const [newsData, setNewsData] = useState([]);
   // 뉴스 항목을 추가하는 함수
   const addNewsItem = (newItem) => {
    setNewsData(prevNewsData => [...prevNewsData, newItem]);
  };

  useEffect(() => {
    // Flask API에서 데이터를 가져옵니다.
    const fetchData = async () => {
      try {
        const response = await fetch('/data');
        const result = await response.json();
        setNewsData(result); 
      } catch (error) {
        console.error('Error fetching data: ', error);
      }
    };

    fetchData();
  }, []);

  return (
    <Router>
      <div className="App">
        <MyNavbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<MyTable data={newsData} />} />
            <Route path="/create-news" element={<NewsCreatePage addNewsItem={addNewsItem} />} />
            {/* 여기에 더 많은 라우트를 추가할 수 있습니다 */}
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
