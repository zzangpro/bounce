import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col, } from 'react-bootstrap';
import { Container } from 'react-bootstrap';
import '../styles/NewsCreatePage.scss'; // 이 파일 내에 해당하는 스타일을 정의해야 함
import HwpDataProcessor from './HwpDataProcessor';
//import { addNews } from '../api/newsAPI'; // API 호출 함수 임포트

const NewsCreatePage = ({ addNewsItem }) => {
  // 현재 날짜를 YYYY-MM-DD 형식으로 초기화
  const today = new Date().toISOString().split('T')[0];
  
  const submitNewsItem = async (newsItem) => {
    try {
        const response = await fetch('http://localhost:5000/news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newsItem),
        });

        if (!response.ok) {
            throw new Error('Something went wrong');
        }

        const data = await response.json();
        console.log('Success:', data);
        addNewsItem(data);  // 데이터를 상위 컴포넌트의 상태에 추가
        // 여기에서 추가 처리를 할 수 있습니다...
    } catch (error) {
        console.error('Error:', error);
    }
};

  // 상태 관리
  const [formData, setFormData] = useState({
    creationDate: today, // 현재 날짜
    updateDate: today, // 업데이트 날짜도 추가해야 할 수 있음
    category1: '', // 선택된 값
    category2: '', // 선택된 값
    category3: '', // 선택된 값
    category4: '', // 선택된 값
    author: '', // 입력된 값
    editor: '', // 입력된 값
    title: '', // 입력된 제목
    subtitle: '', // 입력된 부제목, `MyTable`에서 사용하지 않는다면 제외해도 됨
    content: '', // 입력된 내용, `MyTable`에서 사용하지 않는다면 제외해도 됨
    image: '', // 업로드된 이미지 정보
    status: '' // 상태 정보, 필요에 따라 추가
  });


  const handleHwpData = (processedData) => {
    setFormData({
      ...formData,
      title: processedData.title || '',
      subtitle: processedData.subtitle || '',
      content: processedData.content || '',
      image: processedData.image || ''
    });
  };
  

  // 입력 핸들러
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // 이미지 업로드 핸들러
  const handleImageChange = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('image', file);
  
    try {
      const response = await fetch('http://localhost:5000/upload/image', {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error('Image upload failed');
      }
  
      const data = await response.json();
      setFormData({ ...formData, image: data.imageUrl });  // 이미지 URL을 formData에 저장
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  // 저장 핸들러
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted', formData);
      // addNewsItem 함수를 호출하여 상위 컴포넌트로 데이터 전달
    try {
      const response = await fetch('http://localhost:5000/news', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
  
      if (!response.ok) {
        throw new Error('Something went wrong');
      }
  
      const data = await response.json();
      console.log('Success:', data);
      addNewsItem(data);  // 데이터를 상위 컴포넌트의 상태에 추가
      // 추가적인 성공 처리 로직 (예: 폼 초기화, 성공 알림 표시 등)
    } catch (error) {
      console.error('Error:', error);
      // 사용자에게 에러를 알릴 수 있는 UI 처리 추가
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/news/data'); // 서버 API 경로
        if (!response.ok) {
          throw new Error('Failed to fetch news data');
        }
        const data = await response.json();
        setFormData({
          ...formData,
          title: data.title,
          subtitle: data.subtitle,
          content: data.content,
          image: data.image // 서버에서 이미지 URL을 보내주는 경우
        });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
    fetchData();
  }, []);

  return (
    <Container>
      <HwpDataProcessor onProcessed={handleHwpData} />
      <Form onSubmit={handleSubmit}>
      <Row className="mb-3">
          {['category1', 'category2', 'category3', 'category4'].map((category, index) => (
            <Col xs={12} md={6} key={index}>
              <Form.Group controlId={`form${category.charAt(0).toUpperCase() + category.slice(1)}`}>
                <Form.Label>{`카테고리${index + 1}`}</Form.Label>
                <Form.Control as="select" name={category} value={formData[category]} onChange={handleChange}>
                  <option value="">선택하세요</option>
                  {/* 카테고리 옵션을 동적으로 렌더링 필요 */}
                </Form.Control>
              </Form.Group>
            </Col>
          ))}
        </Row>
        <Form.Group controlId="formTitle">
          <Form.Label>제목</Form.Label>
          <Form.Control type="text" placeholder="제목 입력" name="title" value={formData.title} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formSubtitle">
          <Form.Label>부제목</Form.Label>
          <Form.Control type="text" placeholder="부제목 입력" name="subtitle" value={formData.subtitle} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formContent">
          <Form.Label>내용</Form.Label>
          <Form.Control as="textarea" rows={5} name="content" value={formData.content} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formImage">
          <Form.Label>이미지 업로드</Form.Label>
          <Form.Control type="file" onChange={handleImageChange} />
        </Form.Group>
        <Button variant="primary" type="submit">저장</Button>
      </Form>
    </Container>
  );

};

export default NewsCreatePage;
